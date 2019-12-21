# Shmup game
import pygame
import random
import os

WIDTH = 480
HEIGHT = 600
FPS = 60
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

class Santa(pygame.sprite.Sprite):
    # sprite for the player
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join(img_folder, "cute santa.png")).convert()
		self.image.set_colorkey(GREEN)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH / 2, HEIGHT / 2)
		self.y_speed = 5

	def update(self):
		self.rect.x += 5
		self.rect.y += self.y_speed
		if self.rect.bottom > HEIGHT - 200:
			self.y_speed = -5
		if self.rect.top < 200:
			self.y_speed = 5
		if self.rect.left > WIDTH:
			self.rect.right = 0
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Awesome Shmup Game")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50, 40))
		self.image.fill(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0

	def update(self):
		self.speedx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -9
		if keystate[pygame.K_RIGHT]:
			self.speedx = 9
		self.rect.x += self.speedx
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

all_sprites = pygame.sprite.Group()
santa = Santa()
player = Player()
all_sprites.add(player)
# Game loop
running = True
while running:
	# keep loop running at the right speed
	clock.tick(FPS)
	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			running = False

	# Update
	all_sprites.update()
	# Draw / render
	screen.fill(GREEN)
	all_sprites.draw(screen)
	# *after* drawing everything, flip the display
	pygame.display.flip()

pygame.quit()
