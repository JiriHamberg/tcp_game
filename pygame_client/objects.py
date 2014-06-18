import threading

class ObjectStore(object):
  def __init__(self):
    self.sprite_map = {}
    self.lock = threading.RLock()
    self.events = {"add": {}, "update": {}, "remove": {}}

  def bind_event(self, event_type, sprite_type, event_callback):    
    event_map = self.events[event_type]
    event_map[sprite_type] = event_callback

  def all(self):
    with self.lock:
      return [sprite for sprite in map(lambda key: self.sprite_map[key], self.sprite_map)]

  def add(self, sprite):
    event_map = self.events["add"]
    #assert(sprite["sprite_id"] not in self.sprite_map)
    with self.lock:
      #if sprite["sprite_id"] in self.sprite_map:
      #  return
      self.sprite_map[sprite["sprite_id"]] = sprite
      if sprite["type"] in event_map:
        event_map[sprite["type"]](sprite)

  def update(self, sprite):
    event_map = self.events["update"]
    #assert(sprite["sprite_id"] in self.sprite_map)
    with self.lock:
      #if sprite["sprite_id"] not in self.sprite_map:
      #  return
      self.add(sprite)
      if sprite["type"] in event_map:
        event_map[sprite["type"]](sprite)

  def remove(self, sprite):
    event_map = self.events["remove"]
    with self.lock:
      del self.sprite_map[sprite["sprite_id"]]
      if sprite["type"] in event_map:
        event_map[sprite["type"]](sprite)