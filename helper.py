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
                # default Image
                self.defaultImage = pygame.image.load("soccerball.png")
                dw, dh = self.defaultImage.get_size()
                self.defaultImage = pygame.transform.scale(self.defaultImage, (int(dw*.2), int(dh*.2)))
                # Image
                self.image, self.rect = loadImage("soccerball.png")
                w, h = self.image.get_size()
                self.image = pygame.transform.scale(self.image, (int(w*.2), int(h*.2)))
                self.rect = self.image.get_rect()
                self.rect.center = (320,400)
                self.display = pygame.display.get_surface()
                self.area = self.image.get_rect()
                
                self.speed = 5
                self.reset()

        #def update(self):
                #newRect = self.rect.move(self.position)
                #self.rect = newRect
                #pygame.event.pump()


        def reset(self):
                self.position = [320,400]
