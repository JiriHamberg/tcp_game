import random

from utils import Sprite, PlayerSprite

class Map(object):
  def __init__(self, w, h):
      #self.grid = GridFactory.generate_map(w=w, h=h, player_count=2)
      self.dim = (w, h)
      self.player_sprites = []
      self.brick_sprites = []
      self.tile_sprites = []
      self.players = []

  def on_join(self, player):
    pos = self.find_spawning_point(player)
    player.sprite =  PlayerSprite(pos[0], pos[1], 50, 50, "red")
    self.player_sprites.append(player.sprite)
    self.players.append(player)
   
  def find_spawning_point(self, color):
    return (100, 100)  

  def update(self):
    pass

  def on_move(self, player, command):
    my_sprite = player.sprite
    collision_candidates = self.player_sprites + self.brick_sprites + self.tile_sprites 
    collision_candidates.remove(my_sprite)
    if command == "up":
      collision_candidates = filter(lambda s: s.pos[1] >= my_sprite.pos[1] and s.collides(my_sprite)[0], collision_candidates)
      closest = player.velocity if len(collision_candidates) == 0 else min(map(lambda s: s.distance(my_sprite)[1], collision_candidates))
      my_sprite.pos[1] += min(player.velocity, closest)
    elif command == "down":
      collision_candidates = filter(lambda s: s.pos[1] <= my_sprite.pos[1] and s.collides(my_sprite)[0], collision_candidates)
      closest = player.velocity if len(collision_candidates) == 0 else min(map(lambda s: s.distance(my_sprite)[1], collision_candidates))
      my_sprite.pos[1] -= min(player.velocity, closest)
    elif command == "left":
      collision_candidates = filter(lambda s: s.pos[0] >= my_sprite.pos[0] and s.collides(my_sprite)[1], collision_candidates)
      closest = player.velocity if len(collision_candidates) == 0 else min(map(lambda s: s.distance(my_sprite)[0], collision_candidates))
      my_sprite.pos[0] += min(player.velocity, closest)
    elif command == "right":
      collision_candidates = filter(lambda s: s.pos[0] <= my_sprite.pos[0] and s.collides(my_sprite)[1], collision_candidates)
      closest = player.velocity if len(collision_candidates) == 0 else min(map(lambda s: s.distance(my_sprite)[0], collision_candidates))
      my_sprite.pos[0] -= min(player.velocity, closest)
    else:
      raise Exception("Invalid command for move: must be 'up', 'down', 'left' or 'right', but is '%s'" % (command))


  def pack_objects(self):
    objects = []
    for sprite in self.player_sprites + self.brick_sprites + self.tile_sprites: 
      packed = sprite.pack()
      objects.append(packed)
    return objects

  #def apply_move(self, color, old_x, old_y, x, y ):
  #  self.grid[y % len(self.grid)][x % len(self.grid[0])] = color
  #  self.grid[old_y][old_x] = ' '


class GridFactory(object):
  @staticmethod
  def generate_map(w=10, h=10, player_count=2):
      grid = []
      for y in range(0, h):
          grid.append([' '] * w)
      grid[0][random.randint(0, w - 1)] = '1'
      grid[h - 1][random.randint(0, w - 1)] = '2'
      return grid