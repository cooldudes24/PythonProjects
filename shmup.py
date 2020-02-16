# Shmup game
import pygame
import random
import os
from os import path

from pygame.sprite import Group

img_dir = path.join(path.dirname(__file__), 'img')

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

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cooldudes24 and Basherboy1 Shmup Game")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, False, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite): #Helllllllllllllllloooooooooooooooooooooooooooooooooooooooooo!
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = player_img
		self.image = pygame.transform.scale(player_img, (60, 48))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0

	def update(self):
		self.speedx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -5
		if keystate[pygame.K_RIGHT]:
			self.speedx = 5
		self.rect.x += self.speedx
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)


# By the power of MOBS! (REMEMBER TO WATCH VIDEO 5!)
class Mob(pygame.sprite.Sprite):
	def __init__(self) -> object:
		pygame.sprite.Sprite.__init__(self)
		self.image_orig = random.choice(meteor_images)
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width * .85 / 2)
		# pygame.draw.circle(self-image-whatever)
		# BlaBlaBlaBlaBlaBla!
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-150, -100)
		self.speedy = random.randrange(1, 8)
		self.speedx = random.randrange(-3, 3)
		self.rot = 0
		self.rot_speed = random.randrange(-8, 8)
		self.last_update = pygame.time.get_ticks()

	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			self.rot = (self.rot + self.rot_speed) % 360
			self.image = pygame.transform.rotate(self.image_orig, self.rot)

	def update(self):
		self.rotate()
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -70)
			# Supposed to be 40^^^^^^instead of 70
			self.speedy = random.randrange(1, 10)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x: object, y: object) -> object:
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		# kill if it moves off the top of the screen
		if self.rect.bottom < 0:
			self.kill()


# Load all game graphics
background = pygame.image.load(os.path.join(img_folder, "Background.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "Blue.png")).convert()
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserBlue.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_med1.png',
               'meteorBrown_med1.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png', ]
for img in meteor_list:
	meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

# self.image = pygame.image.load(os.path.join(img_folder, "meteorBrown.png"))

all_sprites: Group = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
# IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
for i in range(20):
	# IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	  m = Mob()
all_sprites.add(m)
mobs.add(m)

score = 0

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
	# check to see if a bullet hit a mob
	hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
	for hit in hits:
		hits += 50 - hit.radius
		m = Mob()
		all_sprites.add(m)
		mobs.add(m)

	# check to see if a mob hit a player
	hits = pygame.sprite.spritecollide(player, mobs, False)
	if hits:
		running = False

	# Draw / render
	screen.fill(GREEN)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 18, WIDTH / 2, 10)
	# *after* drawing everything, flip the display
	pygame.display.flip()

pygame.quit()
