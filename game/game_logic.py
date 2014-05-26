import server.tcp_io as tcp_io
import server.handler as handler

import game.players as players
import game.maps as maps

import time
import threading

class GameLogic(object):
  def __init__(self, server):
    self.max_player_count = 2
    self.server = server
    self.map = maps.Map(25, 15)
    self.players = {}

  def event_join(self, connection_id, data):
    if len(self.players) == self.max_player_count:
      self.server.send_message(connection_id, {"type": "rejected", "data": "GAME_FULL"})
      return
    color = str(len(self.players) + 1)
    player = players.Player(color)
    self.players[connection_id] = player
    self.map.on_join(player)

  def event_leave(self, connection_id):
    if connection_id in self.players:
      del self.players[connection_id]

  def event_move(self, connection_id, data):
    if connection_id in self.players:
      self.map.on_move(self.players[connection_id], data["command"])

  def event_bomb(self, connection_id, data):
    if connection_id in self.players:
      player = self.players[connection_id]
      if player.can_drop_bomb():
        self.map.on_drop_bomb(player)
        player.on_drop_bomb()

  def update(self):
    self.map.update()
    for k in self.players:
      self.players[k].update()
    msg = {"type": "update", "data": self.map.pack_objects()}
    for connection_id in self.players:
      self.server.send_message(connection_id, msg)

class GameServer(object):
  FPS = 20.0
  def __init__(self):
    self.server = tcp_io.Server(('127.0.0.1', 13373))
    self.event_handler = handler.JSON_EventMap(self.server.dispatch_message)
    self.server.set_handler(self.event_handler)
    self.main_loop_function = None

  def _main_loop(self):
    while True:
      time.sleep(1.0 / self.FPS)
      self.main_loop_function()

  def bind_event(self, event_name, event_function):
    self.event_handler.bind_event(event_name, event_function)

  def bind_connection_closed(self, on_connection_closed_function):
    self.event_handler.set_on_connection_closed(on_connection_closed_function)

  def bind_main_loop(self, main_loop_function):
    self.main_loop_function = main_loop_function

  def send_message(self, connection_id, message):
    self.event_handler.send_message(connection_id, message)

  def start(self):
    threads = []
    threads.append(self.event_handler.start_thread())
    threads.append(self.server.start_thread())
    main_thread = threading.Thread(target=self._main_loop)
    main_thread.daemon = True 
    main_thread.start()
    threads.append(main_thread)
    return threads

class GameMain(object):
  def __init__(self):
    self.game_server = GameServer()
    self.game_logic = GameLogic(self.game_server)

  def bind_events(self):
    self.game_server.bind_main_loop(self.game_logic.update)
    self.game_server.event_handler.set_on_connection_closed(self.game_logic.event_leave)
    self.game_server.event_handler.bind_event("join", self.game_logic.event_join)
    self.game_server.event_handler.bind_event("move", self.game_logic.event_move)
    self.game_server.event_handler.bind_event("bomb", self.game_logic.event_bomb)

  def start(self):
    """ Entry point to the game. Binds game logic events to game server events and starts the server.
        Returns the list of threads started.
    """
    self.bind_events()
    return self.game_server.start()

