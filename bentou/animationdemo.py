import sys
import pygame
import pachouli
import scene
import danmoku
import enemy
from macrodf import *

def main():

	pygame.init()

	clock = pygame.time.Clock()

	size = (1280, 720)
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("TOUHOUBENTOU")

	#初始化帕奇类和陷阱类 同步进精灵组
	pachi = pachouli.Paqiuli()
	slimes = [enemy.Slime((145, 2050), (1000, 430)), enemy.Slime((145, 2050), (1800, 430))]
	cirnos = []
	summoncir = True

	font1 = pygame.font.Font("simhei.ttf", 16) #设置字体
	fontHeight = font1.get_linesize() # 获得字体的高度
	guideText = ["z-射鸡", "space-跳", "← →-移动", "↓-止血+蹲(无敌)"]

	trapR = pygame.sprite.Group()
	for each in pachi.scenes.traps:
		trapR.add(each)
	for each in slimes: #干脆把怪也加进去算了 反正都是撞
		trapR.add(each)

	dmk = []
	dmkR = pygame.sprite.Group()

	edmk = []
	edmkR = pygame.sprite.Group()

	pygame.event.set_blocked(pygame.MOUSEMOTION)
	while pachi.alive:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or not pachi.alive:
				sys.exit()

			# 左右移动 下蹲 空格跳 s改变move方式
			if event.type == pygame.KEYDOWN:  # 检测type 如果是键盘按下则判断是否是方向键 用字典 event.key == K_键
				if event.key in pachi.keystatus:
					pachi.keystatus[event.key] = True
				if event.key == pygame.K_s:
					pachi.suberu = not pachi.suberu
				if event.key == pygame.K_z:
					if pachi.status != "fire":
						dmk.append(danmoku.Pafireball(pachi.isright, pachi.rect))
						dmkR.add(dmk[-1])
						pachi.status = "fire"
						pachi.statuslock = True

						
			if event.type == pygame.KEYUP:
				if event.key in pachi.keystatus:
					pachi.keystatus[event.key] = False

			if event.type == HURT:
				pachi.blink = not pachi.blink
				pachi.hp -= 4
                                                                                          
		#screen.blit(background, (0, 0))

		pachi.move()

		if summoncir and pachi.scenes.left_border > 4400:
			print('1')
			summoncir = False
			for each in trapR:
				if hasattr(each, 'hp'):
					trapR.remove(each)
			del slimes[:]
			for i in range(2):
				cirnos.append(enemy.Cirno())
				trapR.add(cirnos[i])




		for each in slimes:
			each.move(pachi.rect, pachi.scenes.boderchanged, pachi.scenes.heightchanged)
		
		for each in cirnos:
			each.move(pachi.rect, pachi.scenes.boderchanged, pachi.scenes.heightchanged)
			if each.isfire:
				print("fireeee")
				each.isfire = False
				edmk.append(danmoku.Cirice(each.orientR, each.rect.center, pachi.rect.center))
				edmkR.add(edmk[-1])
		
		for each in dmk:
			each.move(pachi.scenes.boderchanged, pachi.scenes.heightchanged)
			if each.outrange:
				dmk.remove(each)
				dmkR.remove(each)

		for each in edmk:
			each.move(pachi.scenes.boderchanged, pachi.scenes.heightchanged)
			if each.outrange:
				edmk.remove(each)
				edmkR.remove(each)


		
		collide = pygame.sprite.spritecollide(pachi, trapR, False, pygame.sprite.collide_circle)
		if collide and not pachi.ishurt:
			pachi.ishurt = True
			pachi.attacked = True
			pachi.vx = 0
			pygame.time.set_timer(HURT, 150)
			print("collied")
			#pachi.alive = False
		#pachi.hurt(screen)
		collide = pygame.sprite.spritecollide(pachi, edmkR, False, pygame.sprite.collide_circle)
		if collide and not pachi.ishurt:
			pachi.ishurt = True
			pachi.attacked = True
			pachi.vx = 0
			pygame.time.set_timer(HURT, 150)
			print("collied")
		
		# 帕奇的子弹
		bulletcollide = pygame.sprite.groupcollide(dmkR, trapR, False, False, pygame.sprite.collide_circle)
		for bullet,target in bulletcollide.items(): #拆解dict 返回键和值的元祖
			if target:
				if hasattr(target[0], 'hp'):
					target[0].hurtAct()
					print(target[0].hp)
					if target[0].hp <= 0:
						trapR.remove(target[0])

					dmkR.remove(bullet)
					dmk.remove(bullet)


		pachi.show(screen)

		fontpos = 0
		for line in guideText:
			str1 = font1.render(line, True, (255,255,255))
			screen.blit(str1, (0, fontpos))
			fontpos += fontHeight

		
		for each in slimes:
			each.show(screen)
			if each.dead:
				slimes.remove(each)
		
		for each in cirnos:
			each.show(screen)
			if each.dead:
				cirnos.remove(each)
		
		for each in dmk:
			each.show(screen)
		for each in edmk:
			each.show(screen)


		if pachi.hp <= 0:
			pachi.alive = False


		pygame.display.flip()  # 更新界面

		clock.tick(60)


if __name__ == "__main__":
	main()
