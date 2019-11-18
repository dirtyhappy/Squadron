#!/usr/bin/python
############################################################################################################
try:
	import sys
	import os
	import pygame
	from pygame.locals import *
except ImportError as err:
	print("could not load module: " ,err)
	sys.exit(2)
############################################################################################################
# Constants
FRAME_RATE = 30

###########################################################################################################
def load_png(name):
	#load an image and return a pygame.image
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
############################################################################################################
class Soldier(pygame.sprite.Sprite):
	def __init__(self,name,image_name):
		pygame.sprite.Sprite.__init__(self)
		self.name = name
		self.image, self.rect = load_png(image_name)
		self.image = self.image.convert()
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.x = 0
		self.rect.y = 0 
		self.dx = 0 
		self.dy = 0	
		
	def update(self):
		self.rect.centerx += self.dx
		self.rect.centery -= self.dy

	def move_left(self):
		self.dx = -10
		self.state = "moveleft"
	
	def move_right(self):
		self.dx = 10
		self.state = "moveright"

	def move_up(self):
		self.dy = 5
		self.state = "moveup"

	def move_down(self):
		self.dy = -5
		self.state = "movedown"

	
	
############################################################################################################	 
def main():
	#Initialize Screen
	pygame.init()
	screen = pygame.display.set_mode((640,380))
	pygame.display.set_caption("Squadron")
	
	#Fill Background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0,0,0))
	screen.blit(background, (0,0))
	
	#Initialize player
	player = Soldier("Bob", "red_square.png")	
	background.blit(player.image, (0,0))
	allSprites = pygame.sprite.RenderUpdates(player)

	#Initialize clock
	clock = pygame.time.Clock()
	keepGoing = True

	#Game Loop
	while keepGoing:
			clock.tick(FRAME_RATE)

			for event in pygame.event.get():
					if event.type == QUIT:
							keepGoing = False	
					elif event.type == KEYDOWN:
						if event.key == K_RIGHT:
							player.move_right()
						if event.key == K_LEFT:
							player.move_left()
						if event.key == K_UP:
							player.move_up()
					elif event.type == KEYUP:
						if event.key == K_RIGHT or K_LEFT or K_UP:
							player.state = "still"	
			allSprites.clear(screen, background)
			allSprites.update()
			allSprites.draw(screen)
			pygame.display.flip()
if __name__=='__main__' : main()

