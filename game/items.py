import random

class Items(object):

  @staticmethod
  def callbacks():
    return {"bomb_power": Items.bomb_power_callback,
            "bomb_speed": Items.bomb_speed_callback }

  @staticmethod
  def random_item():
    "Returns new random item"
    return random.choice(Items.callbacks().keys())

  @staticmethod
  def should_spawn():
    return random.random() < 1.0 / 7.0

  @staticmethod
  def collision_callback(player_sprite, item_type):
    "Generic item collision logic"
    Items.callbacks()[item_type](player_sprite.player)

  @staticmethod
  def bomb_power_callback(player):
    player.bomb_power += 1

  @staticmethod
  def bomb_speed_callback(player):
    player.bomb_cooldown = max(5, player.bomb_cooldown - 5)