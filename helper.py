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

class Ball(pygame.sprite.Sprite):
        def __init__(self, environment):
                pygame.sprite.Sprite.__init__(self)
                self.defaultImage = pygame.image.load("soccerball.png")
                self.image, self.rect = loadImage("soccerball.png")
                self.display = pygame.display.get_surface()
                self.area = self.image.get_rect()
                
                self.speed = 5

        def update(self):
                self.rect = self.rect.move(self.speed)
