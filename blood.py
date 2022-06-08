import pygame
import random

class Blood(pygame.sprite.Sprite):
	def __init__(self, pos, color ,screen):
		super(Blood, self).__init__()
		self.color = color

		self.x, self.y = pos
		self.y += 10
		self.dx = random.randint(0,20) / 10 - 1
		self.dy = -2
		self.size = random.randint(4,7)

		self.rect = pygame.draw.circle(  screen ,self.color, (self.x, self.y), self.size)

	def update(self , screen):
		self.x -= self.dx
		self.y -= self.dy
		self.size -= 0.1

		if self.size <= 0:
			self.kill()

		self.rect = pygame.draw.circle( screen, self.color, (self.x, self.y), self.size)