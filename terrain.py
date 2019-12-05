#!/usr/bin/python
#####################################################################################
try:
	import sys
	import pygame
	import os
	from scipy import signal	
	from skimage.exposure import rescale_intensity
	from pygame.locals import *
	from random import seed
	from random import randint
	import numpy
	from lib.perlin2d import generate_perlin_noise_2d
	from collections import deque
except ImportError as err:
	print("Could not load module: ", err)
	sys.exit(2)

#####################################################################################
	# Constants
FRAME_RATE = 30

#####################################################################################
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


smallBlur = numpy.ones((7,7), dtype="float") * (1.0/(7*7))			
largeBlur = numpy.ones((21,21), dtype="float") * (1.0/(21*21))
sharpen = numpy.array((
	[0,-1,0],
	[-1,5,-1],
	[0,-1,0]), dtype ="int")

#######################################################################################
		
class Terrain(pygame.sprite.Sprite):
		def __init__(self,screen,base_image):
				pygame.sprite.Sprite.__init__(self)
				self.screen = screen
				self.x,self.y = screen.get_size()
				self.image,self.rect = load_png(base_image)
				self.noisemap = generate_perlin_noise_2d((self.x,self.y),(20,20))
				self.noisemap = self.noisemap * 255
				self.add_darkness(self.noisemap)
				self.add_light(self.noisemap)
				
				self.noisemap = signal.convolve2d(self.noisemap,largeBlur,'same')
				self.noisemap = signal.convolve2d(self.noisemap,largeBlur,'same')
				self.noisemap = signal.convolve2d(self.noisemap,largeBlur,'same')
				self.noisemap = signal.convolve2d(self.noisemap,largeBlur,'same')
				self.noisemap = signal.convolve2d(self.noisemap,sharpen,'same')
				self.bitmap = self.generate_bitmap()
				self.surface = pygame.PixelArray.make_surface(self.bitmap)
				
						
		def add_darkness(self,noisemap):
			for row in range(self.x):
				for col in range(200):						
					noisemap[row,col] = noisemap[row,col] + 200
			for row in range(50):
				for col in range(self.y-1, 200,-1):
					noisemap[row,col] = noisemap[row,col] + 200
			for row in range(self.x-1,590,-1):
				for col in range(self.y-1, 200, -1):
					noisemap[row,col] = noisemap[row,col] + 200 
			

		def add_light(self, noisemap):
			for row in range(self.x):
				for col in range(self.y-1, 340, -1):
					value = noisemap[row,col]
					noisemap[row,col] = value - 100 

		def generate_bitmap(self):
				surface = pygame.Surface((self.x,self.y))
				bitmap = pygame.PixelArray(surface)
				for row in range(self.x-1,0,-1):
						for col in range(self.y-1, 0, -1):
							#	if self.image.get_at((row,col))[0] == 237:
							#			bitmap[row,col] = pygame.Color(255,255,255)
								if self.noisemap[row,col] < 5:
									bitmap[row,col] = pygame.Color(255,255,255)
								
				return bitmap
"""
		def flood_fill(self,stack,bitmap,surface):
				while len(stack) > 0:
						array = pygame.surfarray.array2d(surface)
						pt = stack.pop()
						x = pt[0]
						y = pt[1]
						if 
							bitmap[x,y] = pygame.Color(255,255,255)
							stack.append((x+1,y))
							stack.append((x-1,y))
							stack.append((x, y+1))
							stack.append((x,y-1))
						else:
							bitmap[x,y] = pygame.Color(0,0,0)
							continue
	"""						
				
				

#####################################################################################
def main():
		pygame.init()
		screen = pygame.display.set_mode((640,360))
		pygame.display.set_caption("Terrain_Testing")

		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((255,255,255))
		screen.blit(background, (0,0))
		terrain = Terrain(screen,"terrain_base.png")
	#m = generate_noisemap(screen)
	#start_array = generate_start_array(m, screen)
	#terrain_array = generate_terrain_array(start_array,screen)
	#terrain = pygame.PixelArray.make_surface(terrain_array)
		
		screen.blit(terrain.surface, (0,0))
		pygame.display.flip()
	
		allSprites = pygame.sprite.Group()
	
		keepGoing = True
		while(keepGoing):
				for event in pygame.event.get():
						if event.type == QUIT:
								keepGoing = False
				allSprites.clear(screen,background)
				allSprites.draw(screen)
				pygame.display.flip()	

#	background = pygame.Surface(screen.get_size())
#	background = background.convert()
#	background.fill((255,255,255))
#	screen.blit(background, (0,0))

if __name__=='__main__':
	main()	
	
	
