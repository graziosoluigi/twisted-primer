#	Luigi Grazioso & Aron Lam
#	May 5th, 2017
#	Twisted Pygame (player2.py)

import sys, pygame, os
from helper import *
from pygame.locals import *
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from threading import Thread
import time



#Connection~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class GameConnection(Protocol):
	def __init__(self, gs):
		self.gs = gs

	def connectionMade(self):
		#gs.main is run on a separate thread so it doesnt intervene with reactor
		self.t = Thread(target=gs.main, args=(self, )).start()
		

	def dataReceived(self, data):
		if data == "quit":
			pygame.quit()
			reactor.stop()
			os._exit(1)
		try:
			#Gets Data for ball rotation from P1 aiming
			if data.find("angle: ") != -1:
				tmp_str = data.split(" ")
				self.gs.ball.angle = float(tmp_str[1])
				self.gs.ball.rotate()
		except AttributeError:
			pass
		try:
			#updates balls position on this screen based on P1 ball movement
			if data.find("position: ") != -1:
				tmp_str = data.split(" ")
				self.gs.ball.shot_fn(int(tmp_str[1]), int(tmp_str[2]))
		except ValueError:
			pass
		if data == "RESET":
			self.gs.resetBall()
			self.gs.scoreboard.reset()


class GameConnectionFactory(ClientFactory):
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
		pygame.display.set_caption("Player 2 (Goalkeeper)", "")
		self.bgImage, self.bgRect = loadImage("background.jpg")
		self.bgImage, self.bgRect = scaleImage(self.bgImage, 0.5)
		self.bgRect.center = (320,210)

		self.goalImage, self.goalRect = loadImage("goal.png")
		self.goalImage, self.goalRect = scaleImage(self.goalImage, 0.55)
		self.goalRect.center = (320,270)

		#init all game objects
		self.clock = pygame.time.Clock()
		self.sprites = pygame.sprite.Group()
                self.ball = Ball(self)
		self.gloves = Gloves(self)
		self.scoreboard = ScoreBoard(self)
                self.sprites.add(self.ball)
		self.sprites.add(self.gloves)

		pygame.key.set_repeat()

		while 1:
			self.clock.tick(60);
			#print self.count
			for event in pygame.event.get():
				#handles user quiting the game and it quits on both windows(by sending message in conn)
				if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
					self.conn.transport.write("quit")
					reactor.stop()
					pygame.quit()
					os._exit(1)
				#resets game in current window and sends message to reset in other window
				elif event.type == KEYDOWN and event.key == K_SPACE and self.scoreboard.shot_num > 4:
					self.resetBall()
					self.scoreboard.reset()
					self.conn.transport.write("RESET")
					time.sleep(.1)

			#tick function to move gloves according to mouse
			self.gloves.tick()
			#tick function to update scoreboard according to score (also check game results)
			self.scoreboard.tick()


			#Display objects on screen
			self.screen.blit(self.bgImage, self.bgRect)
			self.screen.blit(self.ball.image, self.ball.rect)
                        self.screen.blit(self.goalImage, self.goalRect)
			self.screen.blit(self.scoreboard.image, self.scoreboard.rect)
			self.screen.blit(self.scoreboard.shot1Image, self.scoreboard.shot1Rect)
			self.screen.blit(self.scoreboard.shot2Image, self.scoreboard.shot2Rect)
			self.screen.blit(self.scoreboard.shot3Image, self.scoreboard.shot3Rect)
			self.screen.blit(self.scoreboard.shot4Image, self.scoreboard.shot4Rect)
			self.screen.blit(self.scoreboard.shot5Image, self.scoreboard.shot5Rect)
			try:
				self.screen.blit(self.scoreboard.winImage, self.scoreboard.winRect)
			except AttributeError:
				pass
			self.sprites.draw(self.screen)
			pygame.display.flip()

	#used to reset the ball position so that shooter can shoot again, or to restart game
	def resetBall(self):
		self.sprites.remove(self.ball)
		del self.ball
		self.ball = Ball(self)
		self.sprites.add(self.ball)



if __name__ == "__main__":
	gs = GameSpace();
	reactor.connectTCP("ash.campus.nd.edu", 40025, GameConnectionFactory(gs))
	reactor.run()

