import pygame
import copy
from macrodf import *


class ScenarioOne:
	def __init__(self):

		self.background = pygame.image.load('redmoon.png').convert()

		self.buildings = [pygame.Rect(0,469,2050,250), pygame.Rect(53,355,85,105), 
						  pygame.Rect(2137,353,157,67), pygame.Rect(2439, 227,157,67), pygame.Rect(2911,417,157,67) ,
						  pygame.Rect(3352,417,1246,65), pygame.Rect(4796,463,2008,256)]
		self.buildCopy = copy.deepcopy(self.buildings)
		self.buildTopCopy = [self.buildings[x].top for x in range(len(self.buildings))]
		self.traps = [CircularSaw((3739, 332)), CircularSaw((4027, 332)), CircularSaw((4316, 332))]
		self.trapsCopy = copy.deepcopy(self.traps)
		self.route = pygame.image.load("bg.png").convert_alpha()

		self.left_border = 0
		self.initheight = 0
		self.height = self.initheight
		self.lastboder = 0
		self.boderchanged = 0
		self.heightchanged = 0
		self.vy 	= 0

	def moveH(self, paqix, paqivx):
		paqivx = int(paqivx)

		temp = 0
		if (self.left_border == 0 or self.route.get_width() - self.left_border == 1290) and paqivx != 0:
			if abs(paqix - SCREENSIZE[0]/2) < 5:
				self.left_border += paqivx
			else:
				temp = paqivx
		elif paqivx != 0:
			self.left_border += paqivx
			if self.left_border <= 0:
				diff = paqivx - self.left_border
				self.left_border = 0
				self.initialize()
				self.updateframes()
				temp = paqivx
			elif self.left_border >= self.route.get_width() - 1290:
				temp = paqivx
				diff = self.route.get_width() - 1290 - self.left_border
				self.moveH(paqix, diff)
				#self.left_border = self.route.get_width() - 1290
		#print(self.left_border)


		'''for each in self.buildings:
			each.top -= self.vy
			print(self.vy)
			#帕奇走到中间时开始移动建筑的碰撞区域
			if self.left_border != 0:  
				each.left -= paqivx'''
		self.height -= self.vy
		#print(self.height)
		for i in range(len(self.buildings)):
			#这个问题卡了我两天 原因是rect里面存的是int  然后我的self.height 存的是 float 导致的偏差
			#self.buildings[i].top = self.buildTopCopy[i] + self.height
			self.buildings[i].top -= self.vy

			if self.left_border != 0 and self.route.get_width() - self.left_border != 1290:
				self.buildings[i].left -= paqivx

		for each in self.traps:
			each.move(self.left_border, self.vy)

		self.boderchanged = self.left_border - self.lastboder
		self.lastboder 	  = self.left_border
		#print(self.boderchanged)
		return temp

	def updateframes(self):
		for i in range(len(self.buildings)):
			#这个问题卡了我两天 原因是rect里面存的是int  然后我的self.height 存的是 float 导致的偏差
			self.buildings[i].top = self.buildTopCopy[i] + self.height
		for each in self.traps:
			each.move(self.left_border, self.vy)

	def initialize(self):
		self.buildings = copy.deepcopy(self.buildCopy)
	'''def initHeight(self):
		for each,top in zip(self.buildings, self.buildTopCopy):
			each.top = top 
	def changedHeight(self):
		self.buildCopy = copy.deepcopy(self.buildings)
		self.buildTopCopy = [self.buildCopy[x].top for x in range(len(self.buildings))]
	def inscreen(self, build):
		#想着用filter返回屏幕内的碰撞矩形 但是这个计算量好像不差什么了？ 先放着吧
		if (build.left - self.left_border < 1280 and build.left - self.left_border > 0) or \
			(build.right - self.left_border < 1280 and build.right - self.left_border > 0) :
			return True
		else:
			return False'''

	def show(self, target):

		target.blit(self.background, (0, 0))
		try:
			temp = self.route.subsurface(((self.left_border, 0), SCREENSIZE))
		except(ValueError):
			temp = self.route.subsurface(((0,0), SCREENSIZE))

		target.blit(temp, (0, self.height))

class CircularSaw(pygame.sprite.Sprite):
	def __init__(self, pos):
		# type => circularSaw
		pygame.sprite.Sprite.__init__(self)
		self.radius = 82
		self.rect = pygame.Rect(pos,(self.radius * 2,self.radius * 2))
		self.rectL = self.rect.left

	def move(self, leftB, vy):
		self.rect.left = self.rectL - leftB
		self.rect.top  -= vy
		



		

