

class Player(object):
  def __init__(self, color):
    self.color = color
    self.sprite = None
    self.velocity = 2.0
    self.bomb_power = 3