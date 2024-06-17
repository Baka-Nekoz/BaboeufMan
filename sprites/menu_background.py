import pygame
from pygame.locals import *
import math

class MenuBackground:
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(0, 0, self.game.width, self.game.height)

        self.image_sunset = self.game.assets['sunset']
        self.image_sunset = pygame.transform.scale(self.image_sunset, (self.game.width * 0.8, self.game.height))
        self.rect_sunset = self.image_sunset.get_rect()
        

        self.color = [0,0,255]

        
    def display(self):
        pygame.draw.rect(self.game.screen, self.color, self.rect)
        self.game.screen.blit(self.image_sunset, self.rect_sunset)