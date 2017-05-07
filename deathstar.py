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

# For the explosion
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

# Initialize the game space
class gameSpace:
        def main(self):
                pygame.init()
                # Initialize Window
                self.size = self.width, self.height = 640, 420
                self.black = 0, 0, 0
                self.screen = pygame.display.set_mode(self.size)
                pygame.display.set_caption("Deathstar")

                self.background = pygame.Surface(self.screen.get_size())
                self.background = self.background.convert()
                self.background.fill((self.black))

                # Initialize game objects
                self.player = Player(self)
                self.enemy = Enemy(self)
                self.clock = pygame.time.Clock()
                self.sprites = pygame.sprite.Group()
                self.earth = pygame.sprite.RenderPlain(self.enemy)
                self.deathstar = pygame.sprite.RenderPlain(self.player)
                self.sprites.add(self.earth)
                self.sprites.add(self.deathstar)
                self.lasers = pygame.sprite.Group()
                self.running = True
                self.victory = False

                self.screen.blit(self.background, (0,0))
                pygame.display.update()

                # Game  loop
                while self.running:
                        self.clock.tick(60)
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        self.running = False
                                elif event.type == KEYDOWN:
                                        self.player.move(event)
                                elif event.type == MOUSEMOTION:
                                        xMouse, yMouse = event.pos
                                        self.player.rotate(xMouse, yMouse)
                                elif event.type == MOUSEBUTTONDOWN:
                                        if self.victory == True:
                                                self.running = False
                                        pos = pygame.mouse.get_pos()
                                        laser = Laser([pos[0] / 10.0, pos[1] / 10.0])
                                        self.player.fire(laser)
                                        self.lasers.add(laser)
                                        lSprite = pygame.sprite.RenderPlain(laser)
                                        self.sprites.add(lSprite)
                        # Collision checking 
                        for laser in self.lasers:
                                rect_hit = pygame.sprite.spritecollide(laser, self.earth, False)
                                for item in rect_hit:
                                        self.lasers.remove(laser)
                                        self.enemy.endGame()
                                        explosion = Explosion(self)
                                        explosionSprite = pygame.sprite.RenderPlain(explosion)
                                        self.sprites.add(explosionSprite)
                                        self.victory = True

                                if laser.rect.y < -10:
                                        self.lasers.remove(laser)

                        # Update Window
                        self.screen.fill(self.black)
                        self.sprites.update()
                        self.sprites.draw(self.screen)
                        pygame.display.update()

class Player(pygame.sprite.Sprite):
        def __init__(self, environment):
                pygame.sprite.Sprite.__init__(self)
                self.defaultImage = pygame.image.load("/home/scratch/paradigms/deathstar/deathstar.png").convert_alpha()
                self.image, self.rect = loadImage("/home/scratch/paradigms/deathstar/deathstar.png")
                self.display = pygame.display.get_surface()
                self.area = self.image.get_rect()
                self.angle = 0
                self.speed = 4
                self.reset()

        def reset(self):
                self.position = [0, 0]

        def move(self, event):
                #left
                if event.unicode == "a":            
                        self.position[0] -= self.speed
                        self.update()
                # up
                elif event.unicode == "w":                  
                        self.position[1] -= self.speed
                        self.update()
                # right
                if event.unicode == "d":
                        self.position[0] += self.speed
                        self.update()
                # down
                elif event.unicode == "s":                  
                        self.position[1] += self.speed
                        self.update()

        # Handle Rotation of death star to face mouse
        def rotate(self, xMouse, yMouse):
                xPlayer, yPlayer = self.rect.centery, self.rect.centerx
                # using atan to calculate angle
                self.angle = 360 - math.degrees(math.atan2(yMouse - yPlayer, xMouse - xPlayer))
                self.image = pygame.transform.rotate(self.defaultImage, self.angle)
                self.rect = self.image.get_rect(center = self.rect.center)

        def fire(self, laser):
                laser.rect.x = self.rect.centerx
                laser.rect.y = self.rect.centery
        
        def update(self):
                newRect = self.rect.move(self.position)
                self.rect = newRect
                pygame.event.pump()

class Enemy(pygame.sprite.Sprite):
        def __init__(self, environment):
                pygame.sprite.Sprite.__init__(self)
                self.image, self.rect = loadImage("/home/scratch/paradigms/deathstar/globe.png")
                self.rect.centerx = environment.width
                self.rect.centery = environment.height

        def endGame(self):
                print("GAME OVER\n")
                self.image.fill((0, 0, 0))

        def update(self):
                self.rect.x = self.rect.x
                self.rect.y = self.rect.y

class Laser(pygame.sprite.Sprite):
        def __init__(self, speed):
                pygame.sprite.Sprite.__init__(self)
                self.speed = speed
                self.image, self.rect = loadImage("/home/scratch/paradigms/deathstar/laser2.png")

        def update(self):
                self.rect = self.rect.move(self.speed)


class Explosion(pygame.sprite.Sprite):
        def __init__(self, environment):
                pygame.sprite.Sprite.__init__(self)
                
                # Variables
                self.index = 0
                self.images = []
                self.animate()
                self.image = self.images[self.index]
                self.rect = self.image.get_rect()
                self.rect.bottomright = [environment.width, environment.height]

        def animate(self):
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames000a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames001a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames002a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames003a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames004a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames005a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames006a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames007a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames008a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames009a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames010a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames011a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames012a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames013a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames014a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames015a.png"))
                self.images.append(loadImage2("/home/scratch/paradigms/deathstar/explosion/frames016a.png"))

        def update(self):
                self.index += 1
                if self.index >= len(self.images):
                        self.image.fill((0,0,0))
                else:
                        self.image = self.images[self.index]

if __name__ == "__main__":
        gs = gameSpace()
        gs.main()
