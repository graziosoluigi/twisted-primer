#       Luigi Grazioso & Aron Lam
#       May 5th, 2017
#       Twisted Pygame (helper.py)

import os
import pygame
import math
from pygame.compat import geterror
from pygame.locals import *

# Load an image and its rect and return tuple
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

# Scale an image and its rect and return tuple
def scaleImage(image, scale):
	w, h = image.get_size()
	image = pygame.transform.scale(image, (int(w*scale), int(h*scale)))
	return image, image.get_rect()

class Ball(pygame.sprite.Sprite):
        def __init__(self, gs):
		self.gs = gs
                pygame.sprite.Sprite.__init__(self)

                # defaultImage
                self.defaultImage = pygame.image.load("soccerball.png")
		self.defaultImage, self.defaultImageRect = scaleImage(self.defaultImage, 0.2)   

                # Image
                self.image, self.rect = loadImage("soccerball.png")
		self.image, self.rect = scaleImage(self.image, 0.2)
                self.rect.center = (320,390)
                self.display = pygame.display.get_surface()
                self.area = self.image.get_rect()
                
                # Properties
                self.position = (320, 390)
                self.speed = [0, 0]
                self.angle = 0
                self.shot = 0
                self.shot_result = 0
                self.shotPosition = 0, 0
                self.scale = 0.05
		self.prev_shotPos = 0, 0

                
        # Handle Aiming of ball to face mouse
        def tick(self):
                # Ball at Start Position
                if self.shot == 0:
                        x_m, y_m = pygame.mouse.get_pos()
                        (x_p, y_p) = self.rect.center
                
                        # Rotation
                        self.angle = 360 - math.degrees(math.atan2(y_m - y_p, x_m - x_p))            
                        self.image = pygame.transform.rotate(self.defaultImage, self.angle)

                        # Movement
                        self.rect = self.image.get_rect(center = self.rect.center)
                
                        string = "angle: " + str(self.angle) + " "
                        self.gs.conn.transport.write(string)
                # Taking shot
                else:
                        # calculate speed
                        self.speed = [(self.shotPosition[0]-320)/7.0, (self.shotPosition[1]-390)/7.0]

                        # moving ball to desired shot position
                        if self.rect.centery > self.shotPosition[1]:
                                origPos = self.rect.center
                                self.image, self.rect = scaleImage(self.defaultImage, 1-self.scale)
                                self.scale = self.scale + 0.05
                                self.rect.center = origPos
                                newRect = self.rect.move(self.speed)
                                self.rect = newRect

                        # send ball location to player2
                        string = "position: " + str(self.rect.centerx) + " " + str(self.rect.centery) + " "
                        self.gs.conn.transport.write(string)
        # Rotate ball to face mouse position
        def rotate(self):
                self.image = pygame.transform.rotate(self.defaultImage, self.angle)
                self.rect = self.image.get_rect(center = self.rect.center)

        # Determines shot result and moves ball for player 2
	def shot_fn(self, x, y):
		if self.prev_shotPos == (x, y) and self.shot_result == 0:
			if self.rect.left < 158 or self.rect.right > 485 or self.rect.top < 187 or self.rect.bottom > 362:
				self.shot_result = 2
			elif self.gs.gloves.rect.colliderect(self.rect):
				self.shot_result = 2
                        else:
				self.shot_result = 1
                        # send shot result to player 1
			self.gs.conn.transport.write("dec: " + str(self.shot_result) + " ")
                elif self.shot_result == 0:
			self.prev_shotPos = (x, y)
			origPos = self.rect.center
			self.image, self.rect = scaleImage(self.defaultImage, 1-self.scale)
			self.scale = self.scale + 0.05
			self.rect.center = (x, y)


class Gloves(pygame.sprite.Sprite):
	def __init__(self, gs):
		self.gs = gs
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("gloves.png")
		self.image, self.rect = scaleImage(self.image, .08)
		self.rect.center = (320, 210)

	def tick(self):
		'''Gloves tick:		-move gloves based on mouse
					-sends info to connection'''
	        self.rect.center = pygame.mouse.get_pos()
                # Send glove position to player 1
		string = "glove: "+str(self.rect.centerx)+" "+str(self.rect.centery)+" "
		self.gs.conn.transport.write(string)

	def move(self, x, y):
		self.rect.center = (x, y)


