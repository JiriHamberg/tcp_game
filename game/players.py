

class Player(object):
  def __init__(self, color):
    self.color = color
    self.sprite = None
    self.velocity = 2.0
    self.bomb_power = 3
    self.bomb_cooldown = 50
    self.last_bomb = 50

  def update(self):
    self.last_bomb += 1

  def on_drop_bomb(self):
    self.last_bomb = 0

  def can_drop_bomb(self):
    return self.last_bomb > self.bomb_cooldown