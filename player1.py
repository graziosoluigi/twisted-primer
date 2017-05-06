#	Luigi Grazioso & Aron Lam
#	May 5th, 2017
#	Twisted Pygame (player1.py)

import sys, pygame
from pygame.locals import *
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from threading import Thread


#Connection~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class GameConnection(Protocol):
	def connectionMade(self):
		print "Player 1: Connection Made"

	def dataReceived(self, data):
		print "Player 1: Got Data", data


class GameConnectionFactory(Factory):
	def __init__(self):
		self.myconn = GameConnection()

	def buildProtocol(self, addr):
		return self.myconn

#GameSpace~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GameSpace:
	def main(self):
		pygame.init()
		self.size = self.width, self.height = 640, 420
		self.black = 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)

		reactor.run()

		#init all game objects (shooter and goalkeeper)

		self.clock = pygame.time.Clock()

		pygame.key.set_repeat()

		t = Thread(target=reactor.run, args=(False, ))
		t.start()
		while 1:
			self.clock.tick(60);
			for event in pygame.event.get():
				if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
					print("QUIT")
					t.join()
					reactor.stop()
					sys.exit()

				elif event.type == MOUSEBUTTONDOWN:
					print("Player: Mouse Click")


			self.screen.fill(self.black);
			#self.screen.blit(self.players.image, self.players.rect)

			pygame.display.flip()


if __name__ == "__main__":
	reactor.listenTCP(40025, GameConnectionFactory())
	gs = GameSpace();
	gs.main();
	#reactor.run()
