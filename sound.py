import pygame as pg
from pygame import mixer
import time

class Sound:
    def __init__(self):
        mixer.init()
        self.volume = 0.1
        self.phaser_sound = mixer.Sound("sounds/laser-sound.wav")  # Phaser/laser sound
        self.explosion_sound = mixer.Sound("sounds/alien_explosion.wav")  # Alien explosion sound
        self.ship_explosion_sound = mixer.Sound("sounds/ship_explosion.wav")  # Ship explosion sound
        self.alien_fire_sound = mixer.Sound("sounds/alien_fire.wav")  # Alien fire sound
        self.level_up_sound = mixer.Sound("sounds/next_level.wav")  # Level progression sound
        self.laser_collision_sound = mixer.Sound("sounds/laser_collision.wav")  # laser collision sound
        self.set_volume(self.volume)
        
    def set_volume(self, volume=0.3):
        # Sets volume for music and sound effects
        mixer.music.set_volume(volume)
        self.phaser_sound.set_volume(3 * volume)
        self.explosion_sound.set_volume(3 * volume)
        self.ship_explosion_sound.set_volume(3 * volume)
        self.alien_fire_sound.set_volume(3 * volume)
        self.level_up_sound.set_volume(3 * volume)
        self.laser_collision_sound.set_volume(3*volume)

    def play_music(self, filename):
        # Play background music
        self.stop_music()
        mixer.music.load(filename)
        mixer.music.play(loops=-1)

    def pause_music(self):
        # Pause the music
        mixer.music.pause()

    def unpause_music(self):
        # Unpause the music
        mixer.music.unpause()

    def stop_music(self):
        # Stop the music
        mixer.music.stop()

    def play_phaser(self):
        # Play phaser/laser sound effect
        self.phaser_sound.play()

    def play_explosion(self):
        # Play explosion sound effect
        self.explosion_sound.play()

    def play_level_up(self):
        # Play level up sound effect
        self.level_up_sound.play()

    def play_ship_explosion(self):
        # Play ship explosion sound effect
        self.ship_explosion_sound.play()

    def play_alien_fire(self):
        # Play alien fire sound effect
        self.alien_fire_sound.play()

    def play_laser_collision(self):
        # Play laser collision sound effect
        self.laser_collision_sound.play()  

    def play_game_over(self):
        # Special method to play game over sound and ensure it's not cut off
        self.play_music("sounds/game-over.wav")
        time.sleep(2.5)  # Ensure the game over sound has time to play before stopping
        self.stop_music()
