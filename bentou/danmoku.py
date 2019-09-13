import pygame
import math
import pachouli
from macrodf import *

# 弹幕基类

class dmbasic(pygame.sprite.Sprite):
	def __init__(self, pic, r, vel, pos):

		pygame.sprite.Sprite.__init__(self)
		#方向 图片 速度 初始位置 rect radius(假设都是圆的)
		self.bullet = pygame.image.load(pic).convert_alpha()
		self.x 		= pos[0]
		self.y		= pos[1]
		self.vx 	= int(vel[0])
		self.vy 	= int(vel[1])
		print(self.vx , "and", self.vy)
		self.speed	= math.sqrt(pow(self.vx,2) + pow(self.vy,2))

		self.degree = math.degrees(math.asin(self.vy / self.speed))
		if self.vx < 0:
			self.degree = 180 - self.degree

		self.bullet = pygame.transform.rotate(self.bullet, -self.degree) #- 是因为y轴反转
		self.rect	= self.bullet.get_rect(center = pos)
		self.radius = r


		self.outrange = False
	def move(self, bvx = 0, bvy = 0):
		self.x += self.vx
		self.x -= bvx
		self.y += self.vy
		self.y -= bvy

		if self.x > 1280 or self.x < 0 or self.y > 720 or self.y < 0:
			self.outrange = True

		self.updateRect()

	def updateRect(self):
		self.rect.center = (self.x, self.y)

	def show(self, target):
		target.blit(self.bullet, self.rect)

class Pafireball(dmbasic):
	def __init__(self, isright, parect):

		image = "fireball.png"
		velx  = 8
		if not isright:
			velx *= -1

		pos = parect.center

		dmbasic.__init__(self, image, 10, (velx, 0), pos)
		self.From = pachouli.Paqiuli

class Cirice(dmbasic):
	def __init__(self, isright, Cirpos, Papos):

		image = "cirice.png"

		self.orentR = isright
		distance = math.sqrt(pow(Papos[0] - Cirpos[0], 2) + pow(Papos[1] - Cirpos[1], 2))
		unx = (Papos[0] - Cirpos[0]) / distance
		uny = (Papos[1] - Cirpos[1]) / distance #y轴反转

		speed = 10

		r = 5

		dmbasic.__init__(self, image, r, (unx * speed, uny * speed), Cirpos)



		



		



