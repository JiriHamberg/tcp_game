import socket
import json
import struct

HEADER_SIZE = 2

class Player_client(object):
  pass  


def pack_msg(message):
    msg = json.dumps(message)
    data = struct.pack("H", len(msg)) + msg
    return data

def unpack_msg(message):
  msg_len = struct.unpack("H", message[ : HEADER_SIZE])[0]
  msg = json.loads(message[HEADER_SIZE :])
  return (msg_len, msg)

if __name__ == "__main__":
  msg = {'type':'hi', 'data': "trolololololo"*500}
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('127.0.0.1', 13373))
  s.sendall(pack_msg(msg))
  result = s.recv(1024) #json.loads(s.recv(1024))
  unpacked = unpack_msg(result)
  print "msg len: %s  msg: %s" % unpacked
  s.close()