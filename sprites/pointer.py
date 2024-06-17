import pygame
from pygame.locals import *

class Pointer:
    def __init__(self, game, mouse):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/images/viseur.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.game.width/16 * 0.5, self.game.height/9 * 0.5))
        self.rect = self.image.get_rect()
        
    
    def update(self, mouse):
        self.rect.center = mouse