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
    self.active = True

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

class BrickSprite(Sprite):
  def pack(self):
    packed = Sprite.pack(self)
    packed["type"] = "brick"
    return packed

class BombSprite(Sprite):
  def __init__(self, x, y, power, timer=50):
    Sprite.__init__(self, x, y, 32, 32)
    self.timer_start = timer
    self.timer = timer
    self.power = power

  def update(self):
    if active == False:
      return []
    self.timer -= 1
    if timer <= 0:
      return self.explode()
    else:
      return []

  def explode(self):
    self.active = False
    explosions = []
    explosions.append(ExplosionSprite(self.pos[0] - self.dim[0], self.pos[1], self.power, "left"))
    explosions.append(ExplosionSprite(self.pos[0] + self.dim[0], self.pos[1], self.power, "right"))
    explosions.append(ExplosionSprite(self.pos[0], self.pos[1] - self.dim[1] , self.power, "up"))
    explosions.append(ExplosionSprite(self.pos[0], self.pos[1] + self.dim[1] , self.power, "down"))
    return explosions

  def pack(self):
    packed = Sprite.pack(self)
    packed["type"] = "bomb"
    packed["timer"] = self.timer
    packed["timer_start"] = self.timer_start
    return packed

class ExplosionSprite(Sprite):
  def __init__(self, x, y, power, direction, timer=10):
    self.power = power
    self.direction = direction
    self.timer = timer

  def pack(self):
    packed = Sprite.pack(self)
    packed["type"] = "explosion"
    return packed

  def update(self, targets, collision_callback):
    #assert(self.active == True)
    if active == False:
      return []
    self.timer -= 1
    if timer <= 0:
      self.active = False
      for sprite in targets:
        if self.collides(sprite):
          collision_callback(sprite)
          return []
      return self.spawn_explosions()

  def spawn_explosions(self):
    explosions = []
    if power <= 0:
      return explosions
    if direction == "up":
      explosions.append(Explosion(self.pos[0], self.pos[1] - self.dim[1], self.power - 1, direction))
    elif direction == "down":
       explosions.append(Explosion(self.pos[0], self.pos[1] + self.dim[1], self.power - 1, direction))
    elif direction == "left":
      explosions.append(Explosion(self.pos[0] - self.dim[0], self.pos[1], self.power - 1, direction))
    elif direction == "right":
      explosions.append(Explosion(self.pos[0] + self.dim[0], self.pos[1], self.power - 1, direction))
    else:
      raise Exception("Invalid direction: %s" % (direction))
    return explosions


