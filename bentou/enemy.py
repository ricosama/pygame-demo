import pygame
import random
from macrodf import *

class EnemyBasic(pygame.sprite.Sprite):
	def __init__(self, pos, hp, pic, framesN, R):
		# 起始位置 血量 移动
		pygame.sprite.Sprite.__init__(self)

		self.estay = pic[0]
		self.emove = pic[1]
		self.ehurt = pic[2]
		self.efire = pic[3]
		self.freames = {self.estay:framesN[0], self.emove:framesN[1], self.ehurt:framesN[2], self.efire:framesN[3]}
		self.status = self.estay
		self.stchanged = False

		self.x = pos[0]
		self.y = pos[1]
		self.vx = 0
		self.vy = 0
		self.activeRange = [0,10000] #默认无限
		self.pause = 0 #ms
		self.rect = None
		self.radius = R
		self.hp = hp
		self.orientR = True
		self.ishurt  = False
		self.isfire  = False
		self.fLock = False
		self.moving = True #enemy 随机时段移动
		self.dead = False

		self.fupdate = self.updateF(self.status, self.freames[self.status])
		self.nextF	 = next(self.fupdate)

		self.timecheck0 = pygame.time.get_ticks()

	def move(self, vx, vy): #这里的v是配合地图移动
		self.x += vx
		self.y += vy

		if not self.fLock:
			if self.ishurt:
				self.status = self.ehurt
				self.stchanged = True
				self.fLock = True
				self.ishurt = False
				#self.stchange()
			
			elif self.vx != 0 and self.status != self.emove:
				self.stchanged = True
				self.status = self.emove
				#self.stchange()
			
			elif self.status != self.estay and self.vx == 0:
				self.stchanged = True
				self.status = self.estay
				#self.stchange()
		half_w = int(self.rect.width /2)
		if self.x + half_w >= self.activeRange[1]:
			self.x = self.activeRange[1] - half_w
		elif self.x - half_w <= self.activeRange[0]:
			self.x = self.activeRange[0] + half_w
		
		self.nextF = next(self.fupdate)
		self.updateR()


	def stchange(self):
		self.fupdate = self.updateF(self.status, self.freames[self.status])
		self.stchanged = False

	def updateF(self, obj, frameN, delay = 100, conti = False):
		timecheck = pygame.time.get_ticks()
		step = 0

		whidthperfreame = obj.get_width() / frameN
		while True:

			self.rect = pygame.Rect(step*whidthperfreame, 0, whidthperfreame, obj.get_height())

			temp = pygame.time.get_ticks()
			if temp - timecheck >= delay:
				step += 1
				timecheck = temp

				if step == frameN:
					step = 0

					if conti:
						step = frameN - 1

					if self.fLock:
						self.fLock = False
						self.status = self.estay
						if self.hp <= 0:
							self.dead = True


			if self.orientR:
				yield obj.subsurface(self.rect)
			else:
				yield pygame.transform.flip(obj.subsurface(self.rect), True, False)
	def hurtAct(self):
		# 帕奇就一种攻击 -1就对了 懒得扩展
		self.hp -= 1
		self.ishurt = True
		self.vx = int(self.vx * 0.75)

		print("hurt")


	
	def show(self, target):
		if self.stchanged:
			self.stchange()
		target.blit(self.nextF, self.rect)
		pygame.draw.rect(target, (160, 1, 1), (self.rect.left + 5, self.rect.top - 10, self.hp * 10, 10))

	def updateR(self):
		self.rect.center = (self.x, self.y)




