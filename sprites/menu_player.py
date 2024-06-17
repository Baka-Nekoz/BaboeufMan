import pygame
from pygame.locals import *
import math
from sprites import menuarm

class MenuPlayer(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.sprite_w = (self.game.width * 0.025) * 4.5
        self.sprite_h = (self.sprite_w/10*27)

        #chargement des images
        self.image_stand = pygame.image.load('assets/images/player_sprites/eggman_stand.png').convert_alpha()
        self.image_stand = pygame.transform.scale(self.image_stand, (self.sprite_w, self.sprite_h))

        self.image = self.image_stand
        self.rect = self.image.get_rect()
        
        self.rect.centerx = self.game.width * 0.3
        self.rect.y = self.game.height * 0.9 - self.sprite_h

        self.menuarm = menuarm.MenuArm(self.game, self.sprite_w, True)


    def update(self, mouse):
        self.image = self.image_stand

        flipped = mouse[0] < self.rect.centerx
        if flipped:
            self.image = pygame.transform.flip(self.image, True, False)
            

        #arm
        self.menuarm.update((self.rect.centerx, self.rect.centery), mouse, flipped)

        

