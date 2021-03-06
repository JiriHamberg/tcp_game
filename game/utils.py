import math, time

def get_current_millis():
  return int(time.time() * 1000)

class Sprite(object):
  SPRITE_ID = 1

  @staticmethod
  def _line_collides(a_1, a_2, b_1, b_2):
    return ((a_1 < b_1 and b_1 < a_2) or (a_1 < b_2 and b_2 < a_2)) or \
           ((b_1 < a_1 and a_1 < b_2) or (b_1 < a_2 and a_2 < b_2)) or (a_1 == b_1 and a_2 == b_2)
  
  @staticmethod
  def _line_distance(a_1, a_2, b_1, b_2):
    #if (a_1 < b_1 and b_2 < a_2) or (b_1 < a_1 and a_2 < b_2):
    #  return 0.0
    return min(abs(a_2 - b_1), abs(a_1 - b_2))

  def __init__(self, x, y, w, h):
    self.pos = [x, y]
    self.dim = (w, h)
    self.active = True
    self.sprite_id = Sprite.SPRITE_ID
    Sprite.SPRITE_ID += 1

  def collides(self, other):
    return (Sprite._line_collides(self.pos[0], self.pos[0] + self.dim[0], other.pos[0], other.pos[0] + other.dim[0]),
           Sprite._line_collides(self.pos[1], self.pos[1] + self.dim[1], other.pos[1], other.pos[1] + other.dim[1]))
  
  def distance(self, other):
    return (Sprite._line_distance(self.pos[0], self.pos[0] + self.dim[0], other.pos[0], other.pos[0] + other.dim[0]),
            Sprite._line_distance(self.pos[1], self.pos[1] + self.dim[1], other.pos[1], other.pos[1] + other.dim[1]))

  def pack(self):
    return {"pos": self.pos, "dim": self.dim, "sprite_id": self.sprite_id}

  def move_no_collision(self, direction, distance, collision_candidates):
    moved = [0.0, 0.0]
    if direction == "up":
      collision_candidates = filter(lambda s: s.pos[1] <= self.pos[1] and s.collides(self)[0], collision_candidates)
      closest = distance if len(collision_candidates) == 0 else min(map(lambda s: s.distance(self)[1], collision_candidates))
      moved[1] = min(distance, closest)
      self.pos[1] -= moved[1]
    elif direction == "down":
      collision_candidates = filter(lambda s: s.pos[1] >= self.pos[1] and s.collides(self)[0], collision_candidates)
      closest = distance if len(collision_candidates) == 0 else min(map(lambda s: s.distance(self)[1], collision_candidates))
      moved[1] = min(distance, closest)
      self.pos[1] += moved[1]
    elif direction == "left":
      collision_candidates = filter(lambda s: s.pos[0] <= self.pos[0] and s.collides(self)[1], collision_candidates)
      closest = distance if len(collision_candidates) == 0 else min(map(lambda s: s.distance(self)[0], collision_candidates))
      moved[0] = min(distance, closest)
      self.pos[0] -= moved[0]
    elif direction == "right":
      collision_candidates = filter(lambda s: s.pos[0] >= self.pos[0] and s.collides(self)[1], collision_candidates)
      closest = distance if len(collision_candidates) == 0 else min(map(lambda s: s.distance(self)[0], collision_candidates))
      moved[0] = min(distance, closest)
      self.pos[0] += moved[0]
    else:
      raise Exception("Invalid direction: must be 'up', 'down', 'left' or 'right', but is '%s'" % (command))
    return moved

class PlayerSprite(Sprite):
  DIM = (24, 24)
  def __init__(self, x, y, color):
    Sprite.__init__(self, x, y, PlayerSprite.DIM[0], PlayerSprite.DIM[1])
    self.type = "player"
    self.color = color
    self.active = False
    self.direction = "down"
    self.last_state_change = get_current_millis()

  #decorateter pattern
  def move_no_collision(self, direction, distance, collision_candidates):
    moved = Sprite.move_no_collision(self, direction, distance, collision_candidates)
    new_active = sum(moved) != 0
    if self.direction != direction or new_active != self.active:
      self.last_state_change = get_current_millis()
    self.active = new_active
    self.direction = direction

  def pack(self):
    packed = Sprite.pack(self)
    packed["type"] = self.type
    packed["color"] = self.color
    packed["active"] = self.active
    packed["direction"] = self.direction
    packed["last_state_change"] = self.last_state_change
    return packed

class BrickSprite(Sprite):
  DIM = (32, 32)
  def __init__(self, x, y):
    Sprite.__init__(self, x, y, BrickSprite.DIM[0], BrickSprite.DIM[1])
  def pack(self):
    packed = Sprite.pack(self)
    packed["type"] = "brick"
    return packed

