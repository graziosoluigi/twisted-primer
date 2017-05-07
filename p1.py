#	Luigi Grazioso & Aron Lam
#	May 5th, 2017
#	Twisted Pygame (player1.py)

import sys, pygame, os
from helper import *
from pygame.locals import *
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from threading import Thread


#Connection~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class GameConnection(Protocol):
	def __init__(self, gs):
		self.gs = gs

	def connectionMade(self):
		print "Player 1: Connection Made"
		self.t = Thread(target=self.gs.main, args=(self, )).start()

	def dataReceived(self, data):
		print "Data:", data
		if data == "quit":
			pygame.quit()
			reactor.stop()
			os._exit(1)


class GameConnectionFactory(Factory):
	def __init__(self, gs):
		self.myconn = GameConnection(gs)


	def buildProtocol(self, addr):
		return self.myconn

#GameSpace~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GameSpace:
	def main(self, conn):
		self.conn = conn
		pygame.init()

                #Screen, Background, and Goal
		self.size = self.width, self.height = 640, 420
		self.screen = pygame.display.set_mode(self.size)
                self.bgImage, self.bgRect = loadImage("background.jpg")
                w, h = self.bgImage.get_size()
                self.bgImage = pygame.transform.scale(self.bgImage, (int(w*.5), int(h*.5)))
                self.bgRect = self.bgImage.get_rect()
                self.bgRect.center = (320,210)
                
                self.goalImage, self.goalRect = loadImage("goal.png")
                gw, gh = self.goalImage.get_size()
                self.goalImage = pygame.transform.scale(self.goalImage, (int(gw*.55), int(gh*.55)))
                self.goalRect = self.goalImage.get_rect()
                self.goalRect.center = (320,270)

		#init all game objects (shooter and goalkeeper)
		self.clock = pygame.time.Clock()
                self.sprites = pygame.sprite.Group()
                self.ball = Ball(self)
                self.sprites.add(self.ball)

                self.scored = False
                

		pygame.key.set_repeat()


		while 1:
			self.clock.tick(60);
			for event in pygame.event.get():
				if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
					reactor.stop()
					pygame.quit()
					conn.transport.write("quit")
					os._exit(1)
				elif event.type == MOUSEBUTTONDOWN:
					print("Player 1: Mouse Click")
					conn.transport.write("Click on P1")

                        
			#self.screen.fill(self.skyblue);
                        self.screen.blit(self.bgImage, self.bgRect)
			self.screen.blit(self.ball.image, self.ball.rect)
                        self.screen.blit(self.goalImage, self.goalRect)
                        #self.sprites.update()
                        self.sprites.draw(self.screen)
			pygame.display.flip()

if __name__ == "__main__":
	gs = GameSpace();
	reactor.listenTCP(40025, GameConnectionFactory(gs))
	reactor.run()
