import threading

import tcp_server, handler

def on_hi(server, connection_id, data):
  handler.send_message(connection_id, {'return': 'ok'})
  print("From connection: %s  Got data: %s" % (connection_id, data))

if __name__ == "__main__":
  server = tcp_server.Server(('127.0.0.1', 13373))
  handler = handler.JSON_EventMap(server)
  server.set_handler(handler)
  handler.set_msg_map({ 'hi': on_hi })

  handler_thread = handler.start_thread()
  server_thread = server.start_thread()

  server_thread.join()

