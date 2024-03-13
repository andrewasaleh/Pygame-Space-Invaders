import pygame as pg
import sys
from pygame.sprite import Sprite
from vector import Vector 
from random import randint
from lasers import Lasers
from timer import Timer


class Alien(Sprite):
  names = ['Asset 2', 'Asset 3', 'Asset 4', 'Asset 5', 'Asset 6', 'Asset 7']
  points = [40, 10, 60, 100, 150, 200]
  images = [pg.image.load(f'images/alien_{name}.png') for name in names] 
  # nameslen = len(names)
  # choices = [randint(0, nameslen) for _ in range(nameslen)]

  li = [x * x for x in range(1, 11)]

  def __init__(self, game, row, alien_no):
    super().__init__()
    self.game = game 
    self.screen = game.screen
    self.screen_rect = self.screen.get_rect()
    self.settings = game.settings
    
    # Set the image based on the row number for specific alien type per row
    alien_index = row % len(Alien.images)
    self.image = Alien.images[alien_index]

    # Initialize rect and other attributes
    self.rect = self.image.get_rect()

    # Initial position setup remains unchanged
    self.rect.x = self.rect.width
    self.rect.y = self.rect.height 
    self.x = float(self.rect.x)
    self.timer = Timer(Alien.images, start_index=randint(0, len(Alien.images) - 1), delta=20)

    
  def laser_offscreen(self, rect): return rect.bottom > self.screen_rect.bottom  

  def laser_start_rect(self):
    rect = self.rect
    rect.midbottom = self.rect.midbottom
    return rect.copy()

  def fire(self, lasers):
    # print(f'Alien {self.alien_no} firing laser')
    lasers.add(owner=self)

  def check_edges(self):
    r = self.rect 
    sr = self.screen_rect
    return r.right >= sr.right or r.left < 0
  
  def check_bottom(self): return self.rect.bottom >= self.screen_rect.bottom 
  
  def update(self, v, delta_y):
    self.x += v.x
    self.rect.x = self.x
    self.rect.y += delta_y
    self.draw()

  def draw(self): 
      if self.timer is not None:
          self.image = self.timer.current_image()
      self.screen.blit(self.image, self.rect)


class Aliens():
  laser_image_files = [f'images/alien_laser_0{x}.png' for x in range(2)]
  laser_images = [pg.transform.scale(pg.image.load(x), (50, 50)) for x in laser_image_files]

  def __init__(self, game):
    self.game = game
    self.screen = game.screen
    self.settings = game.settings 
    self.stats = game.stats
    self.sb = game.sb
    self.aliens_created = 0
    self.v = Vector(self.settings.alien_speed, 0)
    self.laser_timer = Timer(image_list=Aliens.laser_images, delta=10)
    self.lasers = Lasers(game=game, v=Vector(0, 1) * self.settings.laser_speed, 
                         timer=self.laser_timer, owner=self)

    self.alien_group = pg.sprite.Group()
    self.ship = game.ship
    self.alien_firing_now = 0
    self.fire_every_counter = 0
    self.create_fleet()

  def create_alien(self, alien_number, row_number, alien_width, alien_height):
      # Create an alien and place it in the row.
      alien = Alien(self.game, row=row_number, alien_no=alien_number)
      alien.x = alien_width + 2 * alien_width * alien_number
      alien.rect.x = alien.x
      alien.rect.y = alien_height + 2 * alien_height * row_number
      self.alien_group.add(alien)
      
  def empty(self): self.alien_group.empty()

  def reset(self):
    self.alien_group.empty()
    self.lasers.empty()
    self.create_fleet() 
  
  def create_fleet(self):
      # Create a sample alien to get its size for calculations
      alien = Alien(self.game, row=0, alien_no=-1)
      alien_width, alien_height = alien.rect.size

      # Calculate the number of aliens that fit in a row
      available_space_x = self.settings.screen_width - (2 * alien_width)
      number_aliens_x = available_space_x // (2 * alien_width)

      # Calculate the number of rows of aliens that fit on the screen
      available_space_y = (self.settings.screen_height - (3 * alien_height) - self.ship.rect.height)
      number_rows = available_space_y // (2 * alien_height)

      # Create the fleet of aliens, now with each row having a specific alien type
      for row_number in range(number_rows):
          for alien_number in range(number_aliens_x):
              self.create_alien(alien_number, row_number, alien_width, alien_height)

  def check_edges(self):
    for alien in self.alien_group.sprites():
      if alien.check_edges(): return True
    return False

  def check_bottom(self):
    for alien in self.alien_group.sprites():
      if alien.check_bottom(): return True
    return False
  
  def update(self):
    delta_y = 0
    if self.check_edges():
      delta_y = self.settings.fleet_drop
      self.v.x *= -1
      
    if self.check_bottom(): self.ship.hit()
    
    # ship lasers taking out aliens
    collisions = pg.sprite.groupcollide(self.ship.lasers.lasergroup(), self.alien_group, True, True)
    if len(collisions) > 0: 
        for aliens in collisions.values():
            for alien in aliens:
                self.game.sound.play_explosion()  # Play explosion sound for each alien hit
                # Add score based on alien's point value
                index = alien.timer.current_index()
                points = Alien.points[index]
                self.stats.score += points
        
        self.sb.prep_score()
        self.sb.check_high_score()

    # laser-laser collisions
    collisions = pg.sprite.groupcollide(self.ship.lasers.lasergroup(), self.lasers.lasergroup(), 
                                        True, True)

    for alien in self.alien_group.sprites():
      alien.update(self.v, delta_y)

    # must have aliens to fire at the ship
    if self.alien_group and self.fire_every_counter % self.settings.aliens_fireevery == 0:
      n = randint(0, len(self.alien_group) - 1)
      self.alien_group.sprites()[n].fire(lasers=self.lasers)
    self.fire_every_counter += 1

    # update the positions of all of the aliens' lasers (the ship updates its own lasers)
    self.lasers.update()

    # no more aliens -- time to re-create the fleet
    if not self.alien_group:
      self.lasers.empty()
      self.create_fleet()
      self.settings.increase_speed()
      self.stats.level += 1
      self.sb.prep_level()

    # aliens hitting the ship
    if pg.sprite.spritecollideany(self.ship, self.alien_group):
      self.ship.hit()

    # alien lasers taking out the ship
    if pg.sprite.spritecollideany(self.ship, self.lasers.lasergroup()):
      self.ship.hit()


if __name__ == '__main__':
  print("\nERROR: aliens.py is the wrong file! Run play from alien_invasions.py\n")
