def pack_message(message):
    msg = json.dumps(message)
    data = struct.pack("H", len(msg)) + msg
    return data

def unpack_message(message):
  msg_len = struct.unpack("H", message[ : HEADER_SIZE])[0]
  msg = json.loads(message[HEADER_SIZE :])
  return msg
