#!/usr/bin/python
############################################################################################################
try:
	import sys
	import os
	import pygame
	from pygame.locals import *
	import math
#	from scipy import signal	
#	import numpy
#	from lib.perlin2d import generate_perlin_noise_2d
	from terrain import *
except ImportError as err:
	print("could not load module: " ,err)
	sys.exit(2)


############################################################################################################
# Constants
FRAME_RATE = 30

###########################################################################################################
def load_png(name):
	#load a .png and return a pygame.image
	fullname = os.path.join('assets', name) 
	try:
		image = pygame.image.load(fullname)
		if image.get_alpha() is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	except pygame.error as	message:
		print ("Cannot load image: ", fullname)
		raise SystemExit(message) 
	return image, image.get_rect()	
############################################################################################################
class PhysicsObject():
	def __init__(self,x=0.0,y=0.0):
		self.px = x
		self.py = y
		self.vx = 0.0
		self.vy = 0.0
		self.ax = 0.0
		self.ay = 0.0

		self.radius =	4.0
		self.stable = False
		self.friction = 0.3

class Soldier(pygame.sprite.Sprite,PhysicsObject):
		def __init__(self,name,image,terrain,x=0.0,y=0.0):
				pygame.sprite.Sprite.__init__(self)
				PhysicsObject.__init__(self,x,y)
				self.image, self.rect = load_png(image)
				self.rect = self.image.get_rect()
				self.terrain = terrain
				self.rect.centerx = self.px 
				self.rect.centery = self.py 
		
		def update(self):
				self.ay += 0.1 
				self.vx += self.ax 
				self.vy	+= self.ay 
				potentialX = self.px + self.vx   
				potentialY = self.py + self.vy  
				self.ax = 0.0
				self.ay = 0.0
				self.stable = False

				angle = math.atan2(self.vy, self.vx) 
				responseX = 0
				responseY = 0
				collision = False
				for r in numpy.arange((angle - math.pi/2.0), (angle + math.pi/2.0), (math.pi/8.0)):
					testPosX = self.radius * math.cos(r) +	potentialX
					testPosY = self.radius * math.sin(r) + potentialY
					int_x = int(testPosX)
					int_y = int(testPosY)
					if int_x >= self.terrain.x : int_x = self.terrain.x - 1
					if int_x < 0 : int_x = 0
					if int_y >= self.terrain.y : int_y = self.terrain.y - 1
					if int_y < 0 : int_y = 0	
					if (self.terrain.surface.get_at((int_x,int_y))[0] == 255):
						responseX += potentialX - testPosX
						responseY += potentialY - testPosY
						collision = True
				magVelocity = math.sqrt(self.vx * self.vx + self.vy * self.vy)
				magResponse = math.sqrt(responseX * responseX + responseY * responseY)

				if collision:
					self.stable = True
					dot = self.vx * (responseX / magResponse) + self.vy * (responseY/magResponse)
					self.vx = self.friction * (-2.0 * dot * (responseX / magResponse) + self.vx)
					self.vy = self.friction * (-2.0 * dot * (responseY / magResponse) + self.vy) 
				else:
	
					self.px = potentialX
					self.py = potentialY
				self.rect.centerx = self.px
				self.rect.centery = self.py
				if (magVelocity < 0.1):
					self.stable = True

				pygame.event.pump()



############################################################################################################	 
def main():
	#Initialize Screen
		pygame.init()
		screen = pygame.display.set_mode((640,360))
		pygame.display.set_caption("Squadron")
	
		#Fill Background
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((0,0,0))
		screen.blit(background, (0,0))
		terrain = Terrain(screen)		 
		screen.blit(terrain.surface, (0,0))
		#Initialize player
		allSprites = pygame.sprite.Group()
	
		#Initialize clock
		clock = pygame.time.Clock()
		keepGoing = True
		#Game Loop
		while(keepGoing):
				clock.tick(30)
				for event in pygame.event.get():
						if event.type == QUIT:
								keepGoing = False
						elif event.type == MOUSEBUTTONDOWN:
							x,y = pygame.mouse.get_pos()
							player = Soldier("New", "small_square.png",terrain,x,y)
							player.add(allSprites)
				allSprites.clear(screen, background)
				allSprites.update()
				screen.blit(terrain.surface,(0,0))
				allSprites.draw(screen)
				
				pygame.display.flip()
if __name__=='__main__' : 
		main()

