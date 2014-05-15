import random

class Map(object):
    def __init__(self, w, h):
        self.grid = GridFactory.generate_map(w=w, h=h, player_count=2)
    def update(self):

    def on_move(self, symbol, command):
      for (x, y) in ( (i, j) for j in range(0, len(self.grid)) for i in range(0, len(self.grid[0])) ):
        if self.grid[y][x] == symbol:
          if command == "up":
            self.apply_move(symbol, x, y, x, y + 1)
          elif command == "down":
            self.apply_move(symbol, x, y, x, y - 1)
          elif command == "left":
            self.apply_move(symbol, x, y, x - 1, y)
          elif command == "right":
            self.apply_move(symbol, x, y, x + 1, y)
          else:
            raise Exception("Invalid command for move: must be 'up', 'down', 'left' or 'right', but is '%s'" % (command))
      raise Exception("Could not find symbol '%s' from grid" % (symbol))

    def apply_move(self, symbol, old_x, old_y, x, y ):
      self.grid[old_y][old_x] = ' '
      self.grid[y % len(self.grid)][x % len(self.grid[0])] = symbol

class GridFactory(object):
    @staticmethod
    def generate_map(self, w=10, h=10, player_count=2):
        grid = []
        for h in range(0, n):
            grid[h] = [' '] * w
        grid[0][random.randint(0, w - 1)] = '1'
        grid[n - 1][random.randint(0, w - 1)] = '2'
        return grid