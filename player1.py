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
		#print "Data:", data
		if data == "quit":
			pygame.quit()
			reactor.stop()
			os._exit(1)
		try:
			if self.gs.gloves != None and data.find("glove: ") != -1:
				tmp_str = data.split(" ")
				x = int(tmp_str[1])
				y = int(tmp_str[2])
				self.gs.gloves.move(x, y)
		except AttributeError:
			pass

                try:
                        if data.find("dec: ") != -1:
                                tmp_str = data.split(" ")
                                self.gs.ball.shot = int(tmp_str[1])


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

		#Background, screen, and Goal
		self.size = self.width, self.height = 640, 420
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption("Player 1 (Kicker)", "")
		self.bgImage, self.bgRect = loadImage("background.jpg")
		self.bgImage, self.bgRect = scaleImage(self.bgImage, 0.5)
		self.bgRect.center = (320,210)
		self.scoreboard = ScoreBoard(self)
		self.goalImage, self.goalRect = loadImage("goal.png")
		self.goalImage, self.goalRect = scaleImage(self.goalImage, 0.55)
		self.goalRect.center = (320,270)


		#init all game objects (shooter and goalkeeper)

		self.clock = pygame.time.Clock()
		self.sprites = pygame.sprite.Group()
                self.ball = Ball(self)
		self.gloves = Gloves(self)
		self.scoreboard = ScoreBoard(self)
                self.sprites.add(self.ball)
                self.sprites.add(self.gloves)

		#self.scored = False
		#self.score = [1, 2, 2, 0, 0]

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
					#print("Player 1: Mouse Click")
					#conn.transport.write("Click on P1")
					#print("Clicks on:", pygame.mouse.get_pos())
                                        if self.ball.shot == 0:
                                                self.ball.shot = 1
                                                self.ball.shotPosition = pygame.mouse.get_pos()
                                                
                                            
			self.scoreboard.tick()
                        self.ball.tick()

			#self.screen.blit(self.players.image, self.players.rect)
			self.screen.blit(self.bgImage, self.bgRect)
			self.screen.blit(self.ball.image, self.ball.rect)
                        self.screen.blit(self.goalImage, self.goalRect)
			self.screen.blit(self.scoreboard.image, self.scoreboard.rect)
                        self.screen.blit(self.scoreboard.shot1Image, self.scoreboard.shot1Rect)
			self.screen.blit(self.scoreboard.shot2Image, self.scoreboard.shot2Rect)
			self.screen.blit(self.scoreboard.shot3Image, self.scoreboard.shot3Rect)
			self.screen.blit(self.scoreboard.shot4Image, self.scoreboard.shot4Rect)
			self.screen.blit(self.scoreboard.shot5Image, self.scoreboard.shot5Rect)
			self.sprites.draw(self.screen)
			pygame.display.flip()

#Main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
	gs = GameSpace();
	reactor.listenTCP(40025, GameConnectionFactory(gs))
	reactor.run()
