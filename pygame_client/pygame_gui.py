import threading
import sys

import pygame
from pygame.locals import *

import sprite_utils
import objects
import sound

class GUI(object):
  def __init__(self, grid, send_message_function):
    self.send_message = send_message_function
    self.grid = grid
    self.down_keys = []
    self.player_positions = {}
    self.object_store = objects.ObjectStore()

    pygame.init()
    pygame.mixer.init()
    sound.SoundEffects.init()
    self.clock = pygame.time.Clock()
    self.screen = pygame.display.set_mode((860,608), pygame.DOUBLEBUF, 32)

    self.player_sprite_mapper = sprite_utils.PlayerSpriteMapper()
    self.brick_sprite_mapper = sprite_utils.BrickSpriteMapper()
    self.bomb_sprite_mapper = sprite_utils.BombSpriteMapper()
    self.item_sprite_mapper = sprite_utils.ItemSpriteMapper()

    self.bind_object_store_events()
    self.set_background_music("dreamtest")

  def bind_object_store_events(self):
    def on_bomb_remove(bomb):
      sound.SoundEffects.explosion.play()
    def on_item_remove(item):
      if item["timer"] > 0:
        sound.SoundEffects.play_random_bling()
    self.object_store.bind_event("remove", "bomb", on_bomb_remove)
    self.object_store.bind_event("remove", "item", on_item_remove)

  def set_background_music(self, song):
    sound.SoundEffects.play_background(song)

  def update(self, data):
    for sprite in data["new"]:
      self.object_store.add(sprite)
    for sprite in data["updated"]:
      self.object_store.update(sprite)
    for sprite in data["deleted"]:
      self.object_store.remove(sprite)

  def render(self):
    self.screen.fill((255,255,255))
    for sprite in self.object_store.all():
      if sprite["type"] == "player":
        self.draw_player(sprite)
      elif sprite["type"] == "brick":
        self.draw_brick(sprite)
      elif sprite["type"] == "bomb":
        self.draw_bomb(sprite)
      elif sprite["type"] == "explosion":
        self.draw_explosion(sprite)
      elif sprite["type"] == "tile":
        self.draw_tile(sprite)
      elif sprite["type"] == "item":
        self.draw_item(sprite)
    pygame.display.flip()

  def draw_player(self, sprite):
    sprite_color = sprite["color"]
    if sprite_color not in self.player_positions:
      self.player_positions[sprite_color] = {"direction": "down", "pos": sprite["pos"], "frame": 0}
    image = self.get_player_animation_frame(sprite_color, sprite["pos"])
    x, y = self.player_sprite_mapper.align(sprite)
    self.screen.blit(image, (x, y))

  def draw_brick(self, sprite):
    image = self.brick_sprite_mapper.sprite_at(2, 4)
    x, y = self.brick_sprite_mapper.align(sprite)
    self.screen.blit(image, (x, y))

  def draw_tile(self, sprite):
    image = self.brick_sprite_mapper.sprite_at(4, 5)
    x, y = self.brick_sprite_mapper.align(sprite)
    self.screen.blit(image, (x, y))

  def draw_item(self, sprite):
    x, y = self.item_sprite_mapper.align(sprite)
    color = {"bomb_power": "blue", "bomb_speed": "green"}[sprite["item_type"]]
    animation = self.item_sprite_mapper.animation(color)
    image = animation[sprite["timer"] % len(animation)]
    self.screen.blit(image, (x, y))

  def draw_bomb(self, sprite):
    animation = self.bomb_sprite_mapper.bomb_animation()
    timer = sprite["timer"]
    start_timer = sprite["timer_start"]
    frame = int((len(animation) - 1) - (timer / float(start_timer)) * (len(animation) - 1))
    self.bomb_sprite_mapper.draw_frame(self.screen, sprite, animation, frame)

  def draw_explosion(self, sprite):
    animation = self.bomb_sprite_mapper.explosion_animation()
    timer = sprite["timer"]
    start_timer = sprite["timer_start"]
    frame = int((len(animation) - 1) - (timer / float(start_timer)) * (len(animation) - 1))
    self.bomb_sprite_mapper.draw_frame(self.screen, sprite, animation, frame)

  def get_player_animation_frame(self, color, new_pos):
    state = self.player_positions[color]
    idle = True
    old_direction = state["direction"]
    direction = old_direction
    old_pos = state["pos"]
    if old_pos[0] - new_pos[0] > 0:
      idle = False
      direction = "left"
    elif old_pos[0] - new_pos[0] < 0:
      idle = False
      direction = "right"
    elif old_pos[1] - new_pos[1] > 0:
      idle = False
      direction = "up"
    elif old_pos[1] - new_pos[1] < 0:
      idle = False
      direction = "down"

    if direction == old_direction:
      frame = state["frame"] + 1
    else:
      frame = 0
    state["frame"] = frame
    state["pos"] = new_pos
    state["direction"] = direction
    animation = self.player_sprite_mapper.get_animation(direction, idle)  #sprite_utils.PlayerSprite.get_animation(direction, idle)
    return animation[frame % len(animation)]

  def send_move_command(self):
    for key in self.down_keys:
      if key == K_a:
        self.send_message({"type": "move", "data": {"command": "left"} })
      elif key == K_w:
        self.send_message({"type": "move", "data": {"command": "up"} })
      elif key == K_d:
        self.send_message({"type": "move", "data": {"command": "right"} })
      elif key == K_s:
        self.send_message({"type": "move", "data": {"command": "down"} })
      elif key == K_SPACE:
        self.send_message({"type": "bomb", "data": "" })

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == KEYDOWN:
          self.down_keys.append(event.key)
        if event.type == KEYUP:
          self.down_keys.remove(event.key)

      self.send_move_command()
      self.clock.tick(50)
      self.render()
      #pygame.display.update()

  def start_thread(self):
    thread = threading.Thread(target=self.run)
    thread.daemon = True
    thread.start()
    return thread
