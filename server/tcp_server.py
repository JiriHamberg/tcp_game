import socket
import select
import struct

import json

#protocol:
#   header                  data
#   2B (=size of u short)   0-(2^16-1)B

class TCPServer(object):
  HEADER_SIZE = 2

  def __init__(self, address, handler):
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.setblocking(False)
    self.address = address
    self.handler = handler
    self.server.bind(self.address)
    
    self.inputs = [self.server]
    self.outputs = []
    self.message_buffers = {} #connection -> (in_buffer, out_buffer)

  def listen(self):
    self.server.listen(5) #max num of queued connections

    while self.inputs:
      readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)

      for s in readable:
        if s is self.server:
          #accept a new connection
          connection, client_address = s.accept()
          connection.setblocking(0)
          self.inputs.append(connection)
          self.message_buffers[connection] = {"in": bytearray(), "out": bytearray()}
        else:
          data = s.recv(1024)
          if data:
            self.message_buffers[s]["in"] += data            
            self.handle_client_data(s, data)
          else:
            #closed connection
            self.close_connection(s)

      for s in writable:
        out_buffer = self.message_buffers[s]["out"]
        buffer_len = len(out_buffer)
        if buffer_len > 0:
          sent = s.send(str(out_buffer))
          if sent == 0:
            #closed connection
            self.close_connection(s)
          self.message_buffers[s]["out"] = out_buffer[sent : ]
        else:
          self.outputs.remove(s)

      for s in exceptional:
        self.close_connection(s)

  def close_connection(self, connection):
    self.inputs.remove(connection)
    if connection in self.outputs:
      self.outputs.remove(connection)
    connection.close()
    del self.message_buffers[connection]

  def send_message(self, connection, message):
    data = struct.pack("H", len(message)) + message
    self.message_buffers[connection]["out"] += data
    if connection not in self.outputs:
      self.outputs.append(connection)

  def handle_client_data(self, connection, data):
    while True:
      in_buffer = self.message_buffers[connection]["in"]
      if len(in_buffer) < 2:
        break
      next_msg_len = struct.unpack("H", str(in_buffer[ : TCPServer.HEADER_SIZE]))[0]
      if len(in_buffer) >= next_msg_len + TCPServer.HEADER_SIZE:
        #we have a complete message
        msg = str(in_buffer[TCPServer.HEADER_SIZE : next_msg_len + TCPServer.HEADER_SIZE])
        self.message_buffers[connection]["in"] = in_buffer[next_msg_len + TCPServer.HEADER_SIZE :]
        self.handler.handle(self, connection, msg) #handle(server, connection, message)
      else:
        break           