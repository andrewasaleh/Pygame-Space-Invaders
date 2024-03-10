import pygame as pg
from pygame.sprite import Sprite
from vector import Vector 
# from random import randint
from timer import Timer


class Laser(Sprite):
  def __init__(self, game, v, timer, owner):
    super().__init__()
    self.game = game 
    self.screen = game.screen
    self.settings = game.settings
    self.v = v
    self.timer = timer
    self.owner = owner
    # self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
    # self.color = self.settings.laser_color

    # self.rect = pg.Rect(0, 0, self.settings.laser_width, self.settings.laser_height)
    self.rect = owner.laser_start_rect()
    self.y = float(self.rect.y)

  def update(self):
    self.y += self.v.y
    self.rect.y = self.y

    if self.owner.laser_offscreen(self.rect): self.kill()    # delete off-screen lasers
    self.draw()

  def draw(self): 
    # pg.draw.rect(self.screen, self.color, self.rect)
    image = self.timer.current_image()     # uses timer for animation now
    # rect = image.get_rect()
    self.screen.blit(image, self.rect)


class Lasers():                                # can now have aliens or ship firing
  def __init__(self, game, timer, v, owner):   # one instance for Ship and one for Aliens
    self.game = game
    self.screen = game.screen
    self.settings = game.settings 
    self.timer = timer                         # handles animation
    self.v = v                                 # handles v can be up or down
    self.owner = owner                         # handles which object is shooting the laser
    self.laser_group = pg.sprite.Group()

  def lasergroup(self):  
    return self.laser_group

  def add(self, owner):         
    new_laser = Laser(self.game, v=self.v, timer=self.timer, owner=owner)
    self.laser_group.add(new_laser) 

  def empty(self): 
    self.laser_group.empty()

  def update(self):
    for laser in self.laser_group.sprites():
      laser.update()


if __name__ == '__main__':
  print("\nERROR: lasers.py is the wrong file! Run play from alien_invasions.py\n")

  