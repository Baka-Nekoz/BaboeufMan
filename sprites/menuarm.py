import pygame
from pygame.locals import *
import math
from sprites import bullet, bazooka_bullet
import time

class MenuArm(pygame.sprite.Sprite):
    def __init__(self, game, player_w, is_player):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.is_player = is_player
        
        self.player_w = player_w

        self.sprite_w = player_w / 10 * 23
        self.sprite_h = self.sprite_w

        self.angle = 0

        self.last_shot = time.time()

        #load assets
        if is_player:
            self.image_pistol = pygame.image.load('assets/images/player_sprites/eggarm_pistol.png').convert_alpha()
            self.image_ak = pygame.image.load('assets/images/player_sprites/eggarm_ak.png').convert_alpha()
            self.image_bazooka = pygame.image.load('assets/images/player_sprites/eggarm_bazooka.png').convert_alpha()

            self.image_pistol = pygame.transform.scale(self.image_pistol, (self.sprite_w, self.sprite_h))
            self.image_ak = pygame.transform.scale(self.image_ak, (self.sprite_w, self.sprite_h))
            self.image_bazooka = pygame.transform.scale(self.image_bazooka, (self.sprite_w, self.sprite_h))

            self.weapon = 0
            self.shoot_delay = 0.6
            self.image = self.image_pistol

        self.rect = self.image.get_rect()


    def update(self, pos, target, flipped):
        
        x_diff = pos[0] - target[0]
        y_diff = pos[1] - target[1]


        offsetx = self.player_w*0.12
        offsety = self.player_w*(2/27)

        if flipped:
            x_diff = - x_diff
            offsetx = -offsetx

        if x_diff == 0 and y_diff >= 0:
            self.angle = 90
        elif x_diff == 0 and y_diff < 0:
            self.angle = -90
        else:
            self.angle = - math.degrees(math.atan(y_diff/x_diff))
            
        
        self.rect.center = (pos[0] - offsetx, pos[1] - offsety)
        
        

        if self.is_player:
            self.weapon = (self.weapon - self.game.scroll) % 3

            if self.weapon == 0:
                self.image = self.image_pistol
                self.shoot_delay = 0.6
            elif self.weapon == 1:
                self.image = self.image_ak
                self.shoot_delay = 0.1
            else:
                self.image = self.image_bazooka
                self.shoot_delay = 2.4
        
        else:
            self.image = self.image_pistol


        self.image, self.rect = self.rot_center()
        if flipped:
            self.image = pygame.transform.flip(self.image, True, False)

        
    def rot_center(self):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(self.image, self.angle)
        rot_rect = rot_image.get_rect(center=self.rect.center)
        return rot_image,rot_rect
