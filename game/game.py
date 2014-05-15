import server.tcp_server as tcp_server
import server.handler as handler
import players
import maps
import time


event_handler = handler.JSON_handler()


class Game(object):
  def __init__(self):
    self.event_handler = event_handler
    self.server = tcp_server.TCPServer(('localhost', 13373), self.handler)
    self.map = maps.Map()
    self.players = {}

  def join(self, connection, data):
    symbol = str(len(self.players) + 1)
    self.players[connection] = players.Player(symbol)

  def start(self):
    self.server.listen()


game = Game()


def event_join(server, connection, data):
  game.join(connection, data)

def event_move(server, connection, data):
  game.map.on_move(game.players[connection].symbol, data["command"])

event_handler.bind_event("join", event_join)
event_handler.bind_event("move", event_move)


def update():
  msg = {"type": "update", "map": game.grid }
  for connection, player in game.players:
    event_handler.send_msg(game.server, connection, msg)

last_update = time.time()
fps = 0.5

while True:
  if time.time() - last_update > 1 / fps
    last_update = time.time()
    update()

