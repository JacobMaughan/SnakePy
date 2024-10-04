from sys import exit as sys_exit
from os.path import join as os_join
from os import getcwd as os_getcwd
from random import randint

import pygame, pygame.freetype

class Game:
	def __init__(self):
		# Initilizing backend variables & modules
		pygame.init()
		self.display = pygame.display.set_mode((600, 600))
		pygame.display.set_caption('SnakePy')
		self.font = pygame.freetype.SysFont('Arial', 30)
		self.clock = pygame.time.Clock()
		self.dt = 0
		self.counter = 0
		self.game_state = 0

		# Load or Create highscore file and initialize highscore variables
		try:
			self.highscore_file = open(os_join(os_getcwd(), 'highscore'), 'r+')
			self.highscore = bytes.fromhex(self.highscore_file.read()).decode('utf-8').split('.')[1]
		except:
			highscore_file = open(os_join(os_getcwd(), 'highscore'), 'w+')
			highscore_file.close()
			self.highscore_file = open(os_join(os_getcwd(), 'highscore'), 'r+')
			self.highscore = ''
		self.updated_highscore = False

		# Initializing frontend variables
		self.snake = []
		self.vel_x = 0
		self.vel_y = 0
		self.speed = 0
		self.apple = []
		self.score = 0
		self.last_increased_score = 0

	def update(self):
		self.counter += self.dt
		if self.counter >= 1 / self.speed:
			self.counter = 0
			self.handle_events()

			if self.game_state == 0:
				if self.vel_x != 0 or self.vel_y != 0:
					self.move_snake()
				self.handle_collisions()

			elif self.game_state == 1:
				if self.highscore != '':
					if int(self.highscore) < self.score:
						self.update_highscore()
				else:
					self.update_highscore()

	def render(self):
		self.display.fill((0, 0, 0))

		if self.game_state == 0:
			for body_part in self.snake:
				pygame.draw.rect(self.display, (0, 255, 0), (body_part[0], body_part[1], 20, 20))
			pygame.draw.rect(self.display, (255, 0, 0), (self.apple[0], self.apple[1], 20, 20))
			self.font.render_to(self.display, (20, 10), str(self.score), (255, 255, 255))

		elif self.game_state == 1:
			if self.highscore != '':
				if int(self.highscore) >= self.score and not self.updated_highscore:
					self.font.render_to(self.display, (100, 200), 'Final Score: ' + str(self.score), (255, 255, 255))
					self.font.render_to(self.display, (110, 300), 'Highscore: ' + self.highscore, (255, 255, 255))
				else:
					self.font.render_to(self.display, (90, 200), 'New Highscore: ' + str(self.score), (255, 255, 255))
			else:
				self.font.render_to(self.display, (90, 200), 'New Highscore: ' + str(self.score), (255, 255, 255))

		pygame.display.flip()

	def run(self):
		self.new_game()
		while True:
			self.update()
			self.render()
			self.dt = self.clock.tick(60) / 1000

	def handle_collisions(self):
		for i in range(len(self.snake), 1, -1):
			if self.snake[0][0] == self.snake[i - 1][0] and self.snake[0][1] == self.snake[i - 1][1]:
				self.updated_highscore = False
				self.game_state = 1
		if self.snake[0][0] < 0 or self.snake[0][0] == 600 or self.snake[0][1] < 0 or self.snake[0][1] == 600:
			self.updated_highscore = False
			self.game_state = 1
		if self.snake[0][0] == self.apple[0] and self.snake[0][1] == self.apple[1]:
			self.add_snake()
			self.add_apple()
			self.add_score()

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.highscore_file.close()
				pygame.quit()
				sys_exit()
			if event.type == pygame.KEYDOWN:
				if self.game_state == 0:
					if event.key == pygame.key.key_code('w'):
						if self.vel_y == 0:
							self.vel_y = -1
							self.vel_x = 0
					elif event.key == pygame.key.key_code('s'):
						if self.vel_y == 0:
							self.vel_y = 1
							self.vel_x = 0
					elif event.key == pygame.key.key_code('a'):
						if self.vel_x == 0:
							self.vel_x = -1
							self.vel_y = 0
					elif event.key == pygame.key.key_code('d'):
						if self.vel_x == 0:
							self.vel_x = 1
							self.vel_y = 0
				elif self.game_state == 1:
					if event.key == pygame.key.key_code('space'):
						self.game_state = 0
						self.new_game()

	def move_snake(self):
		for i in range(len(self.snake), 1, -1):
			self.snake[i - 1][0] = self.snake[i - 2][0]
			self.snake[i - 1][1] = self.snake[i - 2][1]
		self.snake[0][0] += self.vel_x * 20
		self.snake[0][1] += self.vel_y * 20

	def new_game(self):
		self.snake = [[15 * 20, 15 * 20]]
		self.vel_x = 0
		self.vel_y = 0
		self.speed = 5
		self.add_apple()
		self.score = 0
		self.last_increased_score = 0

	def add_apple(self):
		self.apple = [ randint(0, 29) * 20, randint(0, 29) * 20 ]

	def add_snake(self):
		if self.snake:
			self.snake.append([ self.snake[len(self.snake) - 1][0], self.snake[len(self.snake) - 1][1] ])

	def add_score(self):
		self.score += 1
		if self.score == self.last_increased_score + 10:
			self.last_increased_score = self.score
			self.speed += 1

	def update_highscore(self):
		if not self.updated_highscore:
			self.highscore_file.seek(0)
			self.highscore_file.write(('jacob.' + str(self.score) + '.maughan').encode('utf-8').hex())
			self.highscore_file.truncate()
			self.highscore = str(self.score)
			self.updated_highscore = True

if __name__ == '__main__':
	game = Game()
	game.run()