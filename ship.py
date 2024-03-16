import time
import pygame as pg
from pygame.sprite import Sprite
from lasers import Lasers
from timer import Timer
from vector import Vector 
from time import sleep
from random import randint


class Ship(Sprite):
  laser_image_files = [f'images/ship_laser_0{x}.png' for x in range(2)]
  laser_images = [pg.image.load(x) for x in laser_image_files]

  def __init__(self, game, v=Vector()):
    super().__init__()
    self.game = game 
    self.v = v
    self.settings = game.settings
    self.stats = game.stats
    self.laser_timer = Timer(image_list=Ship.laser_images, delta=20)
    self.lasers = Lasers(game=game, v=Vector(0, -1) * self.settings.laser_speed, 
                         timer=self.laser_timer, owner=self)
    self.aliens = game.aliens
    self.sound = game.sound
    self.continuous_fire = False
    self.screen = game.screen 
    self.screen_rect = game.screen.get_rect() 

    self.image = pg.image.load('images/ship.png')
    self.rect = self.image.get_rect()

    self.rect.midbottom = self.screen_rect.midbottom 
    self.fire_counter = 0
    
    # Load explosion images into a list for the animation
    self.explosion_images = [pg.image.load(f'images/ship_explosion_0{x}.png') for x in range(1,8)]
    self.explosion_index = 0  # To keep track of the current explosion frame
    self.is_exploding = False  # Control flag for explosion state

    # Add an explosion counter and set the speed
    self.explosion_counter = 0
    self.explosion_speed = 10  # Increase this value to slow down the animation

  def set_aliens(self, aliens): self.aliens = aliens

  # def set_lasers(self, lasers): self.lasers = lasers

  def set_sb(self, sb): self.sb = sb

  def clamp(self):
    r, srect = self.rect, self.screen_rect   # read-only alias 
    # cannot use alias for writing, Python will make a copy
    #     and will change the copy instead

    if r.left < 0: self.rect.left = 0
    if r.right > srect.right: self.rect.right = srect.right 
    if r.top < 0: self.rect.top = 0
    if r.bottom > srect.bottom: self.rect.bottom = srect.bottom
      
  def set_speed(self, speed): self.v = speed

  def add_speed(self, speed): self.v += speed

  def all_stop(self): self.v = Vector()
  
  def fire_everything(self): self.continuous_fire = True

  def cease_fire(self): self.continuous_fire = False

  def fire(self): 
      timer = Timer(Ship.laser_images, start_index=randint(0, len(Ship.laser_images) - 1), delta=10)
      self.lasers.add(owner=self, timer=timer)
      # Use the sound object from the game instance to play the phaser sound
      self.game.sound.play_phaser()

  def hit(self):
      print('Abandon ship! Ship has been hit!')
      # Use the sound object from the game instance to play the ship explosion sound
      self.game.sound.play_ship_explosion()
      self.is_exploding = True
      self.explosion_index = 0  # Reset explosion animation
      time.sleep(0.2)
      self.stats.ships_left -= 1
      self.sb.prep_ships()
      if self.stats.ships_left <= 0:
          self.game.game_over()
      else:
          self.game.restart()

  def laser_offscreen(self, rect): return rect.bottom < 0

  def laser_start_rect(self):
    rect = self.rect
    rect.midtop = self.rect.midtop
    return rect.copy()
  
  def center_ship(self): 
    self.rect.midbottom = self.screen_rect.midbottom 
    self.x = float(self.rect.x)

  def reset(self):
    self.lasers.empty()
    self.center_ship()

  def update(self):
      if self.is_exploding:
          # Update the image to the next frame of the explosion
          self.image = self.explosion_images[self.explosion_index]
          self.explosion_index += 1
          if self.explosion_index >= len(self.explosion_images):
              # Explosion animation finished
              self.is_exploding = False
              if self.stats.ships_left <= 0:
                  self.game.game_over()
              else:
                  self.game.restart()
                  # Reset ship image to default after explosion
                  self.image = pg.image.load('images/ship.png')
      else:
          self.rect.left += self.v.x * self.settings.ship_speed
          self.rect.top += self.v.y * self.settings.ship_speed
          self.clamp()
          if self.continuous_fire and self.fire_counter % 3 == 0:
              self.fire()
          self.fire_counter += 1
          self.lasers.update()

      self.draw()

  def draw(self):
    self.screen.blit(self.image, self.rect)


if __name__ == '__main__':
  print("\nERROR: ship.py is the wrong file! Run play from alien_invasions.py\n")

  