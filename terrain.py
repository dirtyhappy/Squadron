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
# convolution kernels
smallBlur = numpy.ones((7,7), dtype="float") * (1.0/(7*7))			
largeBlur = numpy.ones((21,21), dtype="float") * (1.0/(21*21))
sharpen = numpy.array((
	[0,-1,0],
	[-1,5,-1],
	[0,-1,0]), dtype ="int")

#######################################################################################
#Terrain Class that randomly generates a bitmap for drawing the terrain		
class Terrain(pygame.sprite.Sprite):
		def __init__(self,screen):
			#	pygame.sprite.Sprite.__init__(self)
				self.screen = screen
				self.x,self.y = screen.get_size()
				self.generate_noisemap()
				self.bitmap = self.generate_bitmap(self.noisemap)
				self.surface = pygame.PixelArray.make_surface(self.bitmap)

		#generate and modify the noisemap of the terrain 		
		def generate_noisemap(self):
			self.noisemap = generate_perlin_noise_2d((self.x,self.y),(20,20))
			self.noisemap = self.noisemap * 255
			self.add_darkness(self.noisemap)
			self.add_light(self.noisemap)
			self.perform_convolutions()

		#perform specific convolutions on the noisemap
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
		
		#adjust the noisemap so certain sections will generate black pixels in the bitmap
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
			
		#adjust the noisemap so certain sections will generate white pixels in the bitmap
		def add_light(self, noisemap):
			for row in range(self.x):
				for col in range(self.y-1, 340, -1):
					value = noisemap[row,col]
					noisemap[row,col] = value - 100 

		#use the noisemap to generate the black and white bitmap for drawing the terrain
		def generate_bitmap(self, noisemap):
				surface = pygame.Surface((self.x,self.y))
				bitmap = pygame.PixelArray(surface)
				for row in range(self.x-1,0,-1):
						for col in range(self.y-1, 0, -1):
								if noisemap[row,col] < 1:
									bitmap[row,col] = pygame.Color(255,255,255)
								
				return bitmap

		def update(self):
			self.surface = pygame.PixelArray.make_surface(self.bitmap)

#############################################################################################################
