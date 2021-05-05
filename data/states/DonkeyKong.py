# Kendra Tam
# DonkeyKong_KendraTam.py
# May 27, 2016
# This program is simulating the arcade game Donkey Kong

#importing
import pygame, sys
from data import setup, tools
from data import constants as c
import random
from pygame import mixer

class DK(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def startup(self, current_time, persist):
        """Called when the State object is created"""

        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.game_info[c.LEVEL_STATE] = c.NOT_FROZEN
        self.game_info[c.MARIO_DEAD] = False

        self.state = c.NOT_FROZEN
        self.death_timer = 0
        self.flag_timer = 0
        self.flag_score = None
        self.flag_score_total = 0

        self.leaderboard = {}
        self.score = 0
        self.highestScore = 0
        self.levelNum = 0
        self.difficulty = 0

        self.option = "top"
        self.direction = "right"
        self.display_width = 800
        self.display_height = 800
        setup.SCREEN = pygame.display.set_mode((self.display_width, self.display_height))
        setup.SCREEN_RECT = setup.SCREEN.get_rect()
        self.clock = pygame.time.Clock()
        self.inPlay = True

        self.setup_dk()
        self.setup_mario()
        self.setup_platforms()
        self.setup_barrels()
        self.setup_ladders()
        self.setup_pauline()
        self.setup_screens()
        self.setup_confetti()
        self.setup_boundaries()
        self.setup_icons()

        self.initialize()
        self.instructions()

    def setup_barrels(self):
        self.barrelLadderX = [320, 610, 560, 280, 160, 250, 400, 610, 350, 160, 300, 610]
        self.barrelLadderY1 = [243, 252, 326, 270, 350, 428, 437, 449, 535, 547, 627, 645]
        self.barrelLadderY2 = [343, 322, 446, 344, 420, 538, 527, 519, 625, 617, 727, 715]
        self.barrelAdjust = [-2, 1, -1, 4, 2, 3, 5, 1, 5, 1, 4, 1]

        self.barrelX = []
        self.barrelY = []
        self.throwCountdown = 0
        self.barrelDirection = []
        self.fall = []
        self.fallCount = []
        self.barrelLeft = []
        self.barrelRight = []

        self.barrelStack = pygame.image.load(path_g + "ottakringer_stack.png")
        self.barrelDown = pygame.image.load(path_g + "ottakringer_down.png")
        self.barrel1 = pygame.image.load(path_g + "ottakringer_top1.png")
        self.barrel2 = pygame.image.load(path_g + "ottakringer_top2.png")
        self.barrel3 = pygame.image.load(path_g + "ottakringer_top3.png")
        self.barrel4 = pygame.image.load(path_g + "ottakringer_top4.png")
        self.barrelSequence = [self.barrel1, self.barrel2, self.barrel3, self.barrel4]
        self.barrelPic = []



    def setup_platforms(self):
        self.platformsX = [55, 55, 51, 60, 56, 56, 56]
        self.platformsY = [9, 10, 8, 9, 11, 9, 9, 11]
        self.platNum = 0
        self.platInclineX = [100, 140, 190, 240, 280, 330, 380, 430, 480, 530, 570, 620, 670, 720]
        self.inclineCount = 0

        self.platform0 = pygame.image.load(path_g + "platform0.png")
        self.platform1 = pygame.image.load(path_g + "platform1.png")
        self.platform2 = pygame.image.load(path_g + "platform2.png")
        self.platform3 = pygame.image.load(path_g + "platform3.png")
        self.platform4 = pygame.image.load(path_g + "platform4.png")
        self.platform5 = pygame.image.load(path_g + "platform5.png")
        self.platform6 = pygame.image.load(path_g + "platform6.png")
        self.platforms = [self.platform0, self.platform1, self.platform2, self.platform3, self.platform4, self.platform5, self.platform6]


    def setup_mario(self):
        self.marioX = 150
        self.marioY = 720
        self.addJump = -7
        self.jumpCount = 0
        self.jumpPoint = 0
        self.deathCount = 0
        self.lives = 2

        self.marioLeft = pygame.image.load(path_g + "julian.png")
        self.marioRight = pygame.image.load(path_g + "julian.png")
        self.runLeft = pygame.image.load(path_g + "julian.png")
        self.runRight = pygame.image.load(path_g + "julian.png")
        self.marioJumpLeft = pygame.image.load(path_g + "julian.png")
        self.marioJumpRight = pygame.image.load(path_g + "julian.png")
        self.marioClimb1 = pygame.image.load(path_g + "julian.png")
        self.marioClimb2 = pygame.image.load(path_g + "julian.png")
        self.dead = pygame.image.load(path_g + "julian_vomit.png")
        self.marioImage = self.marioRight


    def setup_dk(self):
        self.dkClimb = 0
        self.climbCount = 15
        self.platNum = 0
        self.dkJumpX = 378
        self.dkJumpY = 172
        self.dkJumpYNum = 0

        self.dkUp1 = pygame.image.load(path_g + "DK_up1.png")
        self.dkUp2 = pygame.image.load(path_g + "DK_up2.png")
        self.dkEmptyClimb1 = pygame.image.load(path_g + "dkClimbEmpty1.png")
        self.dkEmptyClimb2 = pygame.image.load(path_g + "dkClimbEmpty2.png")
        self.dkForward = pygame.image.load(path_g + "dkForward.png")
        self.dkLeft = pygame.image.load(path_g + "dkLeft.png")
        self.dkRight = pygame.image.load(path_g + "dkRight.png")
        self.dkDefeat = pygame.image.load(path_g + "DK-defeat.png")
        self.dkImage = self.dkForward

    def setup_ladders(self):
        self.ladderX1 = [295, 605, 295, 345, 345, 150, 245, 385, 600, 600, 245, 150, 265, 265, 315, 555, 555, 600, 440, 320]
        self.ladderX2 = [305, 610, 310, 350, 350, 160, 255, 400, 610, 610, 255, 160, 280, 280, 325, 565, 565, 610, 450, 335]
        self.ladderY1 = [710, 635, 617, 610, 526, 538, 522, 423, 506, 435, 414, 338, 409, 332, 309, 314, 417, 241, 154, 232]
        self.ladderY2 = [720, 705, 657, 620, 571, 608, 532, 523, 511, 475, 464, 408, 414, 382, 329, 369, 432, 311, 232, 272]
        self.fullLadderUp = [False, True, True, False, True, True, False, True, False, True, True, True, False, True, False,
                        True, False, True, True, True]
        self.fullLadderDown = [True, True, False, True, False, True, True, True, True, False, False, True, True, False, True,
                          False, True, True, True, False]

    def setup_pauline(self):
        self.paulineHelp = pygame.image.load(path_g + "hannah_stand.png")
        self.paulineStill = pygame.image.load(path_g + "hannah_stand.png")

        self.brokenHeart = pygame.image.load(path_g + "broken-heart.png")
        self.fullHeart = pygame.image.load(path_g + "full-heart.png")

    def setup_screens(self):
        self.title = pygame.image.load(path_g + "title-screen.png")
        self.start = pygame.image.load(path_g + "start.png")
        self.winScreen = pygame.image.load(path_g + "win-screen.png")
        self.gameOverScreen = pygame.image.load(path_g + "game-over-screen.png")
        self.withLadder = pygame.image.load(path_g + "withLadder.png")
        self.level = pygame.image.load(path_g + "level.png")

    def setup_confetti(self):
        self.confettiX = []
        self.confettiY = []
        self.confettiRadius = []
        self.confettiSpeed = []
        self.confettiColour = []

        # declares values for 400 confetti pieces
        for i in range(0, 400):
            # chooses random x value and appends it to list
            x = random.randint(0, 800)
            self.confettiX.append(x)

            # chooses random y value and appends it to list
            y = random.randint(-500, -100)
            self.confettiY.append(y)

            # chooses random radius and appends it to list
            r = random.randint(1, 4)
            self.confettiRadius.append(r)

            # chooses random speed and appends it to list
            s = random.randint(5, 20)
            self.confettiSpeed.append(s)

            # chooses random colour and appends it to list
            colour = random.randint(0, 4)
            self.confettiColour.append(colours[colour])

    def setup_icons(self):
        self.selectIcon = pygame.image.load(path_g + "select-icon.png")
        self.life = pygame.image.load(path_g + "mario-life.png")

        self.blue0 = pygame.image.load(path_g + "blue0.png")
        self.blue1 = pygame.image.load(path_g + "blue1.png")
        self.blue2 = pygame.image.load(path_g + "blue2.png")
        self.blue3 = pygame.image.load(path_g + "blue3.png")
        self.blue4 = pygame.image.load(path_g + "blue4.png")
        self.blue5 = pygame.image.load(path_g + "blue5.png")
        self.blueNumbers = [self.blue0, self.blue1, self.blue2, self.blue3, self.blue4, self.blue5]
        self.white0 = pygame.image.load(path_g + "white0.png")
        self.white1 = pygame.image.load(path_g + "white1.png")
        self.white2 = pygame.image.load(path_g + "white2.png")
        self.white3 = pygame.image.load(path_g + "white3.png")
        self.white4 = pygame.image.load(path_g + "white4.png")
        self.white5 = pygame.image.load(path_g + "white5.png")
        self.white6 = pygame.image.load(path_g + "white6.png")
        self.white7 = pygame.image.load(path_g + "white7.png")
        self.white8 = pygame.image.load(path_g + "white8.png")
        self.white9 = pygame.image.load(path_g + "white9.png")
        self.whiteNumbers = [self.white0, self.white1, self.white2, self.white3, self.white4, self.white5, self.white6, self.white7, self.white8, self.white9]

    def setup_boundaries(self):
        self.leftBoundariesY = [541, 341]
        self.rightBoundariesY = [638, 438, 244]

    def initialize(self):
        self.replay = True
        self.pressed = False
        self.climbDone = False
        self.introDone = False
        self.startDone = False
        self.startOutput = False
        self.gameStart = False
        self.throwBarrel = False
        self.jumpLeft = False
        self.jumpRight = False
        self.jumpStill = False
        self.hit = False
        self.deathScene = False
        self.gameDone = False
        self.winGame = False
        self.winLevel = False
        self.scoreWin = False
        self.winGameSceneOutput = False
        self.winGameSceneDone = False

    def sound(self,state):
        if state == "Background":
            mixer.music.load(path_m+"bacmusic.wav")
            mixer.music.play(-1)
        if state == "Intro":
            mixer.music.load(path_m+"intro1_long.wav")
            mixer.music.play()

    def instructions(self):
        print ("Donkey Kong has kidnapped Pauline!")
        print ("You must now help Mario save her by climbing all the way")
        print ("up the structure to the platform where she is being held.")
        print
        print ("You will have three lives, and you get points by rescuing")
        print ("Pauline and jumping over barrels.")
        print ("To win, save her 5 times or get a score of 999999 or over.")
        print
        print ("Use the arrow keys to move, and press the space to jump.")
        print
        print ("In the menus, use the up and down keys to choose your option")
        print ("and the return key to select it.")
        print
        print ("GOOD LUCK!")
        print

    def event_loop(self):
        pygame.event.get()
        self.keys = pygame.key.get_pressed()

    def update(self, surface, current_time):
        """Updates Entire level using states.  Called by the control object"""
        self.game_info[c.CURRENT_TIME] = self.current_time = current_time
        self.handle_states()
        self.blit_everything(surface)
        #self.sound_manager.update(self.game_info, self.mario)

    def blit_everything(self,surface):
        if self.inPlay:
            self.redraw_screen(surface)  # the screen window must be constantly redrawn - animation
            # pygame.time.delay(45)           # pause for 20 miliseconds
            self.clock.tick(20)

        # if it is True, delay the program for 2 seconds to see the startScreen for longer
        if self.startOutput:
            pygame.time.delay(2000)

            # re-set variables
            self.startOutput = False
            self.gameStart = True

        # if it is True, delay the program for 2.5 seconds to see your victory for longer
        if self.winGameSceneOutput:
            pygame.time.delay(2500)

            # re-set variables
            self.winGameSceneOutput = False
            self.winGameSceneDone = True

    def handle_states(self):
        self.update_intro()
        if self.gameStart:
            self.check_collision()
            if self.hit == False:
                self.update_life()
            else:
                self.update_death()
        if self.winLevel:
            self.update_level()
        self.interaction()

    def interaction(self):
        if self.keys[pygame.K_ESCAPE]:

            # reset variables to quit program
            self.inPlay = False
            self.replay = False

            # looks for space to be pressed to make pressed True and start the game
        if self.keys[pygame.K_SPACE]:
            self.pressed = True

            # must satisfy all these conditions in order for pressing  the left, right, up, down, space(for jumping), and return key to do anything
        if (
                self.gameStart and self.jumpLeft == False and self.jumpRight == False and self.jumpStill == False and self.winLevel == False and self.hit == False) or self.gameDone or self.winGame:

            # looks for left arrow to be pressed
            if self.keys[pygame.K_LEFT] and self.moveSides and (self.marioX != 320 or self.marioY > 232) and self.moveLeft and self.marioX != 60:
                # changes mario's y to incline up/go down with the slope
                self.marioY = self.incline(self.marioY, self.marioX, self.direction, "mario")

                # if mario is already facing left, subtract 5 from marioX
                if self.direction == "left":
                    self.marioX = self.marioX - 5

                # if the images for mario is marioLeft change it to runLeft
                if self.marioImage == self.marioLeft:
                    self.marioImage = self.runLeft
                # else, change it to marioLeft
                else:
                    self.marioImage = self.marioLeft

                # if space is pressed while left is also being pressed, jumpLeft is True and change the image
                if self.keys[pygame.K_SPACE]:
                    self.jumpLeft = True
                    self.marioImage = self.marioJumpLeft

                self.direction = "left"

            # looks for right arrow to be pressed
            elif self.keys[pygame.K_RIGHT] and self.moveSides and self.moveRight and self.marioX != 710:
                # changes mario's y to incline up/go down with the slope
                self.marioY = self.incline(self.marioY, self.marioX, self.direction, "mario")

                # if mario was already facing right, add 5 to the x value
                if self.direction == "right":
                    self.marioX = self.marioX + 5

                # if the images for mario is marioRight change it to runRight
                if self.marioImage == self.marioRight:
                    self.marioImage = self.runRight
                # else change it to marioRight
                else:
                    self.marioImage = self.marioRight

                # if space is pressed while right is also being pressed, jumpRight is True and change the image
                if self.keys[pygame.K_SPACE]:
                    self.jumpRight = True
                    self.marioImage = self.marioJumpRight

                self.direction = "right"

            # looks for up arrow to be pressed
            elif self.keys[pygame.K_UP] and (self.upLadder or self.gameDone or self.winGame):
                # if upLadder is true, move mario up 5 pixels
                if self.upLadder:
                    self.marioY =self.marioY - 5

                    # if marioImage is marioClimb1, change it to marioClimb2
                    if self.marioImage == self.marioClimb1:
                        self.marioImage = self.marioClimb2
                    # otherwise, change it to marioClimb1
                    else:
                        self.marioImage = self.marioClimb1

                # if the user is on one of the menus, change the option to select the top one
                if self.gameDone or self.winGame:
                    self.option = "top"

            # looks for down arrow to be pressed and only excutes when you can go down a ladder, and to sele
            elif self.keys[pygame.K_DOWN] and (self.downLadder or self.gameDone or self.winGame):
                # if downLadder is true, change mario's y coordinates to go down
                if self.downLadder:
                    self.marioY = self.marioY + 5

                    # if marioImage is marioClimb1, change it to marioClimb2
                    if self.marioImage == self.marioClimb1:
                        self.marioImage = self.marioClimb2
                    # otherwise, change it to marioClimb1
                    else:
                        self.marioImage = self.marioClimb1

                # if user is on one of the menus, change the option to select the bottom one
                if self.gameDone or self.winGame:
                    self.option = "bottom"

            # looks for space bar to be pressed and can only do something when mario already jumping left or right and you're not in the middle of a ladder
            if self.keys[pygame.K_SPACE] and self.jumpLeft == False and self.jumpRight == False and self.moveSides:
                # it makes jumpStil true
                self.jumpStill = True

                # if you are facing left, blit the image of mario jumping, facing right
                if self.direction == "right":
                    self.marioImage = self.marioJumpRight

                # else blit mario jumping and facing left
                else:
                    self.marioImage = self.marioJumpLeft

            # looks for return to be pressed and it can only do something when the game is lost or won
            if self.keys[pygame.K_RETURN] and (self.gameDone or self.winGame):
                # if the top option is selected, reset the game
                if self.option == "top":

                    # reset variables to restart
                    self.inPlay = True
                    self.winLevel = False
                    self.pressed = False
                    self.climbDone = False
                    self.introDone = False
                    self.gameStart = False
                    self.startDone = False
                    self.gameDone = False
                    self.throwBarrel = False
                    self.jumpLeft = False
                    self.jumpRight = False
                    self.jumpStill = False
                    self.winGame = False
                    self.winLevel = False
                    self.deathScene = False
                    self.scoreWin = False
                    self.winGameSceneDone = False
                    self.score = 0
                    self.levelNum = 0
                    self.dkClimb = 0
                    self.climbCount = 15
                    self.platNum = 0
                    self.dkJumpX = 378
                    self.dkJumpY = 172
                    self.dkJumpYNum = 0
                    self.marioX = 150
                    self.marioY = 720
                    self.addJump = -7
                    self.marioJumpCount = 0
                    self.lives = 2
                    self.difficulty = 0
                    self.barrelX = []
                    self.barrelY = []
                    self.barrelPic = []
                    self.throwCountdown = 0
                    self.barrelDirection = []
                    self.fall = []
                    self.fallCount = []
                    self.barrelLeft = []
                    self.barrelRight = []

                # if the bottom option is selected, you will quit the game
                elif self.option == "bottom":
                    # reset variables
                    self.inPlay = False
                    self.replay = False
                    self.done = True
                    self.next = c.GAME_OVER
                    setup.SCREEN = pygame.display.set_mode((800, 600))
                    setup.SCREEN_RECT = setup.SCREEN.get_rect()

    def update_level(self):

        # if the levelNum is 5 or scoreWin is true, reset values to output correct images in redraw_screen
        if self.levelNum == 1 or self.scoreWin:
            # if this is false, reset values to start the end of the game
            if self.winGameSceneDone == False:
                self.dkImage = self.dkDefeat
                self.winGameSceneOutput = True
            # else, add to the confetti's y coordinates find the highscore and put user's score into leadboard
            else:
                # goes through all the confetti circles
                for i in range(0, 400):
                    # add to make if fall down
                    self.confettiY[i] = self.confettiY[i] + self.confettiSpeed[i]
                self.highestScore = self.highScore()

            # reset values
            self.gameStart = False
            self.winGame = True



        # else, continue on to the next level
        else:

            # DK climbs up
            self.dkClimb = self.dkClimb + self.climbCount

            # if DK climbs 15 pixels, add 250 to the score and delay for time
            if self.dkClimb == 15:
                self.score = self.score + 250
                pygame.time.delay(1000)

            # if DK climbs less than or equal to 30 pixels, the two images are dk not holding pauline
            if self.dkClimb <= 30:
                self.dkImage1 = self.dkEmptyClimb1
                self.dkImage2 = self.dkEmptyClimb2
                self.moveOver1 = 0
                self.moveOver2 = 0
            # else, dk is holding pauline in these two images
            else:
                self.dkImage1 = self.dkUp1
                self.dkImage2 = self.dkUp2

                # adjusts image so that he climbs up smoothly
                self.moveOver1 = 13
                self.moveOver2 = 35

            # if DK has climbed 150 pixels, reset variables for the next level
            if self.dkClimb == 150:
                self.winLevel = False
                self.climbDone = False
                self.introDone = False
                self.startDone = False
                self.gameStart = False
                self.throwBarrel = False
                self.jumpLeft = False
                self.jumpRight = False
                self.jumpStill = False
                self.hit = False
                self.barrelX = []
                self.barrelY = []
                self.barrelPic = []
                self.barrelDirection = []
                self.fall = []
                self.fallCount = []
                self.barrelLeft = []
                self.barrelRight = []
                self.inclineCount = 0
                self.dkClimb = 0
                self.platNum = 0
                self.climbCount = 15
                self.dkJumpX = 378
                self.dkJumpY = 172
                self.dkJumpYNum = 0
                self.addJump = -7
                self.jumpCount = 0
                self.direction = "right"

                # to make the next level more difficult
                self.difficulty = self.difficulty + 8

    def check_collision(self):
        if self.scoreWin == False and self.winLevel == False:
            self.hit = self.collide()
            # checks if mario has hit a boundary to the left or right of him
            self.moveLeft, self.moveRight = self.boundaries(self.marioX, self.marioY)

    def update_death(self):

        # if the deathScene is not done
        if self.deathScene == False:
            mixer.music.stop()
            # moves the dead mario's y coordinates down to make sure he rests where his feet were, not where his head was
            if self.deathCount == 0:
                vomit_sound = mixer.Sound(path_s + "vomit.wav")
                vomit_sound.play()
                self.marioX = self.marioX - 26

            self.deathCount = self.deathCount + 1

            # when the count reaches 60, the short delay is over, reset variables, and lose a life
            if self.deathCount == 60:
                self.deathScene = True
                self.deathCount = 0
                self.lives = self.lives - 1

            # resets variables
            self.marioImage = self.dead

        # if deathScene is true, reset variables to start at the beginning of level again
        else:
            self.startDone = False
            self.gameStart = False
            self.throwBarrel = False
            self.deathScene = False
            self.hit = False
            self.jumpLeft = False
            self.jumpRight = False
            self.jumpStill = False
            self.barrelX = []
            self.barrelY = []
            self.barrelPic = []
            self.throwCountdown = 0
            self.barrelDirection = []
            self.fall = []
            self.fallCount = []
            self.barrelLeft = []
            self.barrelRight = []
            self.inclineCount = 0
            self.jumpPoint = 0
            self.marioX = 150
            self.marioY = 720
            self.addJump = -7
            self.jumpCount = 0
            self.direction = "right"
            self.marioImage = self.marioRight

        # if lives is less than 0, gameDone is True, and put score in leaderboards and find the high score using highScore()
        if self.lives < 0:
            self.gameDone = True

    def update_life(self):

        # checks if mario is on a ladder and whether he can go up, down or left and right
        self.upLadder, self.downLadder, self.moveSides = self.ladderCheck()

        # if mario reaches a y value of less than or equal to 154, he has won the game
        if self.marioY <= 154:
            # reset variables
            self.winLevel = True
            self.dkClimb = -15
            self.climbCount = 15
            self.marioX = 150
            self.marioY = 720
            self.marioImage = self.marioRight

        # if mario is jumping, change x and/or y values accordingly
        if self.jumpLeft or self.jumpRight or self.jumpStill:

            # keeps track of how many jumps
            self.jumpCount = self.jumpCount + 1

            # changes y coordinates
            self.marioY = self.marioY + self.addJump

            # when jumpCount is 7, make mario come back down by change the number he goes up/down by
            if self.jumpCount == 7:
                self.addJump = 7

            # if jumpCount is 14, mario has come back down
            if self.jumpCount == 14:

                # if mario jumped over a barrel, add 100 to the score
                if self.jumpPoint == 1:
                    self.score = self.score + 100

                # if mario was facing right, change the image back to him facing right, and change mario's Y value if he had jumpped over some inclines
                if self.direction == "right":
                    self.marioImage = self.marioRight
                    self.marioY = self.marioY - self.move * self.inclineCount
                # else mario was facing left, change the image back to him facing left, and change mario's Y value if he had jumpped over some inclines
                else:
                    self.marioImage = self.marioLeft
                    self.marioY = self.marioY + self.move * self.inclineCount

                # reseting variables
                self.addJump = -7
                self.jumpCount = 0
                self.jumpPoint = 0
                self.inclineCount = 0

                self.jumpLeft = False
                self.jumpRight = False
                self.jumpStill = False

            # if mario has reached a boundary on the sides, don't add to x values
            if self.marioX != 60 and self.marioX != 710 and (self.marioX != 320 or self.marioY >= 232):
                # checks how many inclines mario jumped over and whether to move up or down when mario lands
                self.move = self.incline(self.marioY, self.marioX, self.direction, "mario")

                # if mario is jumping left and he can move left, minus 5 to his x coordinates
                if self.jumpLeft and self.moveLeft:
                    self.marioX = self.marioX - 5
                # if mario is jumping right and he can move right, add 5 to his x coorinates
                elif self.jumpRight and self.moveRight:
                    self.marioX = self.marioX + 5

            # goes through all the barrels
            for i in range(0, len(self.barrelX)):
                # checks if mario has jumped over a barrel, if so, there is one point will be added if he completes the jump
                if self.marioX >= self.barrelX[i] and self.marioX <= self.barrelX[i] + 28 and self.marioY <= self.barrelY[i] - 23 and self.marioY >= \
                        self.barrelY[i] - 65:
                    self.jumpPoint = 1

        # scoreWin is false, keep the barrels rolling
        if self.scoreWin == False:

            # goes through all the barrels
            for i in range(0, len(self.barrelPic)):
                # if the barrel reaches the end of the structure, make the barrel disappear off the screen
                if self.barrelX[i] <= 31:
                    self.barrelX[i] = -30
                    self.barrelY[i] = -30

                # if the barrel is not falling, check to see if it is
                if self.fall[i] == False:
                    self.barrelLeft[i], self.barrelRight[i] = self.boundaries(self.barrelX[i], self.barrelY[i] - 15)

                    # reset variable if the barrel has hit a platform and can't move either left or right
                    if self.barrelLeft[i] == False or self.barrelRight[i] == False:
                        self.fall[i] = True

                # checks which platform the barrel is on to determine which direction it's going
                if (self.barrelY[i] <= 255 and self.barrelY[i] >= 243) or (self.barrelY[i] <= 452 and self.barrelY[i] >= 415) or (
                        self.barrelY[i] <= 648 and self.barrelY[i] >= 611):
                    self.barrelDirection[i] = "right"

                elif (self.barrelY[i] <= 353 and self.barrelY[i] >= 317) or (self.barrelY[i] <= 550 and self.barrelY[i] >= 513) or (
                        self.barrelY[i] <= 731 and self.barrelY[i] >= 709):
                    self.barrelDirection[i] = "left"

                # if the barrel is not on a ladder it is either rolling or falling
                if self.barrelPic[i] != self.barrelDown:

                    # if the barrel is not falling, it is rolling left or right
                    if self.fall[i] == False:

                        if self.barrelDirection[i] == "right":
                            self.barrelX[i] = self.barrelX[i] + 10
                        else:
                            self.barrelX[i] = self.barrelX[i] - 10

                        # checks if the barrel needs to incline up/down and changes the value in the function
                        self.barrelY[i] = self.incline(self.barrelY[i] - 11, self.barrelX[i], self.barrelDirection[i], "barrel")
                        self.barrelY[i] = self.barrelY[i] + 11
                        # subtracted 11 then added it back so that in the function, the values that the functions checks with the y value can be used for both the barrel and mario

                    # else the barrel is in the process of falling
                    else:
                        # add one to keep track of how long it has fallen
                        self.fallCount[i] = self.fallCount[i] + 1

                        # if the barrel is falling on the left side, x is being subtracted by 5
                        if self.barrelLeft[i] == False:
                            self.barrelX[i] = self.barrelX[i] - 5

                        # if it's falling from the right x is being added by 5
                        elif self.barrelRight[i] == False:
                            self.barrelX[i] = self.barrelX[i] + 5

                        # changing y by 7 each time
                        self.barrelY[i] = self.barrelY[i] + 7

                        # if the count has reached 8, stop falling and reset the values for the next time
                        if self.fallCount[i] == 8:
                            # adjust to make sure it lands on platform right
                            self.barrelY[i] = self.barrelY[i] + 6

                            # resetting variables
                            self.fallCount[i] = 0
                            self.fall[i] = False
                            self.barrelLeft[i] = True
                            self.barrelRight[i] = True

                    # changes the picture of the barrel each time
                    # if the barrelPic is at index 3, change it to at index 0
                    if self.barrelPic[i] == self.barrelSequence[3]:
                        self.barrelPic[i] = self.barrelSequence[0]

                    # else change it to the next number in the list
                    else:
                        for j in range(0, len(self.barrelSequence) - 1):
                            if self.barrelPic[i] == self.barrelSequence[j]:
                                self.barrelPic[i] = self.barrelSequence[j + 1]

                # if the barrelPic[i] is barrel down, the barrel is going down a ladder and add 10 to the y value each time
                else:
                    self.barrelY[i] = self.barrelY[i] + 10

                # goes through all the ladder coordinates for the barrels
                for j in range(0, len(self.barrelLadderX)):
                    # if the barrel's x and y coordinates are same as both barrelLadderX[j] and barrelLadderY[j], respectively, use a random number to choose whether the barrel should go down it or not
                    if self.barrelX[i] == self.barrelLadderX[j] and self.barrelY[i] == self.barrelLadderY1[j]:
                        self.barrelChoice = random.randint(0, 1)

                        # if the random number that was picked is 0, the barrel image and coordinates will be reset
                        if self.barrelChoice == 0:
                            self.barrelPic[i] = self.barrelDown

                            # adjust a bit because the barrel going down is wider than the other barrel images
                            self.barrelX[i] = self.barrelX[i] - 2

                    # if the barrel has reached the end of a ladder, reset the variables back
                    if self.barrelX[i] + 2 == self.barrelLadderX[j] and self.barrelY[i] == self.barrelLadderY2[j]:
                        self.barrelPic[i] = self.barrelSequence[0]
                        self.barrelX[i] = self.barrelX[i] + 2

                        # this makes sure that when it comes down it lands properly on the platform instead of 5 pixels too high, as the barrels move 10 pixels at a time
                        self.barrelY[i] = self.barrelY[i] + self.barrelAdjust[j]

            # if throwBarrel is false, get a random number to decide whether or not DK will throw another barrel
            if self.throwBarrel == False:
                # after each level the range will be smaller, meaning a higher chance of throwing barrels
                self.dkChoice = random.randint(0, 50 - self.difficulty)

                # if the number is 0, reset variables to throw the barrel
                if self.dkChoice == 0:
                    self.dkImage = self.dkLeft
                    self.throwBarrel = True
                # else, don't throw any barrels
                else:
                    self.dkImage = self.dkForward
                    self.throwBarrel = False

            # if throwBarrel is true, go through these changes
            if self.throwBarrel:

                # add to give DK some time to get barrel
                self.throwCountdown = self.throwCountdown + 1

                # if throwCountdown is 20, create a new barrel
                if self.throwCountdown == 20:
                    # reset variable
                    self.dkImage = self.dkRight

                    # declaring new barrel information
                    self.barrelX.append(250)
                    self.barrelY.append(243)
                    self.barrelDirection.append("right")
                    self.barrelPic.append(self.barrel1)
                    self.fall.append(False)
                    self.fallCount.append(0)
                    self.barrelLeft.append(True)
                    self.barrelRight.append(True)

                # if throwCountdown reaches 40, reset variables to when DK wasn't throwing
                if self.throwCountdown == 40:
                    self.throwCountdown = 0
                    self.dkImage = self.dkForward
                    self.throwBarrel = False

    # else, mario gets hit, start the death sequences


    def update_intro(self):
        if self.pressed == True and self.climbDone == False:
            # if he has just started, add to the level number
            if self.dkClimb == 0:
                self.levelNum = self.levelNum + 1

            # if DK has climbed 390 pixels, delay the program
            if self.dkClimb == 390:
                pygame.time.delay(500)

            # if DK has reached 560 pixels and over, reset the climbCount faster to make it look like he's jumping
            if self.dkClimb >= 560:
                self.climbCount = -20

            # DK hasn't reached 510 again on the way down from his jumping, keep adding to dkClimb
            if self.dkClimb != 510 or self.climbCount != -20:
                self.dkClimb = self.dkClimb + self.climbCount

            # else DK has finished climbing and the variable is re-set
            else:
                self.climbDone = True


        # if DK has finished climbing but the intro is not done yet, move on to DK jumping
        elif self.climbDone and self.introDone == False:
            # if the platNum is less than or equal to 6, DK is still jumping
            if self.platNum <= 6:
                # if dkJumpY is 152, reset which way he's jumping to start going down
                if self.dkJumpY == 152:
                    self.dkJumpYNum = 10

                # if dkJumpY is 172, reset which way he's jumping to start going up
                if self.dkJumpY == 172:
                    self.dkJumpYNum = -10

                    # change the platNum to change the background image so that a platform "falls"
                    self.platNum = self.platNum + 1

                # move DK to the left 12 pixels
                self.dkJumpX = self.dkJumpX - 12

                # if platNum is not 6, keep jumping/changing the y coordinates
                if self.platNum != 6:
                    self.dkJumpY = self.dkJumpY + self.dkJumpYNum

                else:
                    self.introDone = True
                    self.startOutput = True
                    self.startDone = True
                    pygame.time.delay(1000)

    def highScore(self):
        return self.score

    # collide - checks whether or not mario has collided into a barrel
    # @param: none
    # @return: hit(boolean)
    def collide(self):
        delete = []
        # goes through all the barrels
        for i in range(0, len(self.barrelX)):
            # if mario's image touches the barrels image anywhere, hit is True
            if self.marioX + 20 >= self.barrelX[i] and self.marioX <= self.barrelX[i] + 26 and self.marioY + 30 >= self.barrelY[i] and self.marioY <= \
                    self.barrelY[i] + 20:
                self.hit = True
                delete.append(i)

        for i in delete:
            del self.barrelX[i]
            del self.barrelY[i]
            del self.barrelPic[i]

        return self.hit

    # ladderCheck - checks whether or not there is a ladder at mario's location
    # @param: none
    # @return: upLadder(boolean), downLadder(boolean), moveSides(boolean)
    def ladderCheck(self):


        # declares variables
        upLadder = False
        downLadder = False
        moveSides = True

        # goes through all the ladders
        for i in range(0, len(self.ladderX1)):
            # if mario is in range of a ladder, he can move up, down, and to the sides
            if self.marioX >= self.ladderX1[i] and self.marioX <= self.ladderX2[i] and self.marioY >= self.ladderY1[i] and self.marioY <= self.ladderY2[i]:
                downLadder = True
                upLadder = True
                moveSides = False

                # if mario is at the top of a ladder, he can't move up further
                if self.marioY == self.ladderY1[i]:
                    upLadder = False

                    # if the ladder isn't broken going up, he can move to the sides when at the top
                    if self.fullLadderUp[i]:
                        moveSides = True

                        # if mario is at the bottom of the ladder, he can't move down further
                if self.marioY == self.ladderY2[i]:
                    downLadder = False

                    # if the ladder isn't broken going down, he can move to the sides when at the bottom
                    if self.fullLadderDown[i]:
                        moveSides = True

            # break out of the loop to stop checking for which ladder mario because the computer has already found it
            if upLadder or downLadder:
                break

        return upLadder, downLadder, moveSides

    # incline - moves Mario up so that he can go on an incline when walking/jumping on the platform
    # @param: y(int), x(int), direction(str), objectt(str)
    # @return: y(int) or move(int)
    def incline(self,y, x, direction, objectt):

        # lines 344 to 371 checks which platform the object is on and then declares the range where the object inclines and how much it moves vertically when going right on a inclined part

        # if the object is on the bottom platform
        if y <= 720 and y >= 657:
            startNum = 6
            endNum = len(self.platInclineX) - 1
            move = 3

        # if object is on the second or fourth platform
        elif (y <= 638 and y >= 553) or (y >= 353 and y <= 438):
            startNum = 0
            endNum = len(self.platInclineX) - 2
            move = -3

        # if object is on the thrid or fifth platform
        elif (y <= 541 and y >= 456) or (y <= 341 and y >= 256):
            startNum = 1
            endNum = len(self.platInclineX) - 1
            move = 3

        # if object is on the top platform
        elif y <= 245 and y >= 149:
            startNum = 8
            endNum = len(self.platInclineX) - 2
            move = -3

        # if not on a platform (on a ladder)
        else:
            startNum = 0
            endNum = 0
            move = 0

        # goes through the platIncline list, with a range of different numbers depending on which platform the object is on
        for i in range(startNum, endNum):

            # if the object has the same x as one of the x incline spot, the object will incline up or down
            if x == self.platInclineX[i]:

                # if the object is mario and he is jumping left or right, keep track of how many inclines he has passed while jumping
                if (self.jumpLeft or self.jumpRight) and objectt == "mario":
                    self.inclineCount = self.inclineCount + 1

                    # else find out which direction he is moving
                else:
                    # if it's right, minus move from y
                    if direction == "right":
                        y = y - move
                    # if its left, add move to y
                    elif direction == "left":
                        y = y + move

        # returns move if the function is for mario when jumping
        if (self.jumpLeft or self.jumpRight) and objectt == "mario":
            return move
        # else return the new y value
        else:
            return y

    # boundaries - checks all of Mario's, the barrels boundaries
    # @param: none
    # @return: left(boolean), right(boolean)
    def boundaries(self,x, y):
        # declare variables
        left = True
        right = True

        # if x is in that range, mario has reached a possible boundary to the left of him
        if x <= 105 and x >= 96:
            # goes through the y coordinate of the left boundaries
            for i in range(0, len(self.leftBoundariesY)):

                # if mario is in that range of the y boundary too, left is False and mario can't move left
                if y <= self.leftBoundariesY[i] and y >= self.leftBoundariesY[i] - 49:
                    left = False

        # if x is in that range, mario has reached a possible boundary to the right of him
        elif x >= 660 and x <= 669:
            # goes through the y coordinate of the right boundaries
            for i in range(0, len(self.rightBoundariesY)):

                # if mario is in that range of the y boundary too, right is False and mario can't move right
                if y <= self.rightBoundariesY[i] and y >= self.rightBoundariesY[i] - 49:
                    right = False

        return left, right

    # introScene - the start scene of the game
    # @param: none
    # @return: none
    def introScene(self,screen):
        # if DK has climbed less than 390 pixels, blit the background with the ladder
        if self.dkClimb <= 390:
            screen.blit(self.withLadder, (48, 0))

            # images will switch to make it look like DK is moving
            # if dkClimb is divisble by 30, blit the first climb image
            if self.dkClimb % 30 == 0:
                screen.blit(self.dkUp2, (350, 660 - self.dkClimb))

            # else blit the other climb image
            else:
                screen.blit(self.dkUp1, (370, 660 - self.dkClimb))

        # if DK has climbed for between 390 and 580 pixels, blit platform0 and keep dk's image as dkUp2
        elif self.dkClimb > 390 and self.dkClimb <= 580:
            screen.blit(self.platform0, (55, 9))
            screen.blit(self.dkUp2, (350, 660 - self.dkClimb))

        # if DK is done climbing, blit the falling platforms beams, Pauline and DK jumping
        if self.climbDone:
            screen.blit(self.platforms[self.platNum], (self.platformsX[self.platNum], self.platformsY[self.platNum]))
            self.pauline(self.paulineStill,screen)
            screen.blit(self.dkForward, (self.dkJumpX, self.dkJumpY))

    # startScreen - outputs the start screen
    # @param: none
    # @return: none
    def startScreen(self,screen):
        # blit image
        screen.blit(self.start, (48, 0))

    # backgroud - outputs the level and barrel stack
    # @param: none
    # @return: none
    def background(self,screen):
        # blit images
        screen.blit(self.level, (31, -14))
        screen.blit(self.barrelStack, (60, 188))

    # dk - outputs DK onto screen
    # @param: none
    # @return: none
    def dk(self,screen):
        # blit image
        screen.blit(self.dkImage, (130, 176))

    # mario - outputs Mario onto screen
    # @param: none
    # @return: none
    def mario(self,screen):
        # blit image
        screen.blit(self.marioImage, (self.marioX, self.marioY))

    # pauline - outputs pauline on to screen
    # @param: paulinePic(image)
    # @return: none
    def pauline(self,paulinePic,screen):
        # blit image
        screen.blit(paulinePic, (335, 133))

    # barrels - blit all the barrels onto the screen
    # @param: none
    # @return: none
    def barrel(self,screen):
        # goes through all the barrels to find each barrel information so it can blit it
        for i in range(0, len(self.barrelPic)):
            screen.blit(self.barrelPic[i], (self.barrelX[i], self.barrelY[i]))

    # lives - blit visual representation of how many lives Mario has left
    # @param: none
    # @return: none
    def marioLives(self,screen):
        # goes through all the lives you have left
        for i in range(0, self.lives):
            # blit images, adding 20 to the y each time you run the loop
            screen.blit(self.life, (60 + i * 20, 100))

    # levelNumber - blit the level number
    # @param: none
    # @return: none
    def levelNumber(self, screen):
        # goes through all the blue numbers
        for i in range(0, len(self.blueNumbers)):
            # if the ten's digit is equal to i, blit the image for the number
            if self.levelNum / 10 == i:
                screen.blit(self.blueNumbers[i], (611, 86))
            # if the ones's digit is equal to i, blit the image for the number
            if self.levelNum % 10 == i:
                screen.blit(self.blueNumbers[i], (635, 86))

    # playersScores - blit the scores
    # @param: scoreType(int), scoreX(int), scoreY(int)
    # @return: none
    def playersScores(self,scoreType, scoreX, scoreY,screen):

        # declares variables
        tempScore = str(scoreType)
        numOfZero = 6 - len(tempScore)

        # goes through to blit all the zeros needed in front of the score
        for i in range(0, numOfZero):
            screen.blit(self.whiteNumbers[0], (scoreX, scoreY))

            # add 24 to space the number out each time
            scoreX = scoreX + 24

        # goes through each digit/number in the string
        for i in range(0, len(tempScore)):
            # goes through the numbers 0 to 10
            for j in range(0, 10):

                # change tempScore[i] to integer to compare it with j
                # if they are equal, output the coressponding number image
                if int(tempScore[i]) == j:
                    screen.blit(self.whiteNumbers[j], (scoreX, scoreY))

                    # add 24 to space the number out each time
                    scoreX = scoreX + 24

    # win - images outputed when you complete a level
    # @param: none
    # @return: none
    def win(self,screen):

        # blit images
        mixer.music.stop()
        self.background(screen)
        screen.blit(self.marioLeft, (440, 150))

        # if DK has climbed less than 30 pixels, blit Pauline with a full heart
        if self.dkClimb <= 30:
            self.pauline(self.paulineStill,screen)
            screen.blit(self.fullHeart, (386, 130))
        # else just blit a broken heart
        else:
            screen.blit(self.brokenHeart, (387, 130))

        # if the game is not won, switch between two images to blit
        if self.winGame == False:
            if self.dkClimb % 30 == 0:
                screen.blit(self.dkImage1, (240 - self.moveOver1, 160 - self.dkClimb))
            else:
                screen.blit(self.dkImage2, (240 - self.moveOver2, 160 - self.dkClimb))

        # else just blit DK
        else:
            self.dk(screen)

    # end - shows end of the game
    # @param: endScreen(image)
    # @return: none
    def end(self,endScreen,screen):

        # blit image
        screen.blit(endScreen, (0, 30))

        # if the bottom option is selected, blit the icon next to the bottom option
        if self.option == "bottom":
            screen.blit(self.selectIcon, (270, 640))

        # else blit it next to the top option
        else:
            screen.blit(self.selectIcon, (270, 575))

    # confetti - outputs confetti on the screen
    # @param: none
    # @return: none
    def confetti(self,screen):

        # goes through all 400 confetti pieces
        for i in range(0, 400):
            # blit image with the correct confetti info for each piece
            pygame.draw.circle(screen, self.confettiColour[i], (self.confettiX[i], self.confettiY[i]), self.confettiRadius[i], 0)

            # @redraw_screen - function that redraws the screen

    def redraw_screen(self,screen):

        # filling colour of screen
        screen.fill(BLACK)

        # drawing commands

        # if game is done, output end screen and user and high score
        if self.gameDone:
            # calls drawing fucntions
            self.end(self.gameOverScreen,screen)
            self.playersScores(self.score, 388, 387,screen)
            self.playersScores(self.highestScore, 485, 445,screen)

        # if winGame is True, go to the win game sequences
        elif self.winGame:
            # if this is true, blit the images to show the moment DK is defeated
            if self.winGameSceneOutput:
                # calls drawing fucntions
                self.win(screen)
                self.marioLives(screen)

                self.levelNumber(screen)
                self.playersScores(self.score, 88, 40,screen)
                self.playersScores(self.highestScore, 327, 40,screen)

            # if this is true, output the win game menu with confetti
            elif self.winGameSceneDone:
                # calls drawing fucntions
                self.end(self.winScreen,screen)
                self.confetti(screen)
                self.playersScores(self.score, 388, 387,screen)
                self.playersScores(self.highestScore, 485, 445,screen)
                self.done = True
                self.next = c.GAME_OVER
                setup.SCREEN = pygame.display.set_mode((800, 600))
                setup.SCREEN_RECT = setup.SCREEN.get_rect()

        # else the user has not won or lost the game yet
        else:
            # if pressed is false, the title screen is being blited
            if self.pressed == False:
                screen.blit(self.title, (54, 18))

            # if pressed is true and introDone, blit the intro sequence
            elif self.pressed and self.introDone == False:
                # calls drawing fucntions
                if not mixer.music.get_busy(): self.sound("Intro")
                self.introScene(screen)
                self.marioLives(screen)
                self.clock.tick(12)

            # if intro is done and the game hasn't started yet, blit the start screen
            elif self.introDone == True and self.gameStart == False:
                # calls drawing fucntions
                self.startScreen(screen)
                self.marioLives(screen)

                # establishing the start is done by resetting the variables
                self.startOutput = True
                self.startDone = True

            # if the game has started and the level is not won or mario has died, blit the normal game play images
            elif (self.gameStart and self.winLevel == False) or self.deathScene:
                # calls drawing fucntions
                if not self.hit:
                    if not mixer.music.get_busy(): self.sound("Background")
                self.background(screen)
                self.dk(screen)
                self.mario(screen)
                self.pauline(self.paulineHelp,screen)
                self.marioLives(screen)

                # blit barrels if scoreWin and deathScene is false
                if self.scoreWin == False and self.deathScene == False:
                    self.barrel(screen)

            # if user wins the level output winning sequence
            elif self.winLevel:
                # calls drawing fucntions
                self.win(screen)
                self.marioLives(screen)

            # calls drawing fucntions
            self.levelNumber(screen)
            self.playersScores(self.score, 88, 40,screen)
            self.playersScores(self.highestScore, 327, 40,screen)

        # updating
        pygame.display.update()


#Define Colour Values (R,G,B)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTBLUE = (0, 200, 255)
YELLOW = (255, 255, 0)
PURPLE = (170, 0, 225)
colours = [GREEN, RED, LIGHTBLUE, YELLOW, PURPLE]

#declaring global variables

path_g = "resources/graphics/"
path_s = 'resources/sound/'
path_m = 'resources/music/'

