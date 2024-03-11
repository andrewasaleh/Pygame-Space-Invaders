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
    
  # In your Game class
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
      self.screen.blit(self.bg_image, (0, 0))
      
      while not finished:
        self.check_events()    # exits if Cmd-Q on macOS or Ctrl-Q on other OS

        if self.game_active or self.first:
          self.first = False
          self.screen.blit(self.bg_image, (0, 0))
          self.ship.update()
          self.aliens.update()   # when we have aliens
          # self.barriers.update()
          self.barriers.draw(self.screen)
          self.sb.update()
        else:
          self.play_button.update()  
        
        pg.display.flip()
        time.sleep(0.02)


  def show_launch_screen(self):
      """Display the launch screen and wait for the player to start the game."""
      # Load background image
      background_image = pg.image.load('images/background.png').convert()
      # Resize background to fit the screen, if necessary
      background_image = pg.transform.scale(background_image, (self.settings.screen_width, self.settings.screen_height))

      # Blit the background image
      self.screen.blit(background_image, (0, 0))

      # Display the game title
      title_font = pg.font.Font('font/pixelFont.ttf', 74)  # Use Pygame's default font
      title_text = title_font.render("Alien Invasion", True, (255, 255, 255))
      title_rect = title_text.get_rect()
      title_rect.center = (self.settings.screen_width / 2, self.settings.screen_height / 3)
      self.screen.blit(title_text, title_rect)

      # Display the prompt to start the game
      prompt_font = pg.font.Font('font/pixelFont.ttf', 36)
      prompt_text = prompt_font.render("Press 'Space' to play", True, (255, 255, 255))
      prompt_rect = prompt_text.get_rect()
      prompt_rect.center = (self.settings.screen_width / 2, self.settings.screen_height / 2)
      self.screen.blit(prompt_text, prompt_rect)

      pg.display.flip()  # Update the display to show the launch screen

      # Wait for the player to press 'Space' to start the game
      waiting = True
      while waiting:
          for event in pg.event.get():
              if event.type == pg.QUIT:
                  pg.quit()
                  sys.exit()
              elif event.type == pg.KEYDOWN:
                  if event.key == pg.K_SPACE:
                      waiting = False

if __name__ == '__main__':
    g = Game()
    g.show_launch_screen()  # Show the launch screen before starting the game
    g.play()