import pygame
import os
import random

PATH = os.path.dirname( os.path.realpath( __file__ ) )

class SoundEffects(object):
  @staticmethod
  def init():
    SoundEffects.bg_music = {}
    SoundEffects.background = pygame.mixer.Channel(1)
    pygame.mixer.set_reserved(1)
    SoundEffects.load_sound_effects()

  @staticmethod
  def load_sound_effects():
    SoundEffects.explosion = pygame.mixer.Sound(os.path.join(PATH, "sound_effects/atari_boom.wav"))
    SoundEffects.blings = []
    for i in range(1, 11):
      SoundEffects.blings.append(pygame.mixer.Sound(os.path.join(PATH, "sound_effects/coin%d.wav" % (i))))
    SoundEffects.bg_music["dreamtest"] = pygame.mixer.Sound(os.path.join(PATH, "sound_effects/Dreamtest.ogg"))

  @staticmethod
  def play_random_bling():
    random.choice(SoundEffects.blings).play()

  @staticmethod
  def play_background(song):
    song = SoundEffects.bg_music[song]
    song.set_volume(0.2)
    SoundEffects.background.play(song, loops=100)