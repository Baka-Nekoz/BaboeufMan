import pygame
from pygame.locals import *

class Press:
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/images/press.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.game.width*0.7, self.game.height * 0.15))
        self.rect = self.image.get_rect()
        self.rect.center = (self.game.width/2,0)
        self.rect.y = self.game.height * 0.85

        self.level = self.game.height * 0.89