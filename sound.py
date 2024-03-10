import pygame as pg
from pygame import mixer 
import time


class Sound:
    def __init__(self):
        mixer.init() 
        self.volume = 0.1  
        self.phaser_sound = mixer.Sound("sounds/laser-sound.wav")
        self.explosion_sound = mixer.Sound("sounds/explosion-sound.wav")  
        self.set_volume(self.volume)  

    def set_volume(self, volume=0.3):
        mixer.music.set_volume(volume) 
        self.phaser_sound.set_volume(3 * volume)
        self.explosion_sound.set_volume(3 * volume)  

    def play_music(self, filename): 
        self.stop_music()
        mixer.music.load(filename) 
        mixer.music.play(loops=-1) 
 
    def pause_music(self): 
        mixer.music.pause()

    def unpause_music(self):
        mixer.music.unpause()      

    def stop_music(self): 
        mixer.music.stop() 
 
    def play_phaser(self): 
        mixer.Sound.play(self.phaser_sound) 

    def play_game_over(self):
        self.play_music("sounds/game-over.wav")
        time.sleep(2.5)
        self.stop_music()

    def play_explosion(self):
        self.explosion_sound.play()