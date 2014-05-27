import threading
import sys

import pygame
from pygame.locals import *

import sprite_utils
#import sprite_utils

class GUI(object):
  def __init__(self, grid, send_message_function):
    self.send_message = send_message_function
    self.grid = grid
    pygame.init()
    self.clock = pygame.time.Clock()
    self.screen = pygame.display.set_mode((860,640), pygame.DOUBLEBUF, 32)
    self.down_keys = []
    self.player_positions = {}

    self.player_sprite_mapper = sprite_utils.PlayerSpriteMapper()
    self.brick_sprite_mapper = sprite_utils.BrickSpriteMapper()
    self.bomb_sprite_mapper = sprite_utils.BombSpriteMapper()

  def render(self, data):
    self.screen.fill((255,255,255))
    for sprite in data:
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
      #self.draw()
      #pygame.display.update()

  def start_thread(self):
    thread = threading.Thread(target=self.run)
    thread.daemon = True
    thread.start()
    return thread
