import pygame,sys,random
from pygame.math import Vector2
from data import setup, tools
from data import constants as c
from .. components import info

class SNAKE():
	def __init__(self):
		self.cell_size = 40
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0,0)
		self.new_block = False

		self.head_up = pygame.image.load('resources/graphics/julian.png').convert_alpha()
		self.head_down = pygame.image.load('resources/graphics/julian.png').convert_alpha()
		self.head_right = pygame.image.load('resources/graphics/julian.png').convert_alpha()
		self.head_left = pygame.image.load('resources/graphics/julian.png').convert_alpha()
		
		self.tail_up = pygame.image.load('resources/graphics/julian.png').convert_alpha()
		self.tail_down = pygame.image.load('resources/graphics/julian.png').convert_alpha()
		self.tail_right = pygame.image.load('resources/graphics/julian.png').convert_alpha()
		self.tail_left = pygame.image.load('resources/graphics/julian.png').convert_alpha()

		self.body_vertical = pygame.image.load('resources/graphics/julian.png').convert_alpha()
		self.body_horizontal = pygame.image.load('resources/graphics/julian.png').convert_alpha()

		self.body_tr = pygame.image.load('resources/graphics/julian.png').convert_alpha()
		self.body_tl = pygame.image.load('resources/graphics/julian.png').convert_alpha()
		self.body_br = pygame.image.load('resources/graphics/julian.png').convert_alpha()
		self.body_bl = pygame.image.load('resources/graphics/julian.png').convert_alpha()
		self.crunch_sound = pygame.mixer.Sound('resources/sound/crunch.wav')



	def draw_snake(self,screen):
		self.update_head_graphics()
		self.update_tail_graphics()

		for index,block in enumerate(self.body):
			x_pos = int(block.x * self.cell_size)
			y_pos = int(block.y * self.cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,self.cell_size,self.cell_size)

			if index == 0:
				screen.blit(self.head,block_rect)
			elif index == len(self.body) - 1:
				screen.blit(self.tail,block_rect)
			else:
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:
					screen.blit(self.body_vertical,block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal,block_rect)
				else:
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(self.body_tl,block_rect)
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(self.body_bl,block_rect)
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(self.body_tr,block_rect)
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_br,block_rect)

	def update_head_graphics(self):
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1,0): self.head = self.head_left
		elif head_relation == Vector2(-1,0): self.head = self.head_right
		elif head_relation == Vector2(0,1): self.head = self.head_up
		elif head_relation == Vector2(0,-1): self.head = self.head_down

	def update_tail_graphics(self):
		tail_relation = self.body[-2] - self.body[-1]
		if tail_relation == Vector2(1,0): self.tail = self.tail_left
		elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
		elif tail_relation == Vector2(0,1): self.tail = self.tail_up
		elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

	def move_snake(self):
		if self.new_block == True:
			body_copy = self.body[:]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]
			self.new_block = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]

	def add_block(self):
		self.new_block = True

	def play_crunch_sound(self):
		self.crunch_sound.play()

	def reset(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0,0)



