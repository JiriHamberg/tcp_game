import random

from utils import *

class Map(object):
  def __init__(self, w, h):
      #self.grid = GridFactory.generate_map(w=w, h=h, player_count=2)
      self.dim = (w, h)
      self.player_sprites = []
      self.brick_sprites = BrickLayout.generate()
      self.tile_sprites = TileLayout.generate()
      self.bomb_sprites = []
      self.explosion_sprites = []
      self.players = []
     
      self.new_sprites = []
      self.updated_sprites = []
      self.deleted_sprites = []

  def on_join(self, player):
    "Handle player joining logic and return a message containing all objects"
    color = self.get_next_color()
    x, y = self.find_spawning_point(color)
    player.sprite =  PlayerSprite(x, y, color)
    self.player_sprites.append(player.sprite)
    self.players.append(player)
    self.new_sprites.append(player.sprite)
    return self.pack_all_objects()

  def find_spawning_point(self, color):
    spawn_map = {"red": (32, 32), "blue": (16*32, 16*32), "green": (16*32, 32), "yellow": (32, 16*32)}
    return spawn_map[color] 

  def get_next_color(self):
    colors = ["red", "blue", "green", "yellow"]
    return colors[len(self.players) - 1]

  def update(self):
    def on_explosion_collide(sprite):
      if type(sprite) is BombSprite:
        sprite.timer = 1
      elif type(sprite) is BrickSprite:
        sprite.active = False

    self.brick_sprites = self.remove_inactive(self.brick_sprites)
    self.bomb_sprites = self.remove_inactive(self.bomb_sprites)
    self.explosion_sprites = self.remove_inactive(self.explosion_sprites)
    new_explosions = []
    for explosion in self.explosion_sprites:
      explosion_targets = self.solid_sprites()
      #explosion_targets.remove(explosion)
      new_explosions.extend(explosion.update(explosion_targets, on_explosion_collide))
    self.new_sprites.extend(new_explosions)
    self.explosion_sprites.extend(new_explosions)
    self.updated_sprites.extend(self.explosion_sprites)
    new_explosions = []
    for bomb in self.bomb_sprites:
      new_explosions.extend(bomb.update())
    self.explosion_sprites.extend(new_explosions)
    self.new_sprites.extend(new_explosions)
    self.updated_sprites.extend(self.bomb_sprites)

  def remove_inactive(self, sprite_list):
    inactive = filter(lambda s: not s.active, sprite_list)
    self.deleted_sprites.extend(inactive)
    return list(set(sprite_list) - set(inactive))

  def on_move(self, player, command):
    my_sprite = player.sprite
    collision_candidates = self.player_sprites + self.brick_sprites + self.tile_sprites + self.bomb_sprites
    collision_candidates.remove(my_sprite)
    if command == "up":
      collision_candidates = filter(lambda s: s.pos[1] <= my_sprite.pos[1] and s.collides(my_sprite)[0], collision_candidates)
      closest = player.velocity if len(collision_candidates) == 0 else min(map(lambda s: s.distance(my_sprite)[1], collision_candidates))
      my_sprite.pos[1] -= min(player.velocity, closest)
    elif command == "down":
      collision_candidates = filter(lambda s: s.pos[1] >= my_sprite.pos[1] and s.collides(my_sprite)[0], collision_candidates)
      closest = player.velocity if len(collision_candidates) == 0 else min(map(lambda s: s.distance(my_sprite)[1], collision_candidates))
      my_sprite.pos[1] += min(player.velocity, closest)
    elif command == "left":
      collision_candidates = filter(lambda s: s.pos[0] <= my_sprite.pos[0] and s.collides(my_sprite)[1], collision_candidates)
      closest = player.velocity if len(collision_candidates) == 0 else min(map(lambda s: s.distance(my_sprite)[0], collision_candidates))
      my_sprite.pos[0] -= min(player.velocity, closest)
    elif command == "right":
      collision_candidates = filter(lambda s: s.pos[0] >= my_sprite.pos[0] and s.collides(my_sprite)[1], collision_candidates)
      closest = player.velocity if len(collision_candidates) == 0 else min(map(lambda s: s.distance(my_sprite)[0], collision_candidates))
      my_sprite.pos[0] += min(player.velocity, closest)
    else:
      raise Exception("Invalid command for move: must be 'up', 'down', 'left' or 'right', but is '%s'" % (command))
    self.updated_sprites.append(my_sprite)

  def on_drop_bomb(self, player):
    x, y = player.sprite.pos
    x_off, y_off = (PlayerSprite.DIM[0] - BombSprite.DIM[0]) / 2, (PlayerSprite.DIM[1] - BombSprite.DIM[1]) / 2
    bomb = BombSprite( x + x_off, y + y_off, player.bomb_power)
    self.bomb_sprites.append(bomb)
    self.new_sprites.append(bomb)

  def pack_objects(self):
    objects = {}
    objects["new"] = map(lambda s: s.pack(), self.new_sprites)
    objects["updated"] = map(lambda s: s.pack(), self.updated_sprites)
    objects["deleted"] = map(lambda s: s.pack(), self.deleted_sprites)
    self.new_sprites, self.updated_sprites, self.deleted_sprites = [], [], []
    return objects

  def pack_all_objects(self):
    objects = {}
    objects["new"] = map(lambda s: s.pack(), self.all_sprites())
    objects["updated"] = []
    objects["deleted"] = []
    return objects

  def all_sprites(self):
    return self.player_sprites + self.brick_sprites + self.tile_sprites + self.bomb_sprites + self.explosion_sprites

  def solid_sprites(self):
    return self.player_sprites + self.brick_sprites + self.tile_sprites + self.bomb_sprites

class BrickLayout(object):
  @staticmethod
  def generate():
    bricks = []

    for x in range(3, 16):
      for y in range(1, 18):
        if not x % 2 == 0 or not y % 2 == 0:
          bricks.append(BrickSprite(32 * x , 32 * y))

    for x in [1, 2, 16, 17]:
      for y in range(3, 16):
        if not x % 2 == 0 or not y % 2 == 0:
          bricks.append(BrickSprite(32 * x , 32 * y))

    return bricks

class TileLayout(object):
  @staticmethod
  def generate():
    tiles = []

    for y in range(0, 19):
      tiles.append(TileSprite(0, y*32))
      tiles.append(TileSprite(18*32, y*32))

    for x in range(1, 18):
      tiles.append(TileSprite(x*32, 0))
      tiles.append(TileSprite(x*32, 18*32))

    for x in [ 2*i for i in range(0, 9)]:
      for y in [ 2*i for i in range(0, 9)]:
        tiles.append(TileSprite(64 + x*32, 64 + y*32))

    return tiles