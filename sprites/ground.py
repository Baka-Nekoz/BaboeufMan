import pygame
from pygame.locals import *

class Ground:
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/images/ground_2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.game.width, self.game.height * 0.2))
        self.rect = self.image.get_rect()
        self.rect.y = self.game.height * 0.81

        self.level = self.game.height * 0.89