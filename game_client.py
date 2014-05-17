import socket
import json
import struct
import time
import Queue
import sys
import threading

import server.tcp_io as tcp_io
import server.handler as handler
#import protocol

HEADER_SIZE = 2

def pack_msg(message):
    msg = json.dumps(message)
    data = struct.pack("H", len(msg)) + msg
    return data

class ClientIO(object):
  start_thread = tcp_io._start_thread
  
  def __init__(self, socket):
    self.queue = Queue.Queue()
    self.event_map = handler.JSON_EventMap(self.queue.put)
    self.client = tcp_io.Client(socket, 1, self.event_map.queue)
    self.message_consumer = threading.Thread( target = self.consume )

  def consume(self):
    for _, msg in iter(self.queue.get, None):
      self.client.socket.sendall(pack_msg(msg))

  def start(self):
    t1 = self.event_map.start_thread()
    t2 = self.client.start_thread()
    self.message_consumer.daemon = True
    self.message_consumer.start()


def print_data(data):
  for y in range(0, len(data)):
    print(" ".join(data[y]))

def on_update(_, data):
  print_data(data)

def send_message(message):
  client_io.queue.put( (1, message) )

#if __name__ == "__main__":
  #msg = {'type':'join', 'data': ''}  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 13373))
client_io = ClientIO(s)

client_io.event_map.bind_event("update", on_update)

client_io.start()

while True:
  send_message({"type": "join", "data": ""})
  key = sys.stdin.read(1)
  print("input key was: %s" % (key))

  if key == 'a':
    send_message({"type": "move", "data": {"command": "left"} })
  elif key == 'w':
    send_message({"type": "move", "data": {"command": "up"} })
  elif key == 'd':
    send_message({"type": "move", "data": {"command": "right"} })
  elif key == 's':
    send_message({"type": "move", "data": {"command": "down"} })


 # print "msg len: %s  msg: %s" % unpacked
  #s.close()