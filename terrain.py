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
def load_png(name):
	#load a .png and return a pygame.image
	fullname = os.path.join('assets', name) 
	try:
		image = pygame.image.load(fullname)
		if image.get_alpha() is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	except pygame.error as  message:
		print ("Cannot load image: ", fullname)
		raise SystemExit(message) 
	return image, image.get_rect()	
    
#######################################################################################
    
class Terrain(pygame.sprite.Sprite):
    def __init__(self,screen,base_image):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x,self.y = screen.get_size()
        self.image,self.rect = load_png(base_image)
        self.noisemap = generate_perlin_noise_2d((self.x,self.y),(10,10))
        self.bitmap = self.generate_bitmap()
        self.surface = pygame.PixelArray.make_surface(self.bitmap)
        
            
        
    def get_background_points(self):
        bg_list = []
        for row in range(self.x):
            for col in range(self.y):
                if (self.image.get_at((row,col))[0] == 0):
                    bg_list.append((row,col))
        return bg_list
        
    def get_foreground_points(self):
        fg_list = []
        for row in range(self.x):
            for col in range(self.y):
                if(self.image.get_at((row,col))[0] == 63):
                    fg_list.append((row,col))
        return fg_list
                
                
    def generate_bitmap(self):
        surface = pygame.Surface((self.x,self.y))
        bitmap = pygame.PixelArray(surface)
        for row in range(self.x):
            for col in range(self.y):
                if self.image.get_at((row,col))[0] == 237:
                    bitmap[row,col] = pygame.Color(255,255,255)
                if self.noisemap[row,col] < 0.07:
                    if self.image.get_at((row,col))[0] == 63:
                        bitmap[row,col] = pygame.Color(255,255,255)
                    elif self.image.get_at((row,col))[0] == 0:
                        bitmap[row,col] = pygame.Color(0,0,0)
                    
               
        return bitmap

#####################################################################################
def main():
    pygame.init()
    screen = pygame.display.set_mode((640,360))
    pygame.display.set_caption("Terrain_Testing")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
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
    
    print(terrain.image.get_at((320,359)))
	
if __name__=='__main__':
	main()	
	
	
