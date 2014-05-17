import struct
import json
import threading
import Queue

class JSON_EventMap(object):
  def __init__(self, send_message_function):
    """
        @argument send_message_function: describes how to to 
          communicate with the event invoker 
    """
    #self.server = server
    self._send_message_function = send_message_function
    self.queue = Queue.Queue()
    self.msg_map = {}

  def set_msg_map(self, msg_map):
    self.msg_map = msg_map

  def bind_event(self, event_name, event_handler):
    self.msg_map[event_name] = event_handler

  def send_message(self, connection_id, message):
    #self.server.dispatch_message( connection_id, json.dumps(message) )
    self._send_message_function( connection_id, json.dumps(message) )

  def handle(self, connection_id, data):
    msg = json.loads(data.strip())
    msg_type = msg["type"]
    msg_data = msg["data"]
    self.msg_map[msg_type](connection_id, msg_data)

  def run(self):
    """ Listens for new messages and handles them forever """
    for next_msg in iter(self.queue.get, None):
      self.handle(*next_msg)

  def start_thread(self):
    thread = threading.Thread(target = self.run)
    thread.daemon = True
    thread.start()
    return thread
