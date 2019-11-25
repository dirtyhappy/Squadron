#!/usr/bin/python
#####################################################################################
try:
	import sys
	import pygame
	import os
	from pygame.locals import *
	from random import seed
	from random import randint
	import numpy
	from lib.perlin2d import generate_perlin_noise_2d
except ImportError as err:
	print("Could not load module: ", err)
	sys.exit(2)

#####################################################################################
	# Constants
FRAME_RATE = 30

#####################################################################################
def generate_noisemap(screen):
	x,y = screen.get_size() #get dimensions of the screen
#	bitmap = [[0 for i in range(x)] for j in range (y)] # create 2D array
	noisemap = generate_perlin_noise_2d((x,y),(10,10))
	return noisemap	

def generate_start_array(noisemap,screen):
	x,y = screen.get_size()
	for row in range(99,(x-101)):
		for col in range(199,y):
			noisemap[row,col] = 0
	return noisemap

def get_fill_points(noisemap, screen):
	x,y = screen.get_size()
def generate_terrain_array(noisemap, screen):
	x,y = screen.get_size()
	surface = pygame.Surface((x,y))
	terrain_array = pygame.PixelArray(surface) 
	for row in range (x):
		for col in range(y):
			if row >= 49 and row <=(x-51):
				if col >=49:
					if noisemap[row,col] < 0.07:
						terrain_array[row,col] = pygame.Color(255,255,255)
					else:	
						terrain_array[row,col] = pygame.Color(0,0,0)
				else: 
					terrain_array[row,col] = pygame.Color(0,0,0)
			else:
				terrain_array[row,col] = pygame.Color(0,0,0)
	return terrain_array
			
#####################################################################################
def main():
	pygame.init()
	screen = pygame.display.set_mode((640,360))
	pygame.display.set_caption("Terrain_Testing")
	
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0,0,0))
	screen.blit(background, (0,0))
	m = generate_noisemap(screen)
	start_array = generate_start_array(m, screen)
	terrain_array = generate_terrain_array(start_array,screen)
	terrain = pygame.PixelArray.make_surface(terrain_array)
	screen.blit(terrain,(0,0))
	
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
	
	
