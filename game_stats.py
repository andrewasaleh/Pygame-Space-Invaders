class GameStats:
  def __init__(self, game):
    self.game = game 
    self.settings = game.settings
    self.ships_left = 0
    self.reset()
    self.high_score = 0

  def reset(self):
    self.ships_left = self.settings.ship_limit
    self.score = 0
    self.level = 1
