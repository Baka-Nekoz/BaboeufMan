import pygame
from pygame.locals import *
from sprites import player

class Lifebar():
    def __init__(self, game):
        self.game = game

    def update(self):
        self.coeff = 0.75
        self.bar = pygame.Rect(((0.5*self.game.width)-(((0.24*self.coeff)*self.game.width)//2)), ((0.1*self.coeff)*self.game.height), ((0.24*self.coeff)*self.game.width), ((0.095*self.coeff)*self.game.height))
        self.healthbar = pygame.Rect((((0.5+0.0215*self.coeff)*self.game.width)-(((0.24*self.coeff)*self.game.width)/2)), ((0.12*self.coeff)*self.game.height), ((self.game.player.health/100)*self.game.width*(0.2*self.coeff)), ((0.05*self.coeff)*self.game.height))
        
    def display_rect(self): 
        pygame.draw.rect(self.game.screen, (255,0,0), self.bar)
        pygame.draw.rect(self.game.screen, (0,255,0), self.healthbar)