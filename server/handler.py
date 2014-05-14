import struct
import json


class JSON_handler(object):
  def __init__(self):
    self.msg_map = {}

  def set_msg_map(self, msg_map):
    self.msg_map = msg_map

  def bind_event(self, event_name, event_handler):
    self.msg_map[event_name] = event_handler

  def send_msg(self, server, connection, message):
    server.send_message(connection, json.dumps(message))

  def handle(self, server, connection, data):
    msg = json.loads(data.strip())
    msg_type = msg["type"]
    msg_data = msg["data"]
    self.msg_map[msg_type](server, connection, msg_data)
