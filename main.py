from random import randint
from math import sqrt, fabs
import pygame
import sys

pygame.init()
pygame.display.set_caption('Lines v2')

# pygame constants
display = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

background = pygame.Surface(display.get_size())
background.fill((0,0,0))

font = pygame.font.SysFont('AmericanTypewriter', 18)

# constants
fps = 32

class Dots:
	def __init__(self, display):
		self.display = display
		self.name = font.render('Code and design by Elison Crum', True, (255, 255, 255))
		self.display_size = display.get_size()
		self.shape = 0
		self.new_dots()
		self.jitter = (-1, 1)

		# todo, possibly make cleaner
		self.color_value = {
			1:(255, 0, 0),
			2:(0, 255, 0),
			3:(0, 0, 255),
			4:(255, 255, 255),
			5:(125, 125, 125),
			7:(0, 0, 0)
		}
		self.color_names = ['Red', 'Green', 'Blue', 'White', 'Gray', 'Random', 'None']
		self.color_num = 1

	# mainly for clear code
	def display_all(self):
		self.display_lines()
		self.display_dots()

		self.update_dots()
		self.display_text()

	# displays text
	def display_text(self):
		self.display.blit(self.name, (5, 582))
		range_text = font.render('Range : {}'.format(self.range), True, (255, 255, 255))
		self.display.blit(range_text, (10, 10))
		color_text = font.render('Color : {}'.format(self.color_names[self.color_num - 1]), True, (255, 255, 255))
		self.display.blit(color_text, (510, 582))

	# clears self.coords and make a new list of random coords
	def new_dots(self):
		self.range = randint(30, 90)

		rand_num = randint(25, 250)
		tmp = [ [0, 0] ]

		if self.shape == 1:
			count = 0
			while count < rand_num:
				x, y = randint(0, 600), randint(0, 600)
				dist = sqrt(fabs(x - 300) ** 2 + fabs(y - 300) ** 2)

				if dist < 250:
					tmp.append([x, y])
					count += 1

		elif self.shape == 2:
			for x in range(rand_num):
				tmp.append([randint(100, 500), randint(100, 500)])

		else:
			for x in range(rand_num):
				tmp.append([randint(0, self.display_size[0]), (randint(0, self.display_size[1]))])

		self.coords = tmp

	# draws each dot as a circle
	def display_dots(self):
		[pygame.draw.circle(self.display, (255, 255, 255), coord, 1, 1) for coord in self.coords]

	# either returns solid color, or random color
	def get_color(self):
		if self.color_num == 6: return (randint(0,255), randint(0, 255), randint(0, 255))
		return self.color_value[self.color_num]

	# displays lines
	# if sqrt( |x1 + x2^2| + |y1 - y2 ^2| ) < range: draw line
	def display_lines(self):
		for x in self.coords:
			for y in self.coords:
				if sqrt(fabs((x[0] - y[0]) ** 2) + fabs((x[1] - y[1]) ** 2)) < self.range:
					pygame.draw.line(self.display, self.get_color(), x, y)

	# updates dots, specifically adds the jitter motion
	# ignores mouse pos dot
	def update_dots(self):
		self.coords[0] = list(pygame.mouse.get_pos())
		for x in range(1, len(self.coords)):
			self.coords[x][0] += randint(self.jitter[0], self.jitter[1])
			self.coords[x][1] += randint(self.jitter[0], self.jitter[1])

# calling Dots constructor
dots = Dots(display)

while True:
	for event in pygame.event.get():

		# main control flow
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		elif event.type == pygame.MOUSEBUTTONDOWN:
			dots.coords.append(list(pygame.mouse.get_pos()))

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				dots.range += 10

			elif event.key == pygame.K_DOWN:
				dots.range -= 10

			elif event.key == pygame.K_LEFT:
				dots.range -= 1

			elif event.key == pygame.K_RIGHT:
				dots.range += 1

			elif event.key == pygame.K_SPACE:
				dots.new_dots()

			elif event.key == pygame.K_c:
				dots.color_num += 1

			elif event.key == pygame.K_q:
				pygame.quit()
				sys.exit()

			elif event.key == pygame.K_p:
				if dots.jitter == (-1, 1): dots.jitter = (0, 0)
				else: dots.jitter = (-1, 1)

			elif event.key == pygame.K_s:
				dots.shape += 1

				if dots.shape > 2: dots.shape = 0

				dots.new_dots()

			elif event.key == pygame.K_DELETE:
				dots.coords = [ [0, 0] ]

			elif event.key == pygame.K_i:
				if dots.range == float('inf'): dots.range = randint(30, 90)
				else: dots.range = float('inf')


			# reset values, handling overflow errors
			if dots.color_num > 7: dots.color_num = 1
			if dots.range < 0: dots.range = 0

	# main tasks
	display.blit(background, (0,0))
	dots.display_all()

	pygame.display.flip()
	clock.tick()