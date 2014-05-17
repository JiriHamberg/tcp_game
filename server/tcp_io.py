import socket
import select
import struct
import uuid
import threading
import Queue

#protocol:
#   header                  data
#   2B (=size of u short)   0-(2^16-1)B

def _start_thread(self):
  thread = threading.Thread(target = self.run)
  thread.daemon = True
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
        try:         
          self.server.clients[receiver_id].socket.sendall(self.create_packet(message))
        except Exception:
          pass

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
        msg = str(data_buffer[Server.HEADER_SIZE : next_msg_len + Server.HEADER_SIZE])
        self.data_buffer = data_buffer[next_msg_len + Server.HEADER_SIZE :]
        self.packet_queue.put((self.connection_id, msg), block = True) #handle(server, connection, message)
      else:
        break

  def run(self):
    for data in iter(lambda: self.socket.recv(Client.TCP_BUFFER_SIZE), ''):
      self.process_client_data(data)
    #connection closed
