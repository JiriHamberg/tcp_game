import server.tcp_io as tcp_io
import server.handler as handler
import players
import maps

import time

#event_handler = handler.JSON_EventMap()

class Game(object):
  def __init__(self):
    self.server = tcp_io.Server(('127.0.0.1', 13373))
    self.event_handler = handler.JSON_EventMap(self.server.dispatch_message)
    self.server.set_handler(self.event_handler)
    self.map = maps.Map(10, 10)
    self.players = {}

  def join(self, connection_id):
    symbol = str(len(self.players) + 1)
    self.players[connection_id] = players.Player(symbol)

  def start(self):
    self.event_handler.start_thread()
    self.server.start_thread()

game = Game()


def event_join(connection_id, data):
  print("event join")
  game.join(connection_id)

def event_move(connection_id, data):
  game.map.on_move(game.players[connection_id].symbol, data["command"])


game.event_handler.bind_event("join", event_join)
game.event_handler.bind_event("move", event_move)


def update():
  msg = {"type": "update", "data": game.map.grid }
  for connection_id in game.players:
    game.event_handler.send_message(connection_id, msg)


game.start()
last_update = time.time()
fps = 0.5

while True:
  print "game loop"
  #if time.time() - last_update > 1 / fps:
  #  last_update = time.time()
  time.sleep(1.0 / fps)
  update()

