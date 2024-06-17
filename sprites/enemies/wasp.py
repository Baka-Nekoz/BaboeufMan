import pygame
from pygame.locals import *
from random import randint
import math

class wasp(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)

        self.sprite_w = self.game.width * 0.025
        self.sprite_h = self.sprite_w/10*27

        self.wasp1 = self.game.assets['wasp1']
        self.wasp2 = self.game.assets['wasp2']

        self.image_wasp1 = pygame.transform.scale(self.image_wasp1, (self.sprite_w, self.sprite_h))
        self.image_wasp2 = pygame.transform.scale(self.image_wasp2, (self.sprite_w, self.sprite_h))

        self.image = self.image_stand
        self.rect = self.image.get_rect()


        if randint(0, 1):
            self.rect.centerx = - 0.1 * self.game.width
            self.rect.y = 0.8 * self.game.height - self.sprite_h
            self.flipped = False

        else:
            self.rect.centerx = 1.1 * self.game.width
            self.rect.y = 0.8 * self.game.height - self.sprite_h
            self.flipped = True

        self.x_vel = 0
        self.y_vel = 0
        self.vel_cap = 1

        self.walking_since = 0
        self.health = 100
        

    def update(self, player_pos):
        
        if self.rect.centerx > player_pos[0]: # joueur à gauche
            if self.x_vel > - self.vel_cap:
                self.x_vel -= 1
                self.flipped = False
        elif self.rect.centerx < player_pos[0]: # joueur à droite
            if self.x_vel < self.vel_cap:
                self.x_vel += 1
                self.flipped = True
        else:
            if self.x_vel > 0:
                self.x_vel -= 1
            elif self.x_vel < 0:
                self.x_vel += 1


        #change frame
        if not self.x_vel == 0:
            self.walking_since += 1
            frame = math.floor(self.walking_since / 20 % 4)
            if frame == 0:
                self.image = self.image_walk1
            elif frame == 1:
                self.image = self.image_stand
            elif frame == 2:
                self.image = self.image_walk3
            else:
                self.image = self.image_stand

        else:
            self.walking_since = 0
            self.image = self.image_stand



        self.y_vel += 1

        if self.rect.y + self.sprite_h + self.y_vel > self.game.ground.level: #fast ground collision (à changer) (ou pas)
            self.rect.y = self.game.ground.level - self.sprite_h
            self.y_vel = 0


        vel = (self.x_vel, self.y_vel)
        self.rect = self.rect.move(vel)


        self.flipped = player_pos[0] < self.rect.centerx

        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)

        

        self.arm.update(self.rect.center, player_pos, self.flipped, vel)

        if pygame.sprite.spritecollide(self, self.game.player_bullets, True):
            
            self.health -= 5

        if self.health <= 0:
                self.arm.kill()
                self.kill()