class Cirno(EnemyBasic):
	def __init__(self):
		choi = [0, 1380]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
		x = random.choice(choi)
		y = random.randint(100,500)

		cirstay = pygame.image.load("cirstay.png").convert_alpha()
		cirmovef = pygame.image.load("cirmovef.png").convert_alpha()
		cirmoveb = pygame.image.load("cirmoveb.png").convert_alpha()
		cirfire  = pygame.image.load("cirfire.png").convert_alpha()
		cirhurt	 = pygame.image.load("cirhurt.png").convert_alpha()

		actions = (cirstay, cirmovef, cirhurt, cirfire)
		framesN = [1, 8, 3, 6]

		EnemyBasic.__init__(self, (x, y), 10, actions, framesN, 35)

		self.fireInterval = random.randint(2000,3000) #ms
		self.fireTimer	  = self.timecheck0

		self.fireStyle = [0, 1] #跟踪3连击 or 散弹

		self.cirmoveb = cirmoveb
		self.freames.update({cirmoveb:8})

	def move(self, papos, scenevx, scenevy):

		if papos.centerx < self.x:
			self.orientR = False
		else:
			self.orientR = True

		timecheck1 = pygame.time.get_ticks()
		if timecheck1 - self.timecheck0 >= self.pause:
			self.moving = True
			self.timecheck0 = timecheck1
			self.pause = random.randint(1000, 2000)
		if timecheck1 - self.fireTimer >= self.fireInterval:
			self.vx = 0
			self.vy = 0
			self.status = self.efire
			self.fireTimer = timecheck1
			self.fLock = True
			self.isfire = True
			self.fupdate = self.updateF(self.status, self.freames[self.status], delay = 60)

		#配置移动速度
		if self.moving and self.status != self.efire:
			if abs(self.x - papos.centerx) < 100:
				vx = random.randint(-4, -2)
			elif abs(self.x - papos.centerx) > 500:
				vx = random.randint(2, 4)
			else:
				vx = random.randint(-4, 4)

			if not self.orientR:
				vx = -vx 

			if abs(self.y - papos.centery) < 40 or papos.centery - self.y < -100:
				vy = random.randint(-3, -1)
			elif papos.centery - self.y > 300:
				vy = random.randint(2, 4)
			else:
				vy = random.randint(-3, 3)

			self.vx = vx
			self.vy = vy

		self.activeRange[0] -= scenevx
		self.activeRange[1] -= scenevx

		EnemyBasic.move(self, self.vx - scenevx, self.vy - scenevy)
		if self.y >= 720:
			self.y = 720
			self.moving = True
		

		#加载前后移动帧
		if self.moving and self.status != self.efire:
			self.moving = False
			if self.orientR:
				if self.vx < 0:
					self.status = self.cirmoveb
				else:
					self.status = self.emove 
				self.stchange()
				self.status = self.emove
			else:
				if self.vx > 0:
					self.status = self.cirmoveb
				else:
					self.status = self.emove 
				self.stchange()
				self.status = self.emove







class Slime(EnemyBasic):
	def __init__(self, activeRange, pos):
		slistay = pygame.image.load("slistay.png").convert_alpha()
		slihurt = pygame.image.load("slihurt.png").convert_alpha()
		slidash = pygame.image.load("slidash.png").convert_alpha()

		actions = (slistay, slidash, slihurt, None)
		frameN = [4, 1, 3, 0]

		EnemyBasic.__init__(self, pos, 10, actions, frameN, 50)
		# 修改参数
		self.pause = 1200 #ms
		self.activeRange = list(activeRange)

	def move(self, papos, scenevx, scenevy):


		if papos.centerx < self.x:
			self.orientR = False
		else:
			self.orientR = True

		timecheck1 = pygame.time.get_ticks()
		if timecheck1 - self.timecheck0 >= self.pause:
			self.timecheck0 = timecheck1
			self.moving = True

		if self.moving:
			if self.orientR:
				self.vx = 15
			else:
				self.vx = -15
			self.moving = False

		if self.vx < 0:
			self.vx += FRIC
			if self.vx >0:
				self.vx = 0
		elif self.vx > 0:
			self.vx -= FRIC
			if self.vx < 0:
				self.vx = 0


		self.activeRange[0] -= scenevx
		self.activeRange[1] -= scenevx
		EnemyBasic.move(self,self.vx - scenevx, self.vy - scenevy)














