#!/usr/bin/python
#####################################################################################
try:
	import sys
	import pygame
	from scipy import signal	
	from pygame.locals import *
	import numpy
	from lib.perlin2d import generate_perlin_noise_2d
except ImportError as err:
	print("Could not load module: ", err)
	sys.exit(2)

#####################################################################################
	# Constants
#FRAME_RATE = 30

#####################################################################################

smallBlur = numpy.ones((7,7), dtype="float") * (1.0/(7*7))			
largeBlur = numpy.ones((21,21), dtype="float") * (1.0/(21*21))
sharpen = numpy.array((
	[0,-1,0],
	[-1,5,-1],
	[0,-1,0]), dtype ="int")

#######################################################################################
		
class Terrain(pygame.sprite.Sprite):
		def __init__(self,screen):
				pygame.sprite.Sprite.__init__(self)
				self.screen = screen
				self.x,self.y = screen.get_size()
				self.generate_noisemap()
				self.bitmap = self.generate_bitmap(self.noisemap)
				self.surface = pygame.PixelArray.make_surface(self.bitmap)
				
		def generate_noisemap(self):
			self.noisemap = generate_perlin_noise_2d((self.x,self.y),(20,20))
			self.noisemap = self.noisemap * 255
			self.add_darkness(self.noisemap)
			self.add_light(self.noisemap)
			self.perform_convolutions()

		def perform_convolutions(self):
			local_largeBlur = numpy.ones((21,21), dtype="float") * (1.0/(21*21))
			local_sharpen = numpy.array((
				[0,-1,0],
				[-1,5,-1],
				[0,-1,0]), dtype ="int")
			self.noisemap = signal.convolve2d(self.noisemap, local_largeBlur, 'same')
			self.noisemap = signal.convolve2d(self.noisemap, local_largeBlur, 'same')
			self.noisemap = signal.convolve2d(self.noisemap, local_largeBlur, 'same')
			self.noisemap = signal.convolve2d(self.noisemap, local_largeBlur, 'same')
			self.noisemap = signal.convolve2d(self.noisemap, local_sharpen, 'same')

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

		def generate_bitmap(self, noisemap):
				surface = pygame.Surface((self.x,self.y))
				bitmap = pygame.PixelArray(surface)
				for row in range(self.x-1,0,-1):
						for col in range(self.y-1, 0, -1):
							#	if self.image.get_at((row,col))[0] == 237:
							#			bitmap[row,col] = pygame.Color(255,255,255)
								if noisemap[row,col] < 1:
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
"""def main():
		pygame.init()
		screen = pygame.display.set_mode((640,360))
		pygame.display.set_caption("Terrain_Testing")

		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((255,255,255))
		screen.blit(background, (0,0))
		terrain = Terrain(screen)
		
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


if __name__=='__main__':
	main()	
"""	
	
