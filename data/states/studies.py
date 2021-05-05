__author__ = 'justinarmstrong'

import pygame as pg
from data import setup, tools
from data import constants as c
from .. components import info, mario
import sys

class Uni(tools._State):
    def __init__(self):
        """Initializes the state"""
        tools._State.__init__(self)


    def startup(self, current_time, persist):
        """Called every time the game's state becomes this one.  Initializes
        certain values"""
        self.next = c.LOAD_SCREEN
        self.persist = persist
        self.game_info = persist

        self.no_sound = pg.mixer.Sound('resources/sound/no.wav')

        self.setup_background()
        self.setup_cursor()
        #self.keys = pg.key.get_pressed()


    def setup_cursor(self):
        """Creates the mushroom cursor to select 1 or 2 player game"""
        self.cursor = pg.sprite.Sprite()
        self.cursor.image = pg.transform.scale2x(
            pg.image.load('resources/graphics/julian-downflap.png').convert_alpha())
        self.cursor.rect = self.cursor.image.get_rect(center=(100, 512))

        self.cursor.rect.x = 180
        self.cursor.rect.y = 270
        self.cursor.state = c.MED

    def setup_background(self):
        """Setup the background image to blit"""
        self.background = pg.image.load('resources/graphics/uni.png')


    def event_loop(self):
        self.keys = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.keys.append(event.key)
                #self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
            self.get_event(event)



    def update(self, surface, current_time):
        """Updates the state every refresh"""
        self.current_time = current_time
        self.game_info[c.CURRENT_TIME] = self.current_time
        self.update_cursor()

        surface.fill(c.SKY_BLUE)
        surface.blit(self.background,(0,0))
        surface.blit(self.cursor.image, self.cursor.rect)



    def update_cursor(self):
        """Update the position of the cursor"""
        input_list = [pg.K_RETURN, pg.K_a, pg.K_s]
        if self.cursor.state == c.MED:
            self.cursor.rect.x = 180
            self.cursor.rect.y = 270
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.ARC
            for input in input_list:
                if input in self.keys:
                    self.reset_game_info()
                    self.next = c.VICTORY
                    self.done = True
        elif self.cursor.state == c.ARC:
            self.cursor.rect.x = 580
            self.cursor.rect.y = 270
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.MED
            for input in input_list:
                if input in self.keys:
                    print("ERROR")
                    if self.no_sound.get_num_channels() < 1:
                        self.no_sound.play()


    def reset_game_info(self):
        """Resets the game info in case of a Game Over and restart"""
        self.game_info[c.COIN_TOTAL] = 0
        self.game_info[c.SCORE] = 0
        self.game_info[c.LIVES] = 3
        self.game_info[c.CURRENT_TIME] = 0.0
        self.game_info[c.LEVEL_STATE] = None

        self.persist = self.game_info
















