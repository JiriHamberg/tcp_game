import pygame
 
class SpriteSheet(object):
  def __init__(self, filename):
    try:
      self.sheet = pygame.image.load(filename).convert()
    except pygame.error, message:
      print 'Unable to load spritesheet image:', filename
      raise SystemExit, message
  # Load a specific image from a specific rectangle

  def image_at(self, rectangle, colorkey = None, flip = False):
    "Loads image from x,y,x+offset,y+offset"
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size).convert()
    image.blit(self.sheet, (0, 0), rect)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    if flip:
      image = pygame.transform.flip(image, True, False)
    return image
  # Load a whole bunch of images and return them as a list
  def images_at(self, rects, colorkey = None, flip = False):
    "Loads multiple images, supply a list of coordinates" 
    return [self.image_at(rect, colorkey, flip) for rect in rects]
  # Load a whole strip of images
  def load_strip(self, rect, image_count, colorkey = None):
    "Loads a strip of images and returns them as a list"
    tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
            for x in range(image_count)]
    return self.images_at(tups, colorkey)

class SpriteMapper(object):
  def __init__(self, w, h, image_path):
    self.sheet = SpriteSheet(image_path)
    self.w = w
    self.h = h

  def sprite_at(self, x, y, colorkey = None, flip=False):
    left = self.w*(x - 1)
    up = self.h*(y - 1)
    return self.sheet.image_at((left, up, self.w, self.h), colorkey=colorkey, flip=flip)

  def sprites_at(self, points, colorkey = None, flip=False):
    return [ self.sprite_at(point[0], point[1], colorkey=colorkey, flip=flip) for point in points ]

class PlayerSpriteMapper(SpriteMapper):
  IMAGE_PATH = "/home/jiri/Projects/Python/Bomber/client/sprites/Panda.png"
  def __init__(self):
    SpriteMapper.__init__(self, 32, 32, PlayerSpriteMapper.IMAGE_PATH)

  def get_animation(self, direction, idle=True):
    if direction == "up":
      if idle:
        return self.sprites_at([(1,3)])
      else:
        return self.sprites_at([(1,3), (2,3), (3,3)])
    elif direction == "down":
      if idle:
        return self.sprites_at([(1,1), (2,1)])
      else:
        return self.sprites_at([(1,2), (2,2), (3,2)])
    elif direction == "right":
      if idle:
        return self.sprites_at([(1,5), (2,5)])
      else:
        return self.sprites_at([(1,4), (2,4), (3,4)])
    elif direction == "left":
      if idle:
        return self.sprites_at([(1,5), (2,5)], flip=True)
      else:
        return self.sprites_at([(1,4), (2,4), (3,4)], flip=True)
    else:
      raise Exception("Invalid direction: %s" % (direction))

class BrickSpriteMapper(SpriteMapper):
  IMAGE_PATH = "/home/jiri/Projects/Python/Bomber/client/sprites/tiles.png"
  def __init__(self):
    SpriteMapper.__init__(self, 32, 32, BrickSpriteMapper.IMAGE_PATH)

class BombSpriteMapper(SpriteMapper):
  IMAGE_PATH = "/home/jiri/Projects/Python/Bomber/client/sprites/BombExploding.png"
  
  def __init__(self):
    SpriteMapper.__init__(self, 32, 64, BombSpriteMapper.IMAGE_PATH)
    
  def bomb_animation(self):
    return self.sprites_at([(i, 1) for i in range(1, 8)], colorkey=(255, 255, 255))

  def explosion_animation(self):
    return self.sprites_at([(i, 1) for i in range(8, 15)])