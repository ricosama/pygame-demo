import pygame
PAHEIHGT = 101 #帕奇的身高
GRAV	 = 1.5
FRIC	 = 0.5

HURT = pygame.USEREVENT + 1

SCREENSIZE = (1280, 720)
class SC(tuple):
	def __init__(self, *arg):
		self.width = 1280
		self.height = 720
		arg = (width, height)
		tuple.__init__(self, arg)
