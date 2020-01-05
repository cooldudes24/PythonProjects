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
YELLOW = (255, 255, 0)
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
		self.image = pygame.image.load(os.path.join(img_folder, "ship.png")).convert()
		self.image.set_colorkey(WHITE)
		#self.image = pygame.Surface((50, 40))
		#self.image.fill(BLACK)
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

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((30, 40))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.rect.y = random.randrange(1, 8)
		self.speedy = random.randrange(-3, 3)

	def update(self):
		#self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10, 20))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		# wreck it if it moves off the top of the screen
		if self.rect.bottom < 0:
			self.kill()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)

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
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()
	# Update
	all_sprites.update()
	# check if a bullet hits a mob
	hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
	for hit in hits:
		m = Mob()
		all_sprites.add(m)
		mobs.add(m)
	# check if a mob hit the player
	hits = pygame.sprite.spritecollide(player, mobs, False)
	if hits:
		running = False

	# Draw / render
	screen.fill(GREEN)
	all_sprites.draw(screen)
	# *after* drawing everything, flip the display
	pygame.display.flip()

pygame.quit()