class ScoreBoard(pygame.sprite.Sprite):
	def __init__(self, gs):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load("score.png")
		self.image, self.rect = scaleImage(self.image, .3)
		self.rect.center = (320, 50)
		self.score = [0, 0, 0, 0, 0]
		self.shot_num = 0

        # Update scoreboard and decides winner if  game is over
	def tick(self):
		if self.gs.ball.shot_result != 0:
                        # game not over yet
		        if self.shot_num <= 4:
                                self.score[self.shot_num] = self.gs.ball.shot_result
                                if self.shot_num < 4:
                                        self.gs.resetBall()
                        # Game Over, tally up score and decide winner
                        if self.shot_num >= 4:
                                p1 = 0
                                p2 = 0
                                for i in self.score:
                                        if i == 1:
                                                p1 = p1 + 1
                                        else:
                                                p2 = p2 + 1
                                if p1 > p2:
                                        # display player 1 wins
                                        self.winImage, self.winRect = loadImage("Player1wins.png")
                                else:
                                        # display player 2 wins
                                        self.winImage, self.winRect = loadImage("Player2wins.png")
                                
                                self.winImage, self.winRect = scaleImage(self.winImage, .5)
                                self.winRect.center = (320, 210)

                        # Increment shot number
                        self.shot_num = self.shot_num + 1

                # display correct images on scoreboard
		if self.score[0] == 1:
			self.shot1Image = pygame.image.load("soccerball.png")
			self.shot1Image, self.shot1Rect = scaleImage(self.shot1Image, .16)
		elif self.score[0] == 2:
			self.shot1Image = pygame.image.load("miss.png")
			self.shot1Image, self.shot1Rect = scaleImage(self.shot1Image, .17)
		elif self.score[0] == 0:
			self.shot1Image = pygame.image.load("transparent_ball.png")
			self.shot1Image, self.shot1Rect = scaleImage(self.shot1Image, .08)
		self.shot1Rect.center = (265, 47)

		if self.score[1] == 1:
			self.shot2Image = pygame.image.load("soccerball.png")
			self.shot2Image, self.shot2Rect = scaleImage(self.shot2Image, .16)
		elif self.score[1] == 2:
			self.shot2Image = pygame.image.load("miss.png")
			self.shot2Image, self.shot2Rect = scaleImage(self.shot2Image, .17)
		elif self.score[1] == 0:
			self.shot2Image = pygame.image.load("transparent_ball.png")
			self.shot2Image, self.shot2Rect = scaleImage(self.shot2Image, .08)
		self.shot2Rect.center = (315, 47)

		if self.score[2] == 1:
			self.shot3Image = pygame.image.load("soccerball.png")
			self.shot3Image, self.shot3Rect = scaleImage(self.shot3Image, .16)
		elif self.score[2] == 2:
			self.shot3Image = pygame.image.load("miss.png")
			self.shot3Image, self.shot3Rect = scaleImage(self.shot3Image, .17)
		elif self.score[2] == 0:
			self.shot3Image = pygame.image.load("transparent_ball.png")
			self.shot3Image, self.shot3Rect = scaleImage(self.shot3Image, .08)
		self.shot3Rect.center = (365, 47)

		if self.score[3] == 1:
			self.shot4Image = pygame.image.load("soccerball.png")
			self.shot4Image, self.shot4Rect = scaleImage(self.shot4Image, .16)
		elif self.score[3] == 2:
			self.shot4Image = pygame.image.load("miss.png")
			self.shot4Image, self.shot4Rect = scaleImage(self.shot4Image, .17)
		elif self.score[3] == 0:
			self.shot4Image = pygame.image.load("transparent_ball.png")
			self.shot4Image, self.shot4Rect = scaleImage(self.shot4Image, .08)
		self.shot4Rect.center = (415, 47)

		if self.score[4] == 1:
			self.shot5Image = pygame.image.load("soccerball.png")
			self.shot5Image, self.shot5Rect = scaleImage(self.shot5Image, .16)
		elif self.score[4] == 2:
			self.shot5Image = pygame.image.load("miss.png")
			self.shot5Image, self.shot5Rect = scaleImage(self.shot5Image, .17)
		elif self.score[4] == 0:
			self.shot5Image = pygame.image.load("transparent_ball.png")
			self.shot5Image, self.shot5Rect = scaleImage(self.shot5Image, .08)
		self.shot5Rect.center = (465, 47)

        # Resets scoreboard (game)
        def reset(self):
                self.score = [0, 0, 0, 0, 0]
                self.shot_num = 0
                del self.winImage
                del self.winRect

 






