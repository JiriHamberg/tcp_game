import threading
import sys

import pygame
from pygame.locals import *

class GUI(object):
  def __init__(self, grid, send_message_function):
    self.send_message = send_message_function
    self.grid = grid
    pygame.init()
    self.clock = pygame.time.Clock()
    self.screen = pygame.display.set_mode((640,480))
    self.down_keys = []

  def render(self, data):
    self.screen.fill((255,255,255))
    for sprite in data:
      if sprite["type"] == "player":
        self.draw_player(sprite)
    pygame.display.update()

  def draw_player(self, sprite):
    color = color = (255,0,0)
    pygame.draw.rect(self.screen, color, (sprite["pos"][0], sprite["pos"][1], sprite["dim"][0], sprite["dim"][1]))

  """def draw(self):
    self.screen.fill((255,255,255))
    for y in range(0, len(self.grid)):
      for x in range(0, len(self.grid[0])):
        if self.grid[y][x] == ' ':
          color = (255,255,255)
        else:
          color = (255,0,0)
        dx = 640/len(self.grid[0])
        dy = 480/len(self.grid)   
        pygame.draw.rect(self.screen, color, (dx*x, dy*y, dx, dy))"""

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
