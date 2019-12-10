#!/usr/bin/python
############################################################################################################
try:
	import sys
	import os
	import pygame
	from pygame.locals import *
	import math
#	from random import random
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
#load a png file from the assets directory
#From the pygame example docs
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
#The boom object is created from explosions
#Updates the terrain bitmap and effects the physics of PhysicsObjects
#A better implementation might be as an event that gets checked in the game loop 

class Boom():
	def __init__(self,terrain,sprites,worldX,worldY,radius):

		#the terrain of the game
		self.terrain = terrain

		#List of all sprites(physics objects) in the game
		self.sprites = sprites

		#position of the boom
		self.worldX = worldX
		self.worldY = worldY

		self.radius = radius

		#Bresenham function for creating circles in the bitmap
		self.circle_bresenham(self.worldX,self.worldY,self.radius)
		
		#Function to check and update the physics of objects in the radius of the boom
		self.shockwave()
	
	#Change the color of the pixels in the ny row from start x to end x to black.
	#Changes all pixels even if they are already black
	def drawline(self,sx,ex,ny):
		for i in range(sx,ex):
			if (ny >= 0 and ny < self.terrain.y and i >= 0 and i < self.terrain.x):
				self.terrain.bitmap[i,ny] = pygame.Color(0,0,0)			

	#Create a circle with center xc,yc and radius r. 
	#Use the drawline function to draw each line of the circle
	def circle_bresenham(self,xc,yc,r):
		x = 0
		y = r
		p = 3-(2*r)
		if not r:
			return
		
		while(y >= x):
			self.drawline(xc-x,xc+x,yc-y)
			self.drawline(xc-y,xc+y,yc-x)
			self.drawline(xc-x,xc+x,yc+y)
			self.drawline(xc-y,xc+y,yc+x)
			if(p <0):
				x+=1
				p+= 4 * x + 6
			else:
				y-=1
				x+=1
				p+=4 * (x - y) + 10
	#Check to see how far each sprite is from the boom
	#If within the radiuis update the velocity vectors 				 
	def shockwave(self):
		for sprite in self.sprites:
			dx = sprite.px - self.worldX
			dy = sprite.py - self.worldY
			dist = math.sqrt(dx*dx + dy*dy)

			#No divide by zero
			if (dist < 0.0001): dist = 0.0001

		if dist < self.radius:
			sprite.vx = (dx / dist) * self.radius
			sprite.vy = (dy / dist) * self.radius
			sprite.stable = False
					
#Base Object for objects that move				
class PhysicsObject():
	def __init__(self,x=0.0,y=0.0):
		#position vectors
		self.px = x
		self.py = y
		#velocity vectors
		self.vx = 0.0
		self.vy = 0.0
		#acceleration vectors
		self.ax = 0.0
		self.ay = 0.0
		
		#radius of the bounding circle
		self.radius =	4.0
		self.stable = False
		self.friction = 0.3
		
		
#Main character class for the game
#Extends pygame.Sprite and PhysicsObject
class Soldier(pygame.sprite.Sprite,PhysicsObject):
		def __init__(self,name,image,terrain,x=0.0,y=0.0):
				pygame.sprite.Sprite.__init__(self)
				PhysicsObject.__init__(self,x,y)
				self.image, self.rect = load_png(image)
		#		self.rect = self.image.get_rect()
				self.terrain = terrain
				self.rect.centerx = self.px 
				self.rect.centery = self.py 

		
		def update(self):
				#Update physics vectors 
				self.ay += 0.1 #gravity 
				self.vx += self.ax 
				self.vy	+= self.ay 
				#Calculate the potential position, then check for collision
				potentialX = self.px + self.vx   
				potentialY = self.py + self.vy  
				self.ax = 0.0
				self.ay = 0.0
				self.stable = False

				#Find the angle of motion
				angle = math.atan2(self.vy, self.vx) 
				responseX = 0
				responseY = 0
				collision = False
				#iterate over points on bounding circle to check for collisions
				for r in numpy.arange((angle - math.pi/2.0), (angle + math.pi/2.0), (math.pi/8.0)):
					testPosX = self.radius * math.cos(r) +	potentialX
					testPosY = self.radius * math.sin(r) + potentialY
					int_x = int(testPosX)
					int_y = int(testPosY)

					#Constrain to screen
					if int_x >= self.terrain.x : int_x = self.terrain.x - 1
					if int_x < 0 : int_x = 0
					if int_y >= self.terrain.y : int_y = self.terrain.y - 1
					if int_y < 0 : int_y = 0	
					#Check for collision using the color of the bitmap at the test positions
					if (self.terrain.surface.get_at((int_x,int_y))[0] == 255):
						responseX += potentialX - testPosX
						responseY += potentialY - testPosY
						collision = True
					magVelocity = math.sqrt(self.vx * self.vx + self.vy * self.vy)
					magResponse = math.sqrt(responseX * responseX + responseY * responseY)

				if collision:
					self.stable = True
					#Update motion from collision
					dot = self.vx * (responseX / magResponse) + self.vy * (responseY/magResponse)
					self.vx = self.friction * (-2.0 * dot * (responseX / magResponse) + self.vx)
					self.vy = self.friction * (-2.0 * dot * (responseY / magResponse) + self.vy) 
				else:
					self.px = potentialX
					self.py = potentialY
				#Update the rect of the object
				self.rect.centerx = self.px
				self.rect.centery = self.py

				#stop the motion after it gets too low
				if (magVelocity < 0.1):
					self.stable = True

				pygame.event.pump()
		
"""
#Debris object that is generate from terrain destruction

class Debris(PhysicsObject):
	def __init__(self, terrain, x=0.0, y=0.0):
		PhysicsObject.__init__(self,x,y)
		self.terrain = terrain
		self.vx = 10.0 * math.cos((random()/90.0 * 2.0 * math.pi))
		self.vy = 10.0 * math.sin((random()/90.0 * 2.0 * math.pi))
		self.radius = 1.0
		self.surface = pygame.Surface((4,4))
		self.surface.fill((255,255,255))
		self.rect = self.surface.get_rect()
		self.rect.centerx = x
		self.rect.centery = y

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
"""		
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

		#Initialize Terrain
		terrain = Terrain(screen)		 
		screen.blit(terrain.surface, (0,0))

		#Initialize sprite array(Physics Objects array) 
		sprites = []
		
		#Initialize sprite group for drawing soldiers
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
						elif event.type == pygame.KEYDOWN:
							#B button creates a boom object at the mouse position
							if event.key == K_b:
								x,y =pygame.mouse.get_pos()
								boom = Boom(terrain,sprites,x,y,10) 
						#Mouse Click creates a new soldier at mouse position
						elif event.type == MOUSEBUTTONDOWN:
							x,y = pygame.mouse.get_pos()
							player = Soldier("New", "small_square.png",terrain,x,y)
							player.add(allSprites)
							sprites.append(player)
				allSprites.clear(screen, background)
				allSprites.update()

				#Update for destructions
				terrain.update()
				screen.blit(terrain.surface,(0,0))
				allSprites.draw(screen)
				
				pygame.display.flip()
if __name__=='__main__' : 
		main()

