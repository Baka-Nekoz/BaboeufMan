import pygame
from pygame.locals import *
import math
import random


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos=(0,0), angle=0, left=False, entity_vel=(0,0), color=(0,255,255), damage=5, vel=0.008):
        self.game = game
        pygame.sprite.Sprite.__init__(self)

        
        self.image = self.game.assets['blue_bullet']
        self.image = pygame.transform.scale(self.image, (self.game.width * 0.007, self.game.height/9*16 * 0.005))
        self.damage = damage

        self.x_pos, self.y_pos = pos
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.velocity = vel
        
        self.angle = - angle

        self.image, self.rect = self.rot_center(left)

        if left:
            entity_vel = (-entity_vel[0],entity_vel[1])

        

        self.x_vel = math.cos(math.radians(self.angle)) * self.velocity * self.game.width + entity_vel[0] * 0.15
        self.y_vel = math.sin(math.radians(self.angle)) * self.velocity * self.game.height/9*16 + entity_vel[1] * 0.15

        if left:
            self.x_vel = - self.x_vel


    def update(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
        self.rect.center = (self.x_pos, self.y_pos)

        if not(0<self.rect.centerx<self.game.width):
            self.kill()
        elif not(0<self.rect.centery<self.game.ground.level):
            self.kill()



    def rot_center(self, left):
        """rotate an image while keeping its center"""
        if left:
            rot_image = pygame.transform.rotate(self.image, self.angle)
        else:
            rot_image = pygame.transform.rotate(self.image, -self.angle)
        rot_rect = rot_image.get_rect(center=self.rect.center)
        return rot_image,rot_rect