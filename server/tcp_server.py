import socket
import select
import struct
import uuid
import threading
import Queue

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


def _start_thread(self):
  thread = threading.Thread(target = self.run)
  thread.start()
  return thread

class Server(object):
  start_thread = _start_thread
  HEADER_SIZE = 2

  def __init__(self, address):
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.setblocking(True)
    self.address = address
    self.server_socket.bind(self.address)
    self.input_dispatcher = InputDispatcher(self)
    self.output_dispatcher = OutputDispatcher(self)
    self.clients = {}
    self.handler = None

  def set_handler(self, handler):
    self.handler = handler

  def dispatch_message(self, connection_id, message):
    self.output_dispatcher.queue.put( (connection_id, message) )

  def run(self):
    self.input_dispatcher.start_thread()
    self.output_dispatcher.start_thread()
    self.server_socket.listen(5) #max num of queued connections

    for client_socket, client_address in iter(self.server_socket.accept, None):
      client_socket.setblocking(True)
      connection_id = uuid.uuid4()
      client = Client(client_socket, connection_id, self.input_dispatcher.queue)
      self.clients[connection_id] = client
      client.start_thread()

class OutputDispatcher(object):
  start_thread = _start_thread

  def __init__(self, server):
    self.server = server
    self.queue = Queue.Queue()

  def create_packet(self, message):
    return struct.pack("H", len(message)) + message

  def run(self):
    for receiver_id, message in iter(self.queue.get, None):
      if receiver_id in self.server.clients:         
        self.server.clients[receiver_id].socket.sendall(self.create_packet(message))

class InputDispatcher(object):
  start_thread = _start_thread

  def __init__(self, server):
    self.server = server
    self.queue = Queue.Queue()  

  def run(self):
    for sender_id, message in iter(self.queue.get, None):
      self.server.handler.queue.put((sender_id, message))

class Client(object):
  TCP_BUFFER_SIZE = 1024
  start_thread = _start_thread

  def __init__(self, socket, connection_id, packet_queue):
    self.socket = socket
    self.connection_id = connection_id
    self.packet_queue = packet_queue
    self.data_buffer = bytearray()

  def process_client_data(self, data):
    self.data_buffer += data
    while True:
      data_buffer = self.data_buffer
      if len(data_buffer) < 2:
        break
      next_msg_len = struct.unpack("H", str(data_buffer[ : Server.HEADER_SIZE]))[0]
      if len(data_buffer) >= next_msg_len + Server.HEADER_SIZE:
        #we have a complete message
        msg = str(data_buffer[Server.HEADER_SIZE : next_msg_len + Server.HEADER_SIZE])
        self.data_buffer = data_buffer[next_msg_len + TCPServer.HEADER_SIZE :]
        self.packet_queue.put((self.connection_id, msg), block = True) #handle(server, connection, message)
      else:
        break

  def run(self):
    for data in iter(lambda: self.socket.recv(Client.TCP_BUFFER_SIZE), ''):
      self.process_client_data(data)
    #connection closed
