import math

class Sprite(object):
  @staticmethod
  def _line_collides(a_1, a_2, b_1, b_2):
    return ((a_1 < b_1 and b_1 < a_2) or (a_1 < b_2 and b_2 < a_2)) or \
           ((b_1 < a_1 and a_1 < b_2) or (b_1 < a_2 and a_2 < b_2)) or (a_1 == b_1 and a_2 == b_2)
  
  @staticmethod
  def _line_distance(a_1, a_2, b_1, b_2):
    if (a_1 < b_1 and b_2 < a_2) or (b_1 < a_1 and a_2 < b_2):
      return 0.0
    return min(abs(a_2 - b_1), abs(a_1 - b_2))

  def __init__(self, x, y, w, h):
    self.pos = [x, y]
    self.dim = (w, h)

  def collides(self, other):
    return (Sprite._line_collides(self.pos[0], self.pos[0] + self.dim[0], other.pos[0], other.pos[0] + other.dim[0]),
           Sprite._line_collides(self.pos[1], self.pos[1] + self.dim[1], other.pos[1], other.pos[1] + other.dim[1]))
  
  def distance(self, other):
    return (Sprite._line_distance(self.pos[0], self.pos[0] + self.dim[0], other.pos[0], other.pos[0] + other.dim[0]),
            Sprite._line_distance(self.pos[1], self.pos[1] + self.dim[1], other.pos[1], other.pos[1] + other.dim[1]))

  def pack(self):
    return {"pos": self.pos, "dim": self.dim}

class PlayerSprite(Sprite):
  def __init__(self, x, y, w, h, color):
    Sprite.__init__(self, x, y, w, h)
    self.type = "player"
    self.color = color

  def pack(self):
    packed = Sprite.pack(self)
    packed["type"] = self.type
    packed["color"] = self.color
    return packed