class TileSprite(Sprite):
  DIM = (32, 32)
  def __init__(self, x, y):
    Sprite.__init__(self, x, y, TileSprite.DIM[0], TileSprite.DIM[1])
  def pack(self):
    packed = Sprite.pack(self)
    packed["type"] = "tile"
    return packed


class BombSprite(Sprite):
  DIM = (18, 18)
  def __init__(self, x, y, power, timer=100):
    Sprite.__init__(self, x, y, BombSprite.DIM[0], BombSprite.DIM[1])
    self.timer_start = timer
    self.timer = timer
    self.power = power

  def update(self):
    if not self.active:
      return []
    self.timer -= 1
    if self.timer <= 0:
      return self.explode()
    else:
      return []

  def explode(self):
    self.active = False
    explosions = []
    x_off, y_off = (self.dim[0] - ExplosionSprite.DIM[0]) / 2, (self.dim[1] - ExplosionSprite.DIM[1]) / 2
    explosions.append(ExplosionSprite(x_off + self.pos[0], y_off + self.pos[1], 0, "left"))
    explosions.append(ExplosionSprite(x_off + self.pos[0] - self.dim[0], y_off + self.pos[1], self.power - 1, "left"))
    explosions.append(ExplosionSprite(x_off + self.pos[0] + self.dim[0], y_off + self.pos[1], self.power - 1, "right"))
    explosions.append(ExplosionSprite(x_off + self.pos[0], y_off + self.pos[1] - self.dim[1] , self.power - 1, "up"))
    explosions.append(ExplosionSprite(x_off + self.pos[0], y_off + self.pos[1] + self.dim[1] , self.power - 1, "down"))
    return explosions

  def pack(self):
    packed = Sprite.pack(self)
    packed["type"] = "bomb"
    packed["timer"] = self.timer
    packed["timer_start"] = self.timer_start
    return packed

class ExplosionSprite(Sprite):
  DIM = (18, 18)
  def __init__(self, x, y, power, direction, timer=10):
    Sprite.__init__(self, x, y, ExplosionSprite.DIM[0], ExplosionSprite.DIM[1])
    self.power = power
    self.direction = direction
    self.timer = timer
    self.timer_start = timer

  def pack(self):
    packed = Sprite.pack(self)
    packed["type"] = "explosion"
    packed["timer"] = self.timer
    packed["timer_start"] = self.timer_start
    return packed

  def update(self, targets, collision_callback):
    #assert(self.active == True)
    if self.active == False:
      return []
    collided = False
    for sprite in targets:
      if all(self.collides(sprite)):
        #self.active = False
        collided = True
        collision_callback(sprite)
    self.timer -= 1
    if self.timer == self.timer_start - 1 and not collided:
      return self.spawn_explosions()
    if self.timer <= 0:
      self.active = False
    return []

  def spawn_explosions(self):
    explosions = []
    if self.power <= 0:
      return explosions
    if self.direction == "up":
      explosions.append(ExplosionSprite(self.pos[0], self.pos[1] - self.dim[1], self.power - 1, self.direction))
    elif self.direction == "down":
       explosions.append(ExplosionSprite(self.pos[0], self.pos[1] + self.dim[1], self.power - 1, self.direction))
    elif self.direction == "left":
      explosions.append(ExplosionSprite(self.pos[0] - self.dim[0], self.pos[1], self.power - 1, self.direction))
    elif self.direction == "right":
      explosions.append(ExplosionSprite(self.pos[0] + self.dim[0], self.pos[1], self.power - 1, self.direction))
    else:
      raise Exception("Invalid direction: %s" % (self.direction))
    return explosions

class ItemSprite(Sprite):
  DIM = (32, 32)
  def __init__(self, x, y, item_type, timer=300):
    Sprite.__init__(self, x, y, ItemSprite.DIM[0], ItemSprite.DIM[1])
    self.active = True
    self.timer = timer
    self.timer_start = timer
    self.item_type = item_type

  def update(self, targets, collision_callback):
    if self.active == False:
      return
    collided = False
    for sprite in targets:
      if all(self.collides(sprite)):
        collision_callback(sprite, self.item_type)
        self.active = False
        break
    self.timer -= 1
    if self.timer <= 0:
      self.active = False

  def pack(self):
    packed = Sprite.pack(self)
    packed["type"] = "item"
    packed["timer"] = self.timer
    packed["timer_start"] = self.timer_start
    packed["item_type"] = self.item_type
    return packed