class GameStats:
    def __init__(self, game):
        self.settings = game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = self.load_high_score()  # Load high score from file

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open('high_score.txt', 'w') as f:
            f.write(str(self.high_score))

    def reset(self):
        """A convenience method that calls reset_stats."""
        self.reset_stats()