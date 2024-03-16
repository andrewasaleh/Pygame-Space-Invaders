import pygame as pg

class Barrier(pg.sprite.Sprite):
    def __init__(self, game, x, y, max_health=3, scale=0.5):
        super().__init__()
        self.screen = game.screen
        self.max_health = max_health
        self.health = max_health
        self.images = {
            'full': pg.transform.scale(pg.image.load('images/barrier_full.png').convert_alpha(), self._scaled_dimensions('images/barrier_full.png', scale)),
            'medium': pg.transform.scale(pg.image.load('images/barrier_medium.png').convert_alpha(), self._scaled_dimensions('images/barrier_medium.png', scale)),
            'heavy': pg.transform.scale(pg.image.load('images/barrier_heavy.png').convert_alpha(), self._scaled_dimensions('images/barrier_heavy.png', scale)),
            'destroyed': pg.transform.scale(pg.image.load('images/barrier_destroyed.png').convert_alpha(), self._scaled_dimensions('images/barrier_destroyed.png', scale))
        }
        self.state = 'full'
        self.image = self.images[self.state]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _scaled_dimensions(self, image_path, scale):
        """Calculate scaled dimensions of the image based on the scale factor."""
        image = pg.image.load(image_path)
        original_size = image.get_size()
        scaled_size = (int(original_size[0] * scale), int(original_size[1] * scale))
        return scaled_size

    def take_damage(self):
        """Reduce the barrier's health and update its state."""
        self.health -= 1
        if self.health <= 0:
            self.state = 'destroyed'
        elif self.health <= self.max_health // 3:
            self.state = 'heavy'
        elif self.health <= 2 * self.max_health // 3:
            self.state = 'medium'

        # Update the image based on the new state
        self.image = self.images[self.state]

    def draw(self):
        """Draw the barrier on the screen."""
        self.screen.blit(self.image, self.rect)
