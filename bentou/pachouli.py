import pygame
import scene
from macrodf import *


def set_opacity(target, source, loc, opacity):
	#这是创建图片背后的背景的副本然后覆盖在图片上透明化背景已达到透明图片的目的 (都差不多)
	temp = pygame.Surface((source.get_width(),source.get_height())).convert()
	#print(temp.get_rect())
	temp.blit(target,(-loc[0], -loc[1],source.get_width(),source.get_height())) # -x , -y 表示图片位置的背景的位置 =>背景 - 原点坐标到图片的距离
	temp.blit(source, (0,0))
	temp.set_alpha(opacity)
	return temp
	

class Paqiuli(pygame.sprite.Sprite):
	def __init__(self):

		pygame.sprite.Sprite.__init__(self)

		#导入各种动作图片(默认向右)
		self.pastay 	= pygame.image.load("pastay.png").convert_alpha()
		self.pamove	 	= pygame.image.load("paright.png").convert_alpha()
		self.pasquat   	= pygame.image.load("pasquat.png").convert_alpha()
		self.pajump	 	= pygame.image.load("rightjump.png").convert_alpha()
		self.pahurt		= pygame.image.load("pahurt.png").convert_alpha()
		self.pafire		= pygame.image.load("pafire.png").convert_alpha()

		#加载关卡
		self.scenes 		= scene.ScenarioOne() #败笔 不该在角色类里加载地图 傻逼一个

		#设置动作帧数和初始状态
		self.hp			 = 50
		self.alive		 = True
		self.suberu		 = False
		self.isright	 = True
		self.isjump		 = False
		self.issquat	 = False
		self.acting		 = "stay"
		self.frames  	= {"stay":6, "move":10, "squat": 6, "jump": 1, "hurt": 4, "fire": 8}
		self.status  	= "stay"
		self.keystatus 	= {pygame.K_SPACE:False, pygame.K_DOWN:False, pygame.K_LEFT:False, pygame.K_RIGHT:False, pygame.K_z:False}
		self.radius 	= 30 #碰刺的半径
		self.ishurt		= False
		self.attacked	= False
		self.blink		= False

		self.statuslock = False
 

		#生成器 用于循环动作帧
		self.showsub = self.paupdate(self.pastay, self.frames["stay"])
		self.nextframe = None

		#速度位置
		self.x 			= 200
		self.y   		= 365
		self.collidedb	= None
		self.collideTR	= None
		self.lastPos	= 0 
		self.vx      	= 0
		self.vy			= 0
		self.rect 		= self.pajump.get_rect()

	def paupdate(self, paqi, frames, delay = 70, issquat = False, ishurt = False, isfire = False):
		#get_ticks 获得开始时长 返回毫秒
		timecheck = pygame.time.get_ticks()
		step = 0
		P = None
		widthperframe = paqi.get_width() / frames
		while True:
		
			self.rect = pygame.Rect(step*widthperframe, 0, widthperframe, PAHEIHGT)

			# 设置循环周期
			temp = pygame.time.get_ticks()
			if temp - timecheck >= delay:
				step += 1
				timecheck = temp

				if step == frames:
					step = 0
					if issquat:
						step = frames -1
					if ishurt:
						self.status = "stay"
						self.attacked = False
						self.statuslock = False
					if isfire:
						self.status = "stay"
						self.statuslock = False


			P = paqi.subsurface(self.rect)
			if not self.isright:
				P = pygame.transform.flip(P, True, False)
			yield P

	def move(self):
		if True in self.keystatus.values():
			if self.keystatus[pygame.K_SPACE] and (not self.issquat) and (self.status not in ["hurt"]):# 跳
				#如果已经起跳了 只需要像马里奥那样按的久跳的高
				if self.isjump == True:
					self.vy -= 1
				else:
					self.vy = -15
				self.isjump = True
				self.collidedb = None

			if self.keystatus[pygame.K_RIGHT]:# 右
				if self.vx < 0 and self.suberu:
					self.vx = 0
				self.vx += 1
				self.isright = True
				self.issquat = False
				if self.vx > 6:
					self.vx = 8
			if self.keystatus[pygame.K_LEFT]: #左
				if self.vx > 0 and self.suberu:
					self.vx = 0
				self.vx -= 1
				self.isright = False
				self.issquat = False
				if self.vx < -6:
					self.vx = -8
			if self.keystatus[pygame.K_DOWN] and (not self.isjump): #蹲
				self.vx = 0
				self.issquat = True
				


		else:
			#全部松开后 速度开始减少
			if self.vx < 0:
				self.vx += FRIC
				if self.vx >0:
					self.vx = 0
			elif self.vx > 0:
				self.vx -= FRIC
				if self.vx < 0:
					self.vx = 0
		if self.x <= 0:
			self.x = 0

		#确定动作帧
		if not self.statuslock:
			if self.issquat:
				self.status = "squat"
				self.ishurt = False
				pygame.time.set_timer(HURT, 0)
				self.blink = False
			elif self.attacked:
				self.status = "hurt"
				self.statuslock = True
			elif self.isjump:
				self.status = "jump"
			elif self.vx != 0:
				self.status = "move"
			else:
				self.status = "stay"
		else:
			self.vx = 0


		if not self.collidedb:
			self.vy += GRAV
		elif (self.rect.center[0] < self.collidedb.left - int(self.rect.width/2)) or (self.rect.center[0] > self.collidedb.right + int(self.rect.width/2)):
			self.collidedb = None
		
		#x的移动可用地图移动反方向移动代替
		vy_half = int(self.vy/2)
		self.scenes.vy = vy_half #self.initheight - self.y
		self.scenes.heightchanged = vy_half
		self.x  += self.scenes.moveH(self.x, self.vx)
		#y的移动和地图对半分 人往上1半vy  地图往下一半vy造成跳的很高的视觉
		self.y  += vy_half


		#falldown test
		if self.y >= 720:
			self.alive = False

		#更新下一帧的信息 顺带更新rect 然后判断碰撞
		self.nextframe = next(self.showsub)
		self.updateframepos()
		self.buildetect()
		self.lastPos = self.getpos()

	
	def show(self, target):
		#print(self.status)
		if self.status == "squat" and (self.acting != self.status):
			self.showsub = self.paupdate(self.pasquat, self.frames["squat"], issquat = True)
			self.acting = self.status
		
		elif self.status=="jump" and (self.acting != self.status):
			self.showsub = self.paupdate(self.pajump, self.frames["jump"])
			self.acting = self.status
		
		elif self.status=="move" and (self.acting != self.status):
			self.showsub = self.paupdate(self.pamove, self.frames["move"])
			self.acting = self.status

		elif self.status == "hurt" and (self.acting != self.status):
			self.showsub = self.paupdate(self.pahurt, self.frames["hurt"], ishurt = True)
			self.acting = "hurt"

		elif self.status =="stay" and (self.acting != self.status):
			self.showsub = self.paupdate(self.pastay, self.frames["stay"])
			self.acting = self.status
		elif self.status == "fire" and (self.acting != self.status):
			self.showsub = self.paupdate(self.pafire, self. frames["fire"], isfire = True, delay = 30)
			self.acting = self.status

		self.scenes.show(target)
		if self.blink:
			self.hurt(target)
		target.blit(self.nextframe, self.rect)
		pygame.draw.rect(target,(160,1,1), (self.rect.left + 5, self.rect.top - 10, self.hp, 10))

	def buildetect(self):
		index = self.rect.collidelist(self.scenes.buildings)
		#fi = list(filter(self.scenes.inscreen, self.scenes.buildings))
		#print(len(fi))

		if index != -1:
			buil = self.scenes.buildings[index]

			half_h = int(self.rect.height/2)
			half_w = int(self.rect.width/2)
			# 判断是否高于或低于上下两端
			if self.lastPos[1] in range(buil.top - half_h, buil.bottom + half_h) and \
					(self.lastPos[0] <= buil.left - half_w + 20 or self.lastPos[0] >= buil.right + half_w - 20):

				self.vx = 0 #为什么不重置速度就还是会出现相交的情况 明明已经在移动后把帕奇定位在建筑外了 (原因是 更新了x值之后没有更新rect里的值) 但还是选择重置 碰到了停下
				#获取帕奇和建筑的差值 处理相交
				difference = buil.center[0] - self.rect.center[0]
				intersect = ((buil.width/2 + self.rect.width/2) - abs(difference))
				intersect = int(intersect * difference/abs(difference) + 0.5)
				#小于0则在右边 大于0则在左边
				#判断是地图动还是帕奇动
				if self.scenes.left_border != 0:
					#因为vx还存在 所以需要不断更新地图反方向移动 然后框架
					self.scenes.left_border -= intersect
					
					for each in self.scenes.buildings:
						each.left += intersect
					#self.scenes.buildings[index].left += intersect * difference/abs(difference)
				else:
					self.x -= intersect

			else:
				difference = buil.center[1] - self.rect.center[1]
				intersect = ((buil.height/2 + self.rect.height/2) - abs(difference))
				halfIntersect = int(0.5 * intersect * difference/abs(difference) + 1)
				print("hi:",intersect)
				if self.lastPos[1] < buil.top:
					self.y -= halfIntersect 
					self.scenes.height += halfIntersect
					self.scenes.vy = -halfIntersect
					self.scenes.heightchanged -= halfIntersect
					self.scenes.updateframes()
					self.collidedb = buil
					self.xrange	   = (buil.left, buil.right)
					self.vy = 0
					self.scenes.vy = 0
					self.isjump = False
					print("need change height")
					#issue rect莫名抖动 然后 collidelist 只能返回第一个碰撞的下标 如果你踩着一个方块然后又碰撞一个 就失效

			self.updateframepos()
	def updateframepos(self):
		self.rect.left, self.rect.top = self.x, self.y
	def getpos(self):
		return self.rect.center

	def hurt(self, target):
		self.nextframe = set_opacity(target, self.nextframe, (self.rect.left, self.rect.top), 100)






