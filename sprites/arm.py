import pygame
from pygame.locals import *
import math
from sprites import bullet, bazooka_bullet, weapons
import time

class Arm(pygame.sprite.Sprite):
    def __init__(self, game, player_w):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        
        self.player_w = player_w

        self.sprite_w = player_w / 10 * 23
        self.sprite_h = self.sprite_w

        self.angle = 0

        #load assets
        self.image_pistol = pygame.image.load('assets/images/player_sprites/eggarm_pistol.png').convert_alpha()
        self.image_ak = pygame.image.load('assets/images/player_sprites/eggarm_ak.png').convert_alpha()
        self.image_bazooka = pygame.image.load('assets/images/player_sprites/eggarm_bazooka.png').convert_alpha()

        self.image_pistol = pygame.transform.scale(self.image_pistol, (self.sprite_w, self.sprite_h))
        self.image_ak = pygame.transform.scale(self.image_ak, (self.sprite_w, self.sprite_h))
        self.image_bazooka = pygame.transform.scale(self.image_bazooka, (self.sprite_w, self.sprite_h))

        self.weapon1 = weapons.Pistol(self.game, player_w)
        self.weapon2 = weapons.Grenade_Launcher(self.game, player_w)
        self.weapon3 = weapons.Flamethrower(self.game, player_w)

        self.weapon_nbr = 0
        self.weapon = self.weapon1
        self.image = self.weapon.image


        self.rect = self.image.get_rect()


    def update(self, pos, target, flipped, vel):
        
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
        
        

        self.weapon_nbr = (self.weapon_nbr - self.game.scroll) % 3

        if self.weapon_nbr == 0:
            self.weapon = self.weapon1
        elif self.weapon_nbr == 1:
            self.weapon = self.weapon2
        else:
            self.weapon = self.weapon3

        self.image = self.weapon.image


        self.image, self.rect = self.rot_center()
        if flipped:
            self.image = pygame.transform.flip(self.image, True, False)

    
        if pygame.mouse.get_pressed()[0] and self.weapon.can_attack():

            if flipped:
                self.game.player.recoil_x_vel += math.cos(math.radians(self.angle)) * self.game.width * self.weapon.recoil
            else:    
                self.game.player.recoil_x_vel -= math.cos(math.radians(self.angle)) * self.game.width * self.weapon.recoil
             
            self.game.player.recoil_y_vel += math.sin(math.radians(self.angle)) * self.game.height/9*16 * self.weapon.recoil

            self.weapon.shoot(pos, self.angle, flipped, vel)

            #self.game.grenades.add(bazooka_bullet.BazookaBullet(self.game, self.rect.center, self.angle, flipped, vel)) #shoot

    
    def rot_center(self):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(self.image, self.angle)
        rot_rect = rot_image.get_rect(center=self.rect.center)
        return rot_image,rot_rect