class Cake(tools._State):
	def __init__(self):
		tools._State.__init__(self)

	def startup(self, current_time,persist):
		self.game_info = persist
		self.persist = self.game_info
		self.game_info[c.CURRENT_TIME] = current_time
		self.game_info[c.LEVEL_STATE] = c.NOT_FROZEN
		self.game_info[c.MARIO_DEAD] = False

		self.state = c.NOT_FROZEN

		self.overhead_info_display = info.OverheadInfo(self.game_info, c.LEVEL)

		pygame.mixer.music.load('resources/music/Happy_Birthday.wav')
		pygame.mixer.music.play(-1)

		self.cell_size = 40
		self.cell_number = 20

		setup.SCREEN = pygame.display.set_mode((self.cell_number * self.cell_size, self.cell_number * self.cell_size))


		self.apple = pygame.image.load('resources/graphics/cake.png').convert_alpha()
		self.game_font = pygame.font.Font('resources/fonts/PoetsenOne-Regular.ttf', 25)

		pygame.time.set_timer(pygame.USEREVENT, 150)

		self.snake = SNAKE()
		self.setup_fruit()
		self.step = False

	def setup_fruit(self):
		self.randomize()

	def randomize(self):
		self.x = random.randint(0, self.cell_number - 1)
		self.y = random.randint(0, self.cell_number - 1)
		self.pos = Vector2(self.x, self.y)
		self.front_pos = Vector2(self.x, self.y)

	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.USEREVENT:
				self.step = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					if self.snake.direction.y != 1:
						self.snake.direction = Vector2(0, -1)
				if event.key == pygame.K_RIGHT:
					if self.snake.direction.x != -1:
						self.snake.direction = Vector2(1, 0)
				if event.key == pygame.K_DOWN:
					if self.snake.direction.y != -1:
						self.snake.direction = Vector2(0, 1)
				if event.key == pygame.K_LEFT:
					if self.snake.direction.x != 1:
						self.snake.direction = Vector2(-1, 0)

	def update(self,surface, current_time):
		self.game_info[c.CURRENT_TIME] = self.current_time = current_time
		if self.step == True:
			self.handle_states()
			self.draw_elements(surface)
			self.step = False

	def handle_states(self):
		self.snake.move_snake()
		self.check_collision()
		self.check_fail()

	def draw_elements(self,surface):
		surface.fill((175, 215, 70))
		self.draw_grass(surface)
		self.draw_fruit(surface)
		self.snake.draw_snake(surface)
		self.draw_score(surface)


	def check_collision(self):

		front = self.pos + Vector2(1,0)

		if front == self.snake.body[0]:
			self.game_over()
		elif self.pos == self.snake.body[0]:
			self.randomize()
			self.snake.add_block()
			self.snake.play_crunch_sound()

		for block in self.snake.body[1:]:
			if block == self.pos:
				self.randomize()

	def check_fail(self):
		if not 0 <= self.snake.body[0].x < self.cell_number or not 0 <= self.snake.body[0].y < self.cell_number:
			self.game_over()

		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				self.game_over()
		
	def game_over(self):
		if len(self.snake.body) < 29:
			self.snake.reset()
		else:
			pygame.mixer.music.fadeout(1000)
			self.next = c.VICTORY
			self.done = True
			setup.SCREEN = pygame.display.set_mode((800, 600))
			setup.SCREEN_RECT = setup.SCREEN.get_rect()

	def draw_fruit(self,screen):
		fruit_rect = pygame.Rect(int(self.pos.x * self.cell_size),int(self.pos.y * self.cell_size),self.cell_size,self.cell_size)
		screen.blit(self.apple,fruit_rect)
		#pygame.draw.rect(screen,(126,166,114),fruit_rect)

	def draw_grass(self,screen):
		grass_color = (167,209,61)
		for row in range(self.cell_number):
			if row % 2 == 0: 
				for col in range(self.cell_number):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * self.cell_size,row * self.cell_size,self.cell_size,self.cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)
			else:
				for col in range(self.cell_number):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * self.cell_size,row * self.cell_size,self.cell_size,self.cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)			

	def draw_score(self,screen):
		score_text = str(len(self.snake.body) - 3)
		score_surface = self.game_font.render(score_text,True,(56,74,12))
		score_x = int(self.cell_size * self.cell_number - 60)
		score_y = int(self.cell_size * self.cell_number - 40)
		score_rect = score_surface.get_rect(center = (score_x,score_y))
		apple_rect = self.apple.get_rect(midright = (score_rect.left,score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

		pygame.draw.rect(screen,(167,209,61),bg_rect)
		screen.blit(score_surface,score_rect)
		screen.blit(self.apple,apple_rect)
		pygame.draw.rect(screen,(56,74,12),bg_rect,2)



