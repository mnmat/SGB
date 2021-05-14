__author__ = 'justinarmstrong'

from data import setup, tools
from data import constants as c
from .. import game_sound
from ..components import info
import subprocess
import pygame as pg
import sys
import os

class LoadScreen(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def startup(self, current_time, persist):
        self.start_time = current_time
        self.persist = persist
        self.game_info = self.persist
        self.next = self.set_next_state()
        self.descriptor = False
        info_state = self.set_overhead_info_state()

        self.overhead_info = info.OverheadInfo(self.game_info, info_state)
        self.sound_manager = game_sound.Sound(self.overhead_info)
        self.set_title()

        if self.next == c.BIRTH:
            self.description = pg.image.load('resources/graphics/level_1_descriptor.png').convert_alpha()
            self.bg_x1 = 90
            self.bg_y1 = 190
        if self.next == c.FLAPPY:
            self.description = pg.image.load('resources/graphics/level_2_descriptor.png').convert_alpha()
            self.bg_x1 = 100
            self.bg_y1 = 150
        if self.next == c.UNI:
            self.bg_x1 = 30
            self.bg_y1 = 150
            self.description = pg.image.load('resources/graphics/level_3_descriptor.png').convert_alpha()
        if self.next == c.DK:
            self.bg_x1 = 40
            self.bg_y1 = 120
            self.description = pg.image.load('resources/graphics/level_4_descriptor.png').convert_alpha()
        if self.next == c.GABON:
            self.bg_x1 = 60
            self.bg_y1 = 140
            self.description = pg.image.load('resources/graphics/level_5_descriptor.png').convert_alpha()
        if self.next == c.LEVEL1:
            self.bg_x1 = 20
            self.bg_y1 = 140
            self.description = pg.image.load('resources/graphics/level_6_descriptor.png').convert_alpha()
        if self.next == c.CAKE:
            self.bg_x1 = 100
            self.bg_y1 = 170
            self.description = pg.image.load('resources/graphics/level_7_descriptor.png').convert_alpha()

    def set_next_state(self):
        """Sets the next state"""
        return self.game_info[c.SELECT]

    def set_overhead_info_state(self):
        """sets the state to send to the overhead info object"""
        return c.LOAD_SCREEN


    def update(self, surface, current_time):
        """Updates the loading screen"""
        self.game_info[c.CURRENT_TIME] = self.current_time = current_time
        self.handle_states()
        self.blit_everything(surface)

    def set_title(self):
        self.title_label = []
        if self.game_info[c.SELECT] == c.BIRTH:
            self.overhead_info.create_label(self.title_label, 'LEVEL 1   - BIRTH', 200, 300)
            self.label_list = [self.title_label]
        if self.game_info[c.SELECT] == c.FLAPPY:
            self.overhead_info.create_label(self.title_label, 'LEVEL 2   - SCHOOL', 195, 300)
            self.label_list = [self.title_label]
        if self.game_info[c.SELECT] == c.UNI:
            self.overhead_info.create_label(self.title_label, 'LEVEL 3   - UNIVERSITY', 145, 300)
            self.label_list = [self.title_label]
        if self.game_info[c.SELECT] == c.DK:
            self.overhead_info.create_label(self.title_label, 'LEVEL 4   - PFEILHEIM', 155, 300)
            self.label_list = [self.title_label]
        if self.game_info[c.SELECT] == c.GABON:
            self.overhead_info.create_label(self.title_label, 'LEVEL 5   - GABON', 195, 300)
            self.label_list = [self.title_label]
        if self.game_info[c.SELECT] == c.LEVEL1:
            self.overhead_info.create_label(self.title_label, 'LEVEL 6   - LONDON', 190, 300)
            self.label_list = [self.title_label]
        if self.game_info[c.SELECT] == c.CAKE:
            self.overhead_info.create_label(self.title_label, 'LEVEL 7   - CAKE', 200, 300)
            self.label_list = [self.title_label]

    def handle_states(self):
        if self.game_info[c.CURRENT_TIME] - self.start_time < 2600:
            self.descriptor = False
        else:
            self.descriptor = True
            if pg.K_RETURN in self.keys:
                self.done = True

    def blit_everything(self,surface):
        surface.fill(c.BLACK)
        self.overhead_info.draw_level_screen_info(surface)
        if not self.descriptor:
            for label in self.label_list:
                for letter in label:
                    surface.blit(letter.image, letter.rect)
        else:
            surface.blit(self.description,(self.bg_x1, self.bg_y1))


    def event_loop(self):
        self.keys = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.keys.append(event.key)
                self.toggle_show_fps(event.key)
            self.get_event(event)


class GameOver(LoadScreen):
    """A loading screen with Game Over"""
    def __init__(self):
        super(GameOver, self).__init__()


    def set_next_state(self):
        """Sets next state"""
        return c.MAIN_MENU

    def set_overhead_info_state(self):
        """sets the state to send to the overhead info object"""
        return c.GAME_OVER

    def update(self, surface, current_time):
        self.current_time = current_time
        self.sound_manager.update(self.persist, None)

        if (self.current_time - self.start_time) < 7000:
            surface.fill(c.BLACK)
            self.overhead_info.update(self.game_info)
            self.overhead_info.draw(surface)
        elif (self.current_time - self.start_time) < 7200:
            surface.fill(c.BLACK)
        elif (self.current_time - self.start_time) < 7235:
            surface.fill((106, 150, 252))
        else:
            self.done = True

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            self.get_event(event)


class TimeOut(LoadScreen):
    """Loading Screen with Time Out"""
    def __init__(self):
        super(TimeOut, self).__init__()

    def set_next_state(self):
        """Sets next state"""
        if self.persist[c.LIVES] == 0:
            return c.GAME_OVER
        else:
            return c.LOAD_SCREEN

    def set_overhead_info_state(self):
        """Sets the state to send to the overhead info object"""
        return c.MAIN_MENU

    def update(self, surface, current_time):
        self.current_time = current_time

        if (self.current_time - self.start_time) < 2400:
            surface.fill(c.BLACK)
            self.overhead_info.update(self.game_info)
            self.overhead_info.draw(surface)
        else:
            self.done = True

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            self.get_event(event)


class Victory(LoadScreen):
    """Loading Screen with Time Out"""
    def __init__(self):
        super(Victory, self).__init__()
        self.play=False
        self.text = pg.image.load('resources/graphics/reward.png').convert_alpha()
        self.bg_x1 = 100
        self.bg_y1 = 150

    def set_next_state(self):
        """Sets next state"""
        return c.MAIN_MENU

    def set_overhead_info_state(self):
        """Sets the state to send to the overhead info object"""
        return c.VICTORY

    def play_reward(self):
        if self.previous == c.UNI:
            path='resources/video/Meduni/'
        if self.previous == c.FLAPPY:
            path='resources/video/STP/'
        if self.previous == c.BIRTH:
            path = 'resources/video/Birth/'
        if self.previous == c.DK:
            path='resources/video/Pfeilheim/'
        if self.previous == c.GABON:
            path='resources/video/Gabon/'
        if self.previous == c.LEVEL1:
            path='resources/video/London/'

        commands = []
        for fname in os.listdir(path):
            if fname != ".DS_Store":
                command = ('open ' + path + fname)
                commands.append(command)
        processes = [subprocess.Popen(cmd, shell=True) for cmd in commands]
        for p in processes:
            p.wait()

    def update(self, surface, current_time):
        surface.fill(c.BLACK)
        surface.blit(self.text, (self.bg_x1, self.bg_y1))
        if self.play == False:
            self.play = True
            pg.time.wait(500)
            self.play_reward()
        if pg.K_RETURN in self.keys:
            self.play = False
            self.done = True

    def event_loop(self):
        self.keys = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.keys.append(event.key)
                self.toggle_show_fps(event.key)
            self.get_event(event)








