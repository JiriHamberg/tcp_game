import threading

class ObjectStore(object):
  def __init__(self):
    self.sprite_map = {}
    self.lock = threading.RLock()

  def all(self):
    with self.lock:
      return [sprite for sprite in map(lambda key: self.sprite_map[key], self.sprite_map)]

  def add(self, sprite):
    #assert(sprite["sprite_id"] not in self.sprite_map)
    with self.lock:
      #if sprite["sprite_id"] in self.sprite_map:
      #  return
      self.sprite_map[sprite["sprite_id"]] = sprite  

  def update(self, sprite):
    #assert(sprite["sprite_id"] in self.sprite_map)
    with self.lock:
      #if sprite["sprite_id"] not in self.sprite_map:
      #  return
      self.add(sprite)

  def remove(self, sprite):
    with self.lock:
      del self.sprite_map[sprite["sprite_id"]]