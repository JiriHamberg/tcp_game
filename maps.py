import random

class Map(object):
  def __init__(self, w, h):
      self.grid = GridFactory.generate_map(w=w, h=h, player_count=2)
  
  def update(self):
    pass

  def on_move(self, symbol, command):
    for y in range(0, len(self.grid)):
     for x in range(0, len(self.grid[0])):
      if self.grid[y][x] == symbol:
        if command == "up":
          self.apply_move(symbol, x, y, x, y + 1)
          return
        elif command == "down":
          self.apply_move(symbol, x, y, x, y - 1)
          return
        elif command == "left":
          self.apply_move(symbol, x, y, x - 1, y)
          return
        elif command == "right":
          self.apply_move(symbol, x, y, x + 1, y)
          return
        else:
          raise Exception("Invalid command for move: must be 'up', 'down', 'left' or 'right', but is '%s'" % (command))
    raise Exception("Could not find symbol '%s' from grid" % (symbol))

  def apply_move(self, symbol, old_x, old_y, x, y ):
    self.grid[y % len(self.grid)][x % len(self.grid[0])] = symbol
    self.grid[old_y][old_x] = ' '

class GridFactory(object):
  @staticmethod
  def generate_map(w=10, h=10, player_count=2):
      grid = []
      for y in range(0, h):
          grid.append([' '] * w)
      grid[0][random.randint(0, w - 1)] = '1'
      grid[h - 1][random.randint(0, w - 1)] = '2'
      return grid