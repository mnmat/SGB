import pygame, sys, random 

from data import setup, tools
from data import constants as c


class Flappy(tools._State):
	def __init__(self):
		tools._State.__init__(self)

	def startup(self, current_time, persist):
		"""Called when the State object is created"""
		self.game_info = persist
		self.persist = self.game_info
		self.game_info[c.CURRENT_TIME] = current_time
		self.game_info[c.LEVEL_STATE] = c.NOT_FROZEN
		self.game_info[c.MARIO_DEAD] = False
		setup.SCREEN = pygame.display.set_mode((512,1024))
		setup.SCREEN_RECT = setup.SCREEN.get_rect()
		self.state = c.NOT_FROZEN

		self.flap_sound = pygame.mixer.Sound('resources/sound/sfx_wing.wav')
		self.death_sound = pygame.mixer.Sound('resources/sound/sfx_hit.wav')
		self.score_sound = pygame.mixer.Sound('resources/sound/sfx_point.wav')
		self.score_sound_countdown = 100
		pygame.time.set_timer(pygame.USEREVENT+1, 1200)

		self.game_active = True
		self.collision = False
		self.victory = False
		self.score = 0
		self.high_score = 0
		self.gravity = 0.25

		self.moving_score_list = []
		self.game_font = pygame.font.Font('resources/fonts/04B_19.ttf',40)

		self.setup_background()
		self.setup_ground()
		self.setup_bird()
		self.setup_pipes()
		self.setup_gameover()
		self.setup_victory()

	def setup_background(self):
		self.background = pygame.image.load('resources/graphics/STP.png')
		self.background = pygame.transform.scale2x(self.background)

	def setup_ground(self):
		self.floor_surface = pygame.image.load('resources/graphics/base.png').convert()
		self.floor_surface = pygame.transform.scale2x(self.floor_surface)
		self.floor_x_pos = 0

	def setup_bird(self):
		self.bird_img = pygame.transform.scale2x(pygame.image.load('resources/graphics/julian-downflap.png').convert_alpha())
		self.bird_rect = self.bird_img.get_rect(center = (100,512))
		self.bird_movement = 0

	def setup_pipes(self):
		self.pipe_surface = pygame.image.load('resources/graphics/vines.png')
		self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)
		self.pipe_list = []
		self.pipe_height = [400, 600, 800]

	def setup_gameover(self):
		self.game_over_surface = pygame.transform.scale2x(pygame.image.load('resources/graphics/start_message.png').convert_alpha())
		self.game_over_rect = self.game_over_surface.get_rect(center=(288, 512))

	def setup_victory(self):
		self.victory_surface = pygame.transform.scale2x(pygame.image.load('resources/graphics/end_message.png').convert_alpha())
		self.victory_rect = self.victory_surface.get_rect(center=(288, 512))

	def update(self, surface, current_time):
		"""Updates Entire level using states.  Called by the control object"""
		self.game_info[c.CURRENT_TIME] = self.current_time = current_time
		self.handle_states()
		self.blit_everything(surface)
		#self.sound_manager.update(self.game_info, self.mario)


	def blit_everything(self,surface):
		"""Blit all sprites to the main surface"""
		if self.game_active == True:
			self.draw_background(surface)
			self.draw_floor(surface)
			self.draw_pipes(surface)
			self.score_display('main_game',surface)
			surface.blit(self.rotated_bird, self.bird_rect)
		else:
			if self.score < 9:
				self.update_score()
				surface.blit(self.game_over_surface, self.game_over_rect)
				self.score_display('game_over',surface)
			else:
				self.victory = True
				surface.blit(self.victory_surface, self.victory_rect)

	def event_loop(self):
		self.keys = []
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self.keys.append(event.key)
				# self.keys = pg.key.get_pressed()
				self.toggle_show_fps(event.key)
			elif event.type == pygame.USEREVENT+1:
				self.create_pipe()
			self.get_event(event)



	def handle_states(self):
		"""Updates the location of all sprites on the screen."""

		if self.game_active == True:
			self.bird_update()
			self.pipe_update()
			self.score_update()
			self.check_collision()
			self.floor_update()

		if self.game_active == False:
			self.game_update()

	def game_update(self):
		if self.victory == False:
			if tools.keybinding['space'] in self.keys and self.game_active == False and self.victory == False:
				self.game_active = True
				self.pipe_list.clear()
				self.bird_rect.center = (100, 512)
				self.bird_movement = 0
				self.score = 0
		if tools.keybinding['enter'] in self.keys and self.victory == True:
			self.next = c.GAME_OVER
			self.done = True
			setup.SCREEN = pygame.display.set_mode((800, 600))
			setup.SCREEN_RECT = setup.SCREEN.get_rect()

	def floor_update(self):
		self.floor_x_pos -= 1
		if self.floor_x_pos <= -576:
			self.floor_x_pos = 0


	def bird_update(self):
		if tools.keybinding['space'] in self.keys:
			self.bird_movement = 0
			self.bird_movement -= 12
			if self.flap_sound.get_num_channels() < 1:
				print(self.flap_sound.get_num_channels())
				self.flap_sound.play()


		self.bird_movement += self.gravity
		self.rotated_bird = self.rotate_bird()
		self.bird_rect.centery += self.bird_movement

	def pipe_update(self):
		self.move_pipes()
		self.remove_pipes()

	def score_update(self):
		self.score += 0.01
		self.score_sound_countdown -= 1
		if self.score_sound_countdown <= 0:
			self.score_sound.play()
			self.score_sound_countdown = 200/3

	def draw_floor(self,screen):
		screen.blit(self.floor_surface,(self.floor_x_pos,900))
		screen.blit(self.floor_surface,(self.floor_x_pos + 576,900))

	def draw_background(self,screen):
		screen.blit(self.background,(0,0))

	def create_pipe(self):
		random_pipe_pos = random.choice(self.pipe_height)
		bottom_pipe = self.pipe_surface.get_rect(midtop = (700,random_pipe_pos))
		top_pipe = self.pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
		self.pipe_list.extend((bottom_pipe,top_pipe))


	def move_pipes(self):
		for pipe in self.pipe_list:
			pipe.centerx -= 5

	def draw_pipes(self,screen):
		for pipe in self.pipe_list:
			if pipe.bottom >= 1024:
				screen.blit(self.pipe_surface,pipe)
			else:
				flip_pipe = pygame.transform.flip(self.pipe_surface,False,True)
				screen.blit(flip_pipe,pipe)

	def remove_pipes(self):
		for pipe in self.pipe_list:
			if pipe.centerx == -600:
				self.pipe_list.remove(pipe)

	def check_collision(self):
		for pipe in self.pipe_list:
			if self.bird_rect.colliderect(pipe):
				self.death_sound.play()
				self.game_active = False

		if self.bird_rect.top <= -100 or self.bird_rect.bottom >= 900:
			self.game_active =  False

	def rotate_bird(self):
		new_bird = pygame.transform.rotozoom(self.bird_img,-self.bird_movement * 3,1)
		return new_bird

	def score_display(self,game_state, screen):
		if game_state == 'main_game':
			score_surface = self.game_font.render(str(int(self.score)),True,(255,255,255))
			score_rect = score_surface.get_rect(center = (288,100))
			screen.blit(score_surface,score_rect)
		if game_state == 'game_over':
			score_surface = self.game_font.render(f'Score: {int(self.score)}' ,True,(255,255,255))
			score_rect = score_surface.get_rect(center = (288,100))
			screen.blit(score_surface,score_rect)

			high_score_surface = self.game_font.render(f'High score: {int(self.high_score)}',True,(255,255,255))
			high_score_rect = high_score_surface.get_rect(center = (288,850))
			screen.blit(high_score_surface,high_score_rect)

	def update_score(self):
		if self.score > self.high_score:
			self.high_score = self.score