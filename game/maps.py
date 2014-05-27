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

  def on_join(self, player):
    color = self.get_next_color()
    x, y = self.find_spawning_point(color)
    player.sprite =  PlayerSprite(x, y, color)
    self.player_sprites.append(player.sprite)
    self.players.append(player)
   
  def find_spawning_point(self, color):
    spawn_map = {"red": (32, 32), "blue": (16*32, 16*32), "green": (16*32, 32), "yellow": (32, 16*32)}
    return spawn_map[color] 

  def get_next_color(self):
    colors = ["red", "blue", "green", "yellow"]
    return colors[len(self.players) - 1]

  def update(self):
    def on_explosion_collide(sprite):
      sprite.active = False

    self.brick_sprites = filter(lambda s: s.active, self.brick_sprites)
    self.bomb_sprites = filter(lambda s: s.active, self.bomb_sprites)
    self.explosion_sprites = filter(lambda s: s.active, self.explosion_sprites)
    new_explosions = []
    for explosion in self.explosion_sprites:
      explosion_targets = self.all_sprites()
      explosion_targets.remove(explosion)
      new_explosions.extend(explosion.update(explosion_targets, on_explosion_collide))
    self.explosion_sprites.extend(new_explosions)
    for bomb in self.bomb_sprites:
      self.explosion_sprites.extend(bomb.update())

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

  def on_drop_bomb(self, player):
    x, y = player.sprite.pos
    self.bomb_sprites.append(BombSprite( x - (PlayerSprite.DIM[0] - BombSprite.DIM[0]) / 2, y - (PlayerSprite.DIM[1] - BombSprite.DIM[1]) / 2, player.bomb_power))

  def pack_objects(self):
    objects = []
    for sprite in self.all_sprites(): 
      packed = sprite.pack()
      objects.append(packed)
    return objects


  def all_sprites(self):
    return self.player_sprites + self.brick_sprites + self.tile_sprites + self.bomb_sprites + self.explosion_sprites

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

    #for i in [ 2*x for x in range(0, 9)]:
    #  for j in [ 2*x for x in range(0, 9)]:
    #    bricks.append(BrickSprite(32 + i*32, 32 + j*32))
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