import sys, time
import pygame as pg
from settings import Settings 
from ship import Ship
from aliens import Aliens
from vector import Vector
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sound import Sound

class Game:
  key_velocity = {pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1,  0),
                  pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1)}
  
  def __init__(self):
    pg.init()
    self.settings = Settings()
    self.screen = pg.display.set_mode(
      (self.settings.screen_width, self.settings.screen_height))
    pg.display.set_caption("Alien Invasion")

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
    self.game_active = False              # MUST be before Button is created
    self.first = True
    self.play_button = Button(game=self, text='Play')
    self.finished = False 
    # In Game Sounds
    self.sound = Sound()  
    self.explosion_sound = pg.mixer.Sound('sounds/alien_explosion.wav')  # alien explosion sound
    self.level_up_sound = pg.mixer.Sound('sounds/next_level.wav')  # level progression sound
    self.ship_explosion_sound = pg.mixer.Sound('sounds/ship_explosion.wav')  # ship explosion sound
    self.alien_fire_sound = pg.mixer.Sound('sounds/alien_fire.wav')  # alien fire sound

  def schedule_removal(self, alien):
      if alien not in self.to_remove:
          self.to_remove.append(alien)

  def remove_aliens(self):
      # Remove any aliens that have been flagged for removal
      for alien in self.to_remove:
          if alien in self.aliens.alien_group:
              self.aliens.alien_group.remove(alien)
      self.to_remove.clear()

  def draw_volume_level(self):
      font = pg.font.SysFont(None, 24)
      volume_text = font.render(f"Volume: {int(self.sound.volume * 100)}%", True, pg.Color('white'))
      self.screen.blit(volume_text, (10, 10))  # Adjust position as needed

  def check_events(self):
      for event in pg.event.get():
          type = event.type
          if type == pg.KEYUP:
              key = event.key
              if key == pg.K_SPACE:
                  self.ship.cease_fire()
              elif key in Game.key_velocity:
                  self.ship.all_stop()
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
              elif key == pg.K_PAGEUP:  # Increase volume with page up key
                  self.sound.increase_volume()
              elif key == pg.K_PAGEDOWN:  # Decrease volume with page down key
                  self.sound.decrease_volume()
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
    self.settings.initialize_dynamic_settings()                                  

  def game_over(self):
      print('Game Over!')
      pg.mouse.set_visible(True)
      self.play_button.change_text('Play again?')
      self.play_button.show()  # Make sure this method updates the button to be visible
      self.game_active = False
      self.stats.reset()
      self.restart()
      self.sound.play_game_over()

  def activate(self): 
      self.game_active = True
      self.first = False
      self.sound.play_music("sounds/game-music.wav") # Background Music


  def play(self):
      finished = False
      while not finished:
          self.check_events()

          if self.game_active:
              # Main game loop actions
              self.screen.blit(self.bg_image, (0, 0))
              self.ship.update()
              self.aliens.update()
              self.sb.update()
          elif self.first:
              # If it's the first run, display the launch screen instead of playing the game immediately
              self.show_launch_screen()
              self.first = False  # Make sure to set this to False after showing the launch screen
          else:
              # If the game is not active and it's not the first run, update and show the play again button
              self.play_button.update()

          pg.display.flip()
          time.sleep(0.02)
  '''
  Main Game Launch Screen
  '''
  def show_launch_screen(self):
      """Display the launch screen and wait for the player to start the game."""
      self.screen.fill((0, 0, 0))  # Fill the screen with black

      # Display the game title
      title_font = pg.font.Font('font/pixelFont.ttf', 85)
      title_text = title_font.render("Alien Invasion", True, (50, 250, 80))
      title_rect = title_text.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 5))
      self.screen.blit(title_text, title_rect)

      # Display the sound adjustment message
      instructions_font = pg.font.Font('font/pixelFont.ttf', 24)  # Smaller font size than the title
      instructions_text = instructions_font.render("Adjust Sound with PG UP/PG DOWN keys", True, (255, 255, 255))
      instructions_rect = instructions_text.get_rect(center=(self.settings.screen_width / 2, title_rect.bottom + 30))
      self.screen.blit(instructions_text, instructions_rect)

      names = ['rainbow', 'arrow', 'octopus', 'hunter', 'saucer', 'slicer']
      points = [70, 140, 210, 280, 350, 420]
      scale_factor = 0.4  # Change this factor to scale the images by a desired amount

      images = {name: pg.transform.scale(pg.image.load(f'images/aliens/alien_{name}.png'), 
      self._scaled_dimensions(f'images/aliens/alien_{name}.png', scale_factor)) for name in names}
      
      point_font = pg.font.Font('font/pixelFont.ttf', 20)
      start_y = self.settings.screen_height / 2 + 50
      
      # Adjust button positioning
      base_y_adjustment = 300  # Adjust this value to move buttons down
      button_spacing = 60  # Vertical space between buttons

      # Adjust base_y starting point for the "Play" button
      base_y = self.settings.screen_height / 3 + base_y_adjustment

      # "Play" Button
      play_button_font = pg.font.Font('font/pixelFont.ttf', 30)
      play_button_text = play_button_font.render("PLAY GAME", True, (50, 250, 80))
      play_button_rect = play_button_text.get_rect(center=(self.settings.screen_width / 2, base_y))
      self.screen.blit(play_button_text, play_button_rect)

      # "High Scores" Button
      high_scores_button_font = pg.font.Font('font/pixelFont.ttf', 30)
      high_scores_button_text = high_scores_button_font.render("HIGH SCORES", True, (255, 255, 255))
      high_scores_button_rect = high_scores_button_text.get_rect(center=(self.settings.screen_width / 2, base_y + button_spacing))
      self.screen.blit(high_scores_button_text, high_scores_button_rect)

      start_y = self.settings.screen_height / 2.8 # Adjust this value to move the images up or down

      # Assuming a y_spacing to control the space between each row
      y_spacing = 40  # Adjust this value to increase or decrease the space between rows

      # Display each alien image with its corresponding points
      for i, (name, point) in enumerate(zip(names, points)):
          alien_image = images[name]
          # Adjust only the y-coordinate in topleft for vertical positioning
          alien_image_rect = alien_image.get_rect(topleft=(self.settings.screen_width / 2 - 100, start_y + i * y_spacing))
          self.screen.blit(alien_image, alien_image_rect)
          
          # Adjust the position of the point text relative to its alien image
          point_text = point_font.render(f'= {point} POINTS', True, (255, 255, 255))
          point_rect = point_text.get_rect(topleft=(self.settings.screen_width / 2 - 50, start_y + i * y_spacing))
          self.screen.blit(point_text, point_rect)

      pg.display.flip()

      waiting = True
      while waiting:
          for event in pg.event.get():
              if event.type == pg.QUIT:
                  pg.quit()
                  sys.exit()
              elif event.type == pg.MOUSEBUTTONDOWN:
                  mouse_pos = event.pos  # Get the mouse position
                  # Check if "Play" button is clicked
                  if play_button_rect.inflate(20, 10).collidepoint(mouse_pos):
                      waiting = False  # Exit the loop to start the game
                      self.activate()  # Activate the game to start playing
                  elif high_scores_button_rect.inflate(20, 10).collidepoint(mouse_pos):
                      print("High Scores button clicked")
                      self.show_high_scores()
                      # After showing high scores, clear the screen or reset to the launch screen state as needed
                      self.screen.fill((0, 0, 0))  # Optional: Clear the screen again
                      self.show_launch_screen()  # Call launch screen again if you want to return to it


                      # Optionally, clear the screen before the game starts
                      self.screen.fill((0, 0, 0))
                      pg.display.flip()

  """
  Scale aliens size for main screen point display
  """
  def _scaled_dimensions(self, image_path, scale_factor):
      image = pg.image.load(image_path)
      original_size = image.get_size()
      scaled_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
      return scaled_size

if __name__ == '__main__':
    g = Game()
    g.show_launch_screen() 
    g.play()