import tcp_server, handler

if __name__ == "__main__":
  handler = handler.JSON_handler()

  def on_hi(server, connection, data):
    handler.send_msg(server, connection, {'return': 'ok'})
    print("Got data: %s" % (data))

  handler.set_msg_map({ 'hi': on_hi })
  server = tcp_server.TCPServer(('127.0.0.1', 13373), handler)
  server.listen()