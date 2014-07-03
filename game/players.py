

class Player(object):
  def __init__(self, color):
    self.bomb_command = False
    self.move_command = None
    self.color = color
    self.sprite = None
    self.lifes = 3
    self.velocity = 4
    self.bomb_power = 3
    self.bomb_cooldown = 15
    self.last_bomb = 50

  def update(self):
    self.last_bomb += 1

  def on_drop_bomb(self):
    self.last_bomb = 0

  def can_drop_bomb(self):
    return self.last_bomb > self.bomb_cooldown