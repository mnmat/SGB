__author__ = 'justinarmstrong'

import pygame as pg
from data import setup, tools
from data import constants as c
from .. components import info, mario
import sys


class Character(pg.sprite.Sprite):
    """Parent class for all characters used for the overhead level info"""
    def __init__(self, image):
        super(Character, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()


class Birth(tools._State):
    def __init__(self):
        """Initializes the state"""
        tools._State.__init__(self)

    def startup(self, current_time, persist):
        """Called when the State object is created"""
        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.game_info[c.LEVEL_STATE] = c.NOT_FROZEN
        self.game_info[c.MARIO_DEAD] = False
        self.state = c.NOT_FROZEN
        self.sprite_sheet = setup.GFX['text_images']

        pg.mixer.music.load('resources/music/birth.wav')
        pg.mixer.music.play(-1)

        self.game_active = True
        self.victory = False

        self.input=[]
        self.input_list=[]

        self.create_image_dict()
        self.setup_cursor()
        self.create_letters()
        #self.create_description()
        self.create_name()

    def create_description(self):
        self.description = []

        self.create_label(self.description, 'NAME  ', 140, 100)

        self.description_list=[self.description]


    def create_name(self):

        self.name = []

        self.create_label(self.name, '----------', 280, 200)

        self.name_list = [self.name]

    def create_letters(self):
        """Creates the labels that describe each info"""
        self.A = []
        self.B = []
        self.C = []
        self.D = []
        self.E = []
        self.F = []
        self.G = []
        self.H = []
        self.I = []
        self.J = []
        self.K = []
        self.L = []
        self.M = []
        self.N = []
        self.O = []
        self.P = []
        self.Q = []
        self.R = []
        self.S = []
        self.T = []
        self.U = []
        self.V = []
        self.W = []
        self.X = []
        self.Y = []
        self.Z = []

        x = 140
        dx = 40
        y = 300
        dy =100


        self.create_label(self.A, 'A', x, y)
        self.create_label(self.B, 'B', x+1*dx, y)
        self.create_label(self.C, 'C', x+2*dx, y)
        self.create_label(self.D, 'D', x+3*dx, y)
        self.create_label(self.E, 'E', x+4*dx, y)
        self.create_label(self.F, 'F', x+5*dx, y)
        self.create_label(self.G, 'G', x+6*dx, y)
        self.create_label(self.H, 'H', x+7*dx, y)
        self.create_label(self.I, 'I', x+8*dx, y)
        self.create_label(self.J, 'J', x+9*dx, y)
        self.create_label(self.K, 'K', x+10*dx, y)
        self.create_label(self.L, 'L', x+11*dx, y)
        self.create_label(self.M, 'M', x+12*dx, y)
        self.create_label(self.N, 'N', x, y+dy)
        self.create_label(self.O, 'O', x+1*dx, y+dy)
        self.create_label(self.P, 'P', x+2*dx, y+dy)
        self.create_label(self.Q, 'Q', x+3*dx, y+dy)
        self.create_label(self.R, 'R', x+4*dx, y+dy)
        self.create_label(self.S, 'S', x+5*dx, y+dy)
        self.create_label(self.T, 'T', x+6*dx, y+dy)
        self.create_label(self.U, 'U', x+7*dx, y+dy)
        self.create_label(self.V, 'V', x+8*dx, y+dy)
        self.create_label(self.W, 'W', x+9*dx, y+dy)
        self.create_label(self.X, 'X', x+10*dx, y+dy)
        self.create_label(self.Y, 'Y', x+11*dx, y+dy)
        self.create_label(self.Z, 'Z', x+12*dx, y+dy)


        self.label_list = [self.A,
                           self.B,
                           self.C,
                           self.D,
                           self.E,
                           self.F,
                           self.G,
                           self.H,
                           self.I,
                           self.J,
                           self.K,
                           self.L,
                           self.M,
                           self.N,
                           self.O,
                           self.P,
                           self.Q,
                           self.R,
                           self.S,
                           self.T,
                           self.U,
                           self.V,
                           self.W,
                           self.X,
                           self.Y,
                           self.Z,]

    def create_image_dict(self):
        """Creates the initial images for the score"""
        self.image_dict = {}
        image_list = []

        image_list.append(self.get_image(3, 230, 7, 7))
        image_list.append(self.get_image(12, 230, 7, 7))
        image_list.append(self.get_image(19, 230, 7, 7))
        image_list.append(self.get_image(27, 230, 7, 7))
        image_list.append(self.get_image(35, 230, 7, 7))
        image_list.append(self.get_image(43, 230, 7, 7))
        image_list.append(self.get_image(51, 230, 7, 7))
        image_list.append(self.get_image(59, 230, 7, 7))
        image_list.append(self.get_image(67, 230, 7, 7))
        image_list.append(self.get_image(75, 230, 7, 7))

        image_list.append(self.get_image(83, 230, 7, 7))
        image_list.append(self.get_image(91, 230, 7, 7))
        image_list.append(self.get_image(99, 230, 7, 7))
        image_list.append(self.get_image(107, 230, 7, 7))
        image_list.append(self.get_image(115, 230, 7, 7))
        image_list.append(self.get_image(123, 230, 7, 7))
        image_list.append(self.get_image(3, 238, 7, 7))
        image_list.append(self.get_image(11, 238, 7, 7))
        image_list.append(self.get_image(20, 238, 7, 7))
        image_list.append(self.get_image(27, 238, 7, 7))
        image_list.append(self.get_image(35, 238, 7, 7))
        image_list.append(self.get_image(44, 238, 7, 7))
        image_list.append(self.get_image(51, 238, 7, 7))
        image_list.append(self.get_image(59, 238, 7, 7))
        image_list.append(self.get_image(67, 238, 7, 7))
        image_list.append(self.get_image(75, 238, 7, 7))
        image_list.append(self.get_image(83, 238, 7, 7))
        image_list.append(self.get_image(91, 238, 7, 7))
        image_list.append(self.get_image(99, 238, 7, 7))
        image_list.append(self.get_image(108, 238, 7, 7))
        image_list.append(self.get_image(115, 238, 7, 7))
        image_list.append(self.get_image(123, 238, 7, 7))
        image_list.append(self.get_image(3, 246, 7, 7))
        image_list.append(self.get_image(11, 246, 7, 7))
        image_list.append(self.get_image(20, 246, 7, 7))
        image_list.append(self.get_image(27, 246, 7, 7))
        image_list.append(self.get_image(48, 248, 7, 7))

        image_list.append(self.get_image(68, 249, 6, 2))
        image_list.append(self.get_image(75, 247, 6, 6))



        character_string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -*'

        for character, image in zip(character_string, image_list):
            self.image_dict[character] = image

    def create_label(self, label_list, string, x, y):
        """Creates a label (WORLD, TIME, MARIO)"""
        for letter in string:
            label_list.append(Character(self.image_dict[letter]))

        self.set_label_rects(label_list, x, y)


    def set_label_rects(self, label_list, x, y):
        """Set the location of each individual character"""
        for i, letter in enumerate(label_list):
            letter.rect.x = x + ((letter.rect.width + 3) * i)
            letter.rect.y = y
            if letter.image == self.image_dict['-']:
                letter.rect.y += 7
                letter.rect.x += 2


    def setup_cursor(self):
        """Creates the mushroom cursor to select 1 or 2 player game"""
        self.cursor = pg.sprite.Sprite()
        dest = (140, 358)
        self.cursor.image, self.cursor.rect = self.get_cursor(
            24, 160, 8, 8, dest, setup.GFX['item_objects'])
        self.cursor.state = c.A

    def get_cursor(self, x, y, width, height, dest, sprite_sheet):
        """Returns images and rects to blit onto the screen"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(sprite_sheet, (0, 0), (x, y, width, height))
        if sprite_sheet == setup.GFX['title_screen']:
            image.set_colorkey((255, 0, 220))
            image = pg.transform.scale(image,
                                   (int(rect.width*c.SIZE_MULTIPLIER),
                                    int(rect.height*c.SIZE_MULTIPLIER)))
        else:
            image.set_colorkey(c.BLACK)
            image = pg.transform.scale(image,
                                   (int(rect.width*3),
                                    int(rect.height*3)))

        rect = image.get_rect()
        rect.x = dest[0]
        rect.y = dest[1]
        return (image, rect)


    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((92, 148, 252))
        image = pg.transform.scale(image,
                                   (int(rect.width*2.9),
                                    int(rect.height*2.9)))
        return image

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
        self.update_input()

        surface.fill(c.BLACK)
        for word in self.label_list:
            for letter in word:
                surface.blit(letter.image, letter.rect)

        #for x in self.description_list:
        #    for letter in x:
        #        surface.blit(letter.image, letter.rect)

        for x in self.name_list:
            for letter in x:
                surface.blit(letter.image, letter.rect)

        for x in self.input_list:
            for letter in x:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.cursor.image, self.cursor.rect)


    def update_name(self,string):
        if len(self.input) < 8:
            self.list_input = []
            self.input.append(string)

            string = ''
            for ele in self.input:
                string = string + ele

            self.create_label(self.list_input, string, 290, 180)
            self.input_list = [self.list_input]

    def update_input(self):
        if 8 in self.keys: # not sure why pg.K_DELETE outputs 127 and not 8
            self.input = self.input[:-1]
            self.list_input = []

            string = ''
            for ele in self.input:
                string = string + ele

            self.create_label(self.list_input, string, 290, 180)
            self.input_list = [self.list_input]

        if pg.K_RETURN in self.keys:
            string = ''
            for ele in self.input:
                string = string + ele

            if string == "REINHOLD":
                pg.mixer.music.fadeout(1000)
                self.next = c.VICTORY
                self.done = True

            else:
                self.input = []
                self.list_input = []
                self.input_list = [self.list_input]


    def update_cursor(self):
        """Update the position of the cursor"""
        input_list = [pg.K_RETURN, pg.K_a, pg.K_s]
        x = 140
        dx = 40
        y = 340
        dy = 100
        if self.cursor.state == c.A:
            self.cursor.rect.x = x
            self.cursor.rect.y = y
            if pg.K_DOWN in self.keys:
                self.cursor.state = c.N
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.B
            for input in input_list:
                if input in self.keys:
                    self.update_name('A')
        elif self.cursor.state == c.N:
            self.cursor.rect.x = x
            self.cursor.rect.y = y + dy
            if pg.K_UP in self.keys:
                self.cursor.state = c.A
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.O
            for input in input_list:
                if input in self.keys:
                    self.update_name('N')
        elif self.cursor.state == c.B:
            self.cursor.rect.x = x+dx
            self.cursor.rect.y = y
            if pg.K_DOWN in self.keys:
                self.cursor.state = c.O
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.C
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.A
            for input in input_list:
                if input in self.keys:
                    self.update_name('B')
        elif self.cursor.state == c.O:
            self.cursor.rect.x = x + dx
            self.cursor.rect.y = y + dy
            if pg.K_UP in self.keys:
                self.cursor.state = c.B
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.P
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.N
            for input in input_list:
                if input in self.keys:
                    self.update_name('O')
        elif self.cursor.state == c.C:
            self.cursor.rect.x = x+2*dx
            self.cursor.rect.y = y
            if pg.K_DOWN in self.keys:
                self.cursor.state = c.P
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.D
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.B
            for input in input_list:
                if input in self.keys:
                    self.update_name('C')
        elif self.cursor.state == c.P:
            self.cursor.rect.x = x + 2*dx
            self.cursor.rect.y = y + dy
            if pg.K_UP in self.keys:
                self.cursor.state = c.C
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.Q
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.O
            for input in input_list:
                if input in self.keys:
                    self.update_name('P')
        elif self.cursor.state == c.D:
            self.cursor.rect.x = x+3*dx
            self.cursor.rect.y = y
            if pg.K_DOWN in self.keys:
                self.cursor.state = c.Q
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.E
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.C
            for input in input_list:
                if input in self.keys:
                    self.update_name('D')
        elif self.cursor.state == c.Q:
            self.cursor.rect.x = x +3*dx
            self.cursor.rect.y = y + dy
            if pg.K_UP in self.keys:
                self.cursor.state = c.D
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.R
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.P
            for input in input_list:
                if input in self.keys:
                    self.update_name('Q')
        elif self.cursor.state == c.E:
            self.cursor.rect.x = x + 4*dx
            self.cursor.rect.y = y
            if pg.K_DOWN in self.keys:
                self.cursor.state = c.R
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.F
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.D
            for input in input_list:
                if input in self.keys:
                    self.update_name('E')
        elif self.cursor.state == c.R:
            self.cursor.rect.x = x + 4*dx
            self.cursor.rect.y = y + dy
            if pg.K_UP in self.keys:
                self.cursor.state = c.E
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.S
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.Q
            for input in input_list:
                if input in self.keys:
                    self.update_name('R')
        elif self.cursor.state == c.F:
            self.cursor.rect.x = x + 5*dx
            self.cursor.rect.y = y
            if pg.K_DOWN in self.keys:
                self.cursor.state = c.S
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.G
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.E
            for input in input_list:
                if input in self.keys:
                    self.update_name('F')
        elif self.cursor.state == c.S:
            self.cursor.rect.x = x + 5*dx
            self.cursor.rect.y = y + dy
            if pg.K_UP in self.keys:
                self.cursor.state = c.F
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.T
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.R
            for input in input_list:
                if input in self.keys:
                    self.update_name('S')
        elif self.cursor.state == c.G:
            self.cursor.rect.x = x + 6*dx
            self.cursor.rect.y = y
            if pg.K_DOWN in self.keys:
                self.cursor.state = c.T
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.H
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.F
            for input in input_list:
                if input in self.keys:
                    self.update_name('G')
        elif self.cursor.state == c.T:
            self.cursor.rect.x = x+6*dx
            self.cursor.rect.y = y + dy
            if pg.K_UP in self.keys:
                self.cursor.state = c.G
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.U
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.S
            for input in input_list:
                if input in self.keys:
                    self.update_name('T')
        elif self.cursor.state == c.H:
            self.cursor.rect.x = x+7*dx
            self.cursor.rect.y = y
            if pg.K_DOWN in self.keys:
                self.cursor.state = c.U
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.I
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.G
            for input in input_list:
                if input in self.keys:
                    self.update_name('H')
        elif self.cursor.state == c.U:
            self.cursor.rect.x = x + 7*dx
            self.cursor.rect.y = y + dy
            if pg.K_UP in self.keys:
                self.cursor.state = c.H
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.V
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.T
            for input in input_list:
                if input in self.keys:
                    self.update_name('U')
        elif self.cursor.state == c.I:
            self.cursor.rect.x = x + 8*dx
            self.cursor.rect.y = y
            if pg.K_DOWN in self.keys:
                self.cursor.state = c.V
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.J
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.H
            for input in input_list:
                if input in self.keys:
                    self.update_name('I')
        elif self.cursor.state == c.V:
            self.cursor.rect.x = x + 8*dx
            self.cursor.rect.y = y + dy
            if pg.K_UP in self.keys:
                self.cursor.state = c.I
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.W
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.U
            for input in input_list:
                if input in self.keys:
                    self.update_name('V')
        elif self.cursor.state == c.J:
            self.cursor.rect.x = x + 9*dx
            self.cursor.rect.y = y
            if pg.K_DOWN in self.keys:
                self.cursor.state = c.W
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.K
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.I
            for input in input_list:
                if input in self.keys:
                    self.update_name('J')
        elif self.cursor.state == c.W:
            self.cursor.rect.x = x+9*dx
            self.cursor.rect.y = y + dy
            if pg.K_UP in self.keys:
                self.cursor.state = c.J
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.X
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.V
            for input in input_list:
                if input in self.keys:
                    self.update_name('W')
        elif self.cursor.state == c.K:
            self.cursor.rect.x = x+10*dx
            self.cursor.rect.y = y
            if pg.K_DOWN in self.keys:
                self.cursor.state = c.X
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.L
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.J
            for input in input_list:
                if input in self.keys:
                    self.update_name('K')
        elif self.cursor.state == c.X:
            self.cursor.rect.x = x+10*dx
            self.cursor.rect.y = y + dy
            if pg.K_UP in self.keys:
                self.cursor.state = c.K
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.Y
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.W
            for input in input_list:
                if input in self.keys:
                    self.update_name('X')
        elif self.cursor.state == c.L:
            self.cursor.rect.x = x+11*dx
            self.cursor.rect.y = y
            if pg.K_DOWN in self.keys:
                self.cursor.state = c.Y
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.M
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.K
            for input in input_list:
                if input in self.keys:
                    self.update_name('L')
        elif self.cursor.state == c.Y:
            self.cursor.rect.x = x+11*dx
            self.cursor.rect.y = y + dy
            if pg.K_UP in self.keys:
                self.cursor.state = c.L
            if pg.K_RIGHT in self.keys:
                self.cursor.state = c.Z
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.X
            for input in input_list:
                if input in self.keys:
                    self.update_name('Y')
        elif self.cursor.state == c.M:
            self.cursor.rect.x = x+12*dx
            self.cursor.rect.y = y
            if pg.K_DOWN in self.keys:
                self.cursor.state = c.Z
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.L
            for input in input_list:
                if input in self.keys:
                    self.update_name('M')
        elif self.cursor.state == c.Z:
            self.cursor.rect.x = x+12*dx
            self.cursor.rect.y = y + dy
            if pg.K_UP in self.keys:
                self.cursor.state = c.M
            if pg.K_LEFT in self.keys:
                self.cursor.state = c.Y
            for input in input_list:
                if input in self.keys:
                    self.update_name('Z')

    def reset_game_info(self):
        """Resets the game info in case of a Game Over and restart"""
        self.game_info[c.COIN_TOTAL] = 0
        self.game_info[c.SCORE] = 0
        self.game_info[c.LIVES] = 3
        self.game_info[c.CURRENT_TIME] = 0.0
        self.game_info[c.LEVEL_STATE] = None

        self.persist = self.game_info



