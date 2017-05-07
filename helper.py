import os
import pygame
import math
from pygame.compat import geterror
from pygame.locals import *

# For the objects
def loadImage(name, colorkey = None):
        try:
                image = pygame.image.load(name)
        except pygame.error:
                print ("Failed to load image: ", fullname)
                raise SystemExit(str(geterror()))

        if image.get_alpha is None:
                image = image.convert()
        else:
                image = image.convert_alpha()
        return image, image.get_rect()

# 2nd function for explosion effects
def loadImage2(name):
        try:
                image = pygame.image.load(name)
        except pygame.error:
                print ("Failed to load image: ", fullname)
                raise SystemExit(str(geterror()))

        if image.get_alpha is None:
                image = image.convert()
        else:
                image = image.convert_alpha()
        return image

def scaleImage(image, scale):
	w, h = image.get_size()
	image = pygame.transform.scale(image, (int(w*scale), int(h*scale)))
	return image, image.get_rect()

class Ball(pygame.sprite.Sprite):
        def __init__(self, environment):
                pygame.sprite.Sprite.__init__(self)
                # default Image
                self.defaultImage = pygame.image.load("soccerball.png")
		self.defaultImage = scaleImage(self.defaultImage, 0.2)
                # Image
                self.image, self.rect = loadImage("soccerball.png")
		self.image, self.rect = scaleImage(self.image, 0.2)
                self.rect.center = (320,390)
                self.display = pygame.display.get_surface()
                self.area = self.image.get_rect()
                
                self.speed = 5
                self.reset()
                self.angle = 0
        # Handle Aiming of ball to face mouse
        
        #def tick(self):
                #newRect = self.rect.move(self.position)
                #self.rect = newRect
                #pygame.event.pump()


        def reset(self):
                self.position = [320,400]


class Gloves(pygame.sprite.Sprite):
	def __init__(self, gs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("gloves.png")
		self.image, self.rect = scaleImage(self.image, .1)
		self.rect.center = (320, 210)

	def tick(self, gs):
		'''Gloves tick:		-move gloves based on mouse
					-sends info to connection'''
		gs.count = gs.count + 1
		self.rect.center = pygame.mouse.get_pos()
		#if gs.count > 5 :
		string = "glove: "+str(self.rect.centerx)+" "+str(self.rect.centery)
		gs.count = 0
		gs.conn.transport.write(string)

	def move(self, x, y):
		self.rect.center = (x, y)





