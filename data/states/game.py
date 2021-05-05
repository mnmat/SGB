""" 
@author: Anuj Kumar
@email: cdac.anuj@gmail.com
@date: 29th-July-2018
"""
import random
from time import sleep
from data import setup, tools
from data import constants as c
import sys
from .. import game_sound
from data.components import info

import pygame

class CarRacing(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def startup(self,current_time,persist):

        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.game_info[c.LEVEL_STATE] = c.NOT_FROZEN
        self.game_info[c.MARIO_DEAD] = False
        self.overhead_info = info.OverheadInfo(self.game_info, c.GABON)
        pygame.mixer.music.load('resources/music/jungle.mp3')
        pygame.mixer.music.play(-1)

        self.display_width = 800
        self.display_height = 600
        self.message = False

        setup.SCREEN = pygame.display.set_mode((self.display_width, self.display_height))
        setup.SCREEN_RECT = setup.SCREEN.get_rect()
        self.state = c.NOT_FROZEN

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.mul = [1,2,3,4,5,6,8,10]

        self.initialize()

    def initialize(self):

        self.crashed = False
        self.victory = False

        self.carImg = pygame.image.load("resources/graphics/canoe_full.png")
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        # enemy_car
        self.enemy_car = pygame.image.load("resources/graphics/hippo.png")
        self.enemy_car_startx = random.randrange(210, 590)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # reward
        self.reward = pygame.image.load("resources/graphics/Croc.png")
        self.reward_startx = random.randrange(210, 590)
        self.reward_starty = -600
        self.reward_speed = 5
        self.reward_width = 49
        self.reward_height = 100


        # Background
        self.bgImg = pygame.image.load("resources/graphics/jungle.png")
        self.bg_x1 = 0
        self.bg_x2 = 0
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 1
        self.count = 0
        self.score = 0

    def update(self, surface, current_time):
        """Updates Entire level using states.  Called by the control object"""
        self.game_info[c.CURRENT_TIME] = self.current_time = current_time
        self.handle_states()
        self.blit_everything(surface)

    def blit_everything(self,surface):
        self.back_ground_road(surface)
        self.car(self.car_x_coordinate, self.car_y_coordinate,surface)
        self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty,surface)
        self.run_reward(self.reward_startx, self.reward_starty,surface)
        self.display_message(surface)
        self.highscore(self.score,surface)


    def handle_states(self):
        if self.crashed == False:
            self.back_ground_update()
            self.car_update()
            self.update_enemy()
            self.update_reward()
            self.update_speed()
            self.check_collision()
        if self.crashed == True:
            self.game_update()

    def game_update(self):
        if self.victory == False:
            self.initialize()
        if self.victory == True:
            pygame.mixer.music.fadeout(1000)
            self.next = c.VICTORY
            self.done = True
            setup.SCREEN = pygame.display.set_mode((800, 600))
            setup.SCREEN_RECT = setup.SCREEN.get_rect()

    def check_collision(self):
        if self.car_y_coordinate < self.reward_starty + self.reward_height:
            if self.car_x_coordinate > self.reward_startx and self.car_x_coordinate < self.reward_startx + self.reward_width or self.car_x_coordinate + self.car_width > self.reward_startx and self.car_x_coordinate + self.car_width < self.reward_startx + self.reward_width:
                self.reward_starty = 0 - self.reward_height
                self.reward_startx = random.randrange(210, 540)
                self.score += 1

        if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
            if self.car_x_coordinate > self.enemy_car_startx and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or self.car_x_coordinate + self.car_width > self.enemy_car_startx and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                self.crashed = True
                self.message = True

        if self.car_x_coordinate < 210 or self.car_x_coordinate > 590:
            self.crashed = True
            self.message = True

        if self.score >= 40:
            self.crashed = True
            self.victory = True
            self.message = True


    def update_speed(self):
        self.count += 1
        if self.count % 600 == 0 and self.bg_speed < 8:
            self.enemy_car_speed += 1
            self.reward_speed += 1
            self.bg_speed = self.mul[int(self.count / 600)]

    def update_enemy(self):
        self.enemy_car_starty += self.enemy_car_speed

        if self.enemy_car_starty > self.display_height:
            self.enemy_car_starty = 0 - self.enemy_car_height
            self.enemy_car_startx = random.randrange(210, 540)

    def update_reward(self):
        self.reward_starty += self.reward_speed

        if self.reward_starty > self.display_height:
            self.reward_starty = 0 - self.reward_height
            self.reward_startx = random.randrange(210, 540)

    def car_update(self):
        if tools.keybinding['left'] in self.keys:
            self.car_x_coordinate -= 50
        if tools.keybinding['right'] in self.keys:
            self.car_x_coordinate += 50

    def car(self, car_x_coordinate, car_y_coordinate,surface):
        surface.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Gabon Jungle Ride')
        self.run_car()

    def display_message(self, surface):
        if self.message == True:
            font = pygame.font.SysFont("comicsansms", 72, True)
            if self.victory == True:
                msg = "Victory!!!"
            else:
                msg = "Game Over!!!"

            text = font.render(msg, True, (255, 255, 255))
            surface.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
            pygame.display.update()
            self.clock.tick(60)
            sleep(1)
            self.message = False

    def back_ground_update(self):
        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def back_ground_road(self,surface):
        surface.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        surface.blit(self.bgImg, (self.bg_x2, self.bg_y2))

    def run_enemy_car(self, thingx, thingy,surface):
        surface.blit(self.enemy_car, (thingx, thingy))

    def run_reward(self, thingx, thingy, surface):
        surface.blit(self.reward, (thingx, thingy))

    def highscore(self, count,surface):
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Croc Score : " + str(count), True, self.white)
        surface.blit(text, (0, 0))

    def event_loop(self):
        self.keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.keys.append(event.key)
                #self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
            self.get_event(event)


