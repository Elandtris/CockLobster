import pygame
import time
import os
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

mouse_pressed = False

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Cock Lobster")

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
#BIRD_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs","cocklob1.png")), (200, 200)), pygame.transform.scale(pygame.image.load(os.path.join("imgs","cocklob2.png")), (200, 200)), pygame.transform.scale(pygame.image.load(os.path.join("imgs","cocklob3.png")), (200, 200))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))

class Bird:
	IMGS = BIRD_IMGS
	MAX_ROTATION = 25
	ROT_VOL = 20
	ANIMATION_TIME = 5

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.tilt = 0
		self.tick_count = 0
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]

	def jump(self):
		self.vel = -0.1
		self.tick_count = 0
		self.height = self.y

	def move(self):
		self.tick_count += 0.0005

		d = self.vel * self.tick_count + 1.5 * self.tick_count**2

		if d >= 16:
			d = 16

		if d < 0:
			d -= 1

		self.y = self.y + d

		if d < 0  or self.y < self.height + 50:
			if self.tilt < self.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION

		else:
			if self.tilt > -90:
				self.tilt -= self.ROT_VOL

		if self.y > WIN_HEIGHT:
			self.y = WIN_HEIGHT - 48

		if self.y < 0:
			self.y = 0


	def draw(self, win):
		self.img_count += 1

		if self.img_count < self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*3:
			self.img = self.IMGS[2]
		elif self.img_count < self.ANIMATION_TIME*4:
			self.img = self.IMGS[1]
		elif self.img_count == self.ANIMATION_TIME*4+1:
			self.img = self.IMGS[0]
			self.img_count = 0

		if self.tilt <= -80:
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME*2

		blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

	def get_mask(self):
		return pygame.mask.from_surface(self.img)

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def draw_window(win, bird):
	win.blit(BG_IMG, (0,0))
	bird.draw(win)
	pygame.display.update()

def mouse_clicked(event):
	global mouse_pressed
	if event == (0, 0, 0):
		mouse_pressed = False
		return False
	elif mouse_pressed:
		return False
	elif event == (1, 0, 0):
		mouse_pressed = True
		return True


def main():
	bird = Bird(200, 200)

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()

		bird.move()

		if mouse_clicked(pygame.mouse.get_pressed()):
			print('mf jump')
			bird.jump()

		draw_window(WIN, bird)
		

main()