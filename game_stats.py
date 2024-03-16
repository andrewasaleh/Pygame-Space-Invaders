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

    def show_high_scores(self):
        # Fill the screen with a background color or an image
        self.screen.fill((0, 0, 0))
        # Display high scores
        high_scores_font = pg.font.Font('font/pixelFont.ttf', 36)
        # Assume high scores are stored in a list or read from a file
        high_scores = self.stats.get_high_scores()  # Placeholder for actual high score retrieval method
        for index, score in enumerate(high_scores):
            score_text = high_scores_font.render(f"{index + 1}. {score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(self.settings.screen_width / 2, 100 + 40 * index))
            self.screen.blit(score_text, score_rect)
        pg.display.flip()
        # Wait for a key press to return to the launch screen or another state
        waiting_for_key = True
        while waiting_for_key:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    waiting_for_key = False
        # Save high score before returning
        self.save_high_score()
