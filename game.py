import game.game_logic as game_logic

import threading, time

if __name__ == '__main__':
  timeout = 99999999
  game_threads = game_logic.GameMain().start()
  for t in game_threads:
    t.join(timeout)
