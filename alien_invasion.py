import sys, time
import pygame as pg
from settings import Settings 
from ship import Ship
from aliens import Aliens
from vector import Vector
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from barriers import Barrier
from sound import Sound


class Game:
  key_velocity = {pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1,  0),
                  pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1)}
  
  def __init__(self):
    pg.init()
    self.settings = Settings()
    self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
    pg.display.set_caption("Alien Invasion")

    # Load and scale the background image
    self.bg_image = pg.image.load('images/play-background.png').convert()
    self.bg_image = pg.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))

    self.aliens = None
    self.stats = GameStats(game=self)
    self.sound = Sound()
    self.sb = Scoreboard(game=self)

    self.ship = Ship(game=self)
    self.aliens = Aliens(game=self)  
    self.ship.set_aliens(self.aliens)
    self.ship.set_sb(self.sb)

    # self.barriers = Barriers(game=self)
    self.game_active = False              # MUST be before Button is created
    self.first = True
    self.play_button = Button(game=self, text='Play')
    self.barriers = pg.sprite.Group()
    self.create_barriers()
    self.barriers.draw(self.screen)  # Draws all barriers in the group to the screen
    self.finished = False 
    
  def create_barriers(self):
      # Positioning example; adjust as needed
      barrier_positions = [(100, 600), (400, 600), (700, 600), (1000, 600)]
      for pos in barrier_positions:
          barrier = Barrier(self, *pos)
          self.barriers.add(barrier)  # Assuming self.barriers is a pygame.sprite.Group

  def schedule_removal(self, alien):
      if alien not in self.to_remove:
          self.to_remove.append(alien)

  def remove_aliens(self):
      # Remove any aliens that have been flagged for removal
      for alien in self.to_remove:
          if alien in self.aliens.alien_group:
              self.aliens.alien_group.remove(alien)
      self.to_remove.clear()

  def check_events(self):
    for event in pg.event.get():
      type = event.type
      if type == pg.KEYUP: 
        key = event.key 
        if key == pg.K_SPACE: self.ship.cease_fire()
        elif key in Game.key_velocity: self.ship.all_stop()
      elif type == pg.QUIT: 
        pg.quit()
        sys.exit()
      elif type == pg.KEYDOWN:
        key = event.key
        if key == pg.K_SPACE: 
          self.ship.fire_everything()
        elif key == pg.K_p: 
          self.play_button.select(True)
          self.play_button.press()
        elif key in Game.key_velocity: 
          self.ship.add_speed(Game.key_velocity[key])
      elif type == pg.MOUSEBUTTONDOWN:
        b = self.play_button
        x, y = pg.mouse.get_pos()
        if b.rect.collidepoint(x, y):
          b.press()
      elif type == pg.MOUSEMOTION:
        b = self.play_button
        x, y = pg.mouse.get_pos()
        b.select(b.rect.collidepoint(x, y))
    
  def restart(self):
    self.screen.fill(self.settings.bg_color)
    self.ship.reset()
    self.aliens.reset()
    # self.barriers.reset()
    self.settings.initialize_dynamic_settings()                                  

  def game_over(self):
    print('Game Over !')
    pg.mouse.set_visible(True)
    self.play_button.change_text('Play again?')
    self.play_button.show()
    self.first = True
    self.game_active = False
    self.stats.reset()
    self.restart()
    self.sound.play_game_over()

  def activate(self): 
    self.game_active = True
    self.first = False
    self.sound.play_music("sounds/game-music.wav")

  def play(self):
      finished = False
      while not finished:
          self.check_events()

          if self.game_active or self.first:
              self.first = False
              self.screen.blit(self.bg_image, (0, 0))
              self.ship.update()
              self.aliens.update()
              if self.game_active:  # Ensure this is only true when the game is active
                  self.barriers.draw(self.screen)  # Move this inside the conditional
              self.sb.update()
          else:
              self.play_button.update()

          pg.display.flip()
          time.sleep(0.02)

  def show_launch_screen(self):
      """Display the launch screen and wait for the player to start the game."""
      self.screen.fill((0, 0, 0))  # Fill the screen with black

      # Display the game title
      title_font = pg.font.Font('font/pixelFont.ttf', 74)
      title_text = title_font.render("Alien Invasion", True, (255, 255, 255))
      title_rect = title_text.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 3))
      self.screen.blit(title_text, title_rect)

      names = ['Asset 2', 'Asset 3', 'Asset 4', 'Asset 5', 'Asset 6', 'Asset 7']
      points = [40, 10, 60, 100, 150, 200]
      scale_factor = 0.4  # Change this factor to scale the images by a desired amount

      images = {name: pg.transform.scale(pg.image.load(f'images/alien_{name}.png'), self._scaled_dimensions(f'images/alien_{name}.png', scale_factor)) for name in names}
      
      point_font = pg.font.Font('font/pixelFont.ttf', 20)
      start_y = self.settings.screen_height / 2 + 50
      
      # Adjust button positioning
      base_y_adjustment = 280  # Adjust this value to move buttons down
      button_spacing = 60  # Vertical space between buttons

      # Adjust base_y starting point for the "Play" button
      base_y = self.settings.screen_height / 2 + base_y_adjustment

      # "Play" Button
      play_button_font = pg.font.Font('font/pixelFont.ttf', 36)
      play_button_text = play_button_font.render("Play", True, (255, 255, 255))
      play_button_rect = play_button_text.get_rect(center=(self.settings.screen_width / 2, base_y))
      pg.draw.rect(self.screen, (0, 128, 0), play_button_rect.inflate(20, 10))  # Button background
      self.screen.blit(play_button_text, play_button_rect)

      # "High Scores" Button
      high_scores_button_font = pg.font.Font('font/pixelFont.ttf', 36)
      high_scores_button_text = high_scores_button_font.render("High Scores", True, (255, 255, 255))
      high_scores_button_rect = high_scores_button_text.get_rect(center=(self.settings.screen_width / 2, base_y + button_spacing))
      pg.draw.rect(self.screen, (128, 0, 0), high_scores_button_rect.inflate(20, 10))  # Button background
      self.screen.blit(high_scores_button_text, high_scores_button_rect)

      # Display each alien image with its corresponding points
      for i, (name, point) in enumerate(zip(names, points)):
          alien_image = images[name]
          alien_image_rect = alien_image.get_rect(topleft=(self.settings.screen_width / 2 - 100, start_y + i * 30))
          self.screen.blit(alien_image, alien_image_rect)
          
          point_text = point_font.render(f'= {point} POINTS', True, (255, 255, 255))
          point_rect = point_text.get_rect(topleft=(self.settings.screen_width / 2 - 50, start_y + i * 30))
          self.screen.blit(point_text, point_rect)

      pg.display.flip()

      # Wait for the player to interact with the buttons
      waiting = True
      while waiting:
          for event in pg.event.get():
              if event.type == pg.QUIT:
                  pg.quit()
                  sys.exit()
              elif event.type == pg.MOUSEBUTTONDOWN:
                  mouse_pos = event.pos  # Get the mouse position
                  if play_button_rect.inflate(20, 10).collidepoint(mouse_pos):
                      waiting = False  # Begin the game
                  elif high_scores_button_rect.inflate(20, 10).collidepoint(mouse_pos):
                      print("High Scores button clicked")
                      # For example, call a method self.show_high_scores()

      self.screen.fill((0, 0, 0))  # Optional: Clear the screen again before game starts

  def _scaled_dimensions(self, image_path, scale_factor):
      """Calculate scaled dimensions of the image based on the scale factor."""
      image = pg.image.load(image_path)
      original_size = image.get_size()
      scaled_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
      return scaled_size

if __name__ == '__main__':
    g = Game()
    g.show_launch_screen()  # Show the launch screen before starting the game
    g.play()