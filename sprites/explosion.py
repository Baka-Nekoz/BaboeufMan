import pygame
from pygame import locals
import math

import pygame
from pygame import locals
import math
import random


class BazookaBullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, angle, left, entity_vel):
        self.game = game
        pygame.sprite.Sprite.__init__(self)

        self.image = self.game.assets['bullet_bazooka']
        self.image = pygame.transform.scale(self.image, (self.game.width * 0.012, self.game.height/9*16 * 0.012))
        
        self.rect = self.image.get_rect()

        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect.center = (self.x_pos, self.y_pos)

        self.velocity = 0.01

        self.angle = - angle

        if left:
            entity_vel = (-entity_vel[0],entity_vel[1])

        self.x_vel = math.cos(math.radians(self.angle)) * self.velocity * self.game.width + entity_vel[0] * 0.25
        self.y_vel = math.sin(math.radians(self.angle)) * self.velocity * self.game.height/9*16 + entity_vel[1] * 0.25

        if left:
            self.x_vel = - self.x_vel

        self.intervals_before_explosion = 9

        self.ticks_since_explosion = 0


    def update(self):
        
        if self.ticks_since_explosion == 10:
            # for the enemies
        
            for enemy in self.game.ennemies.sprites():
                distance = math.sqrt((enemy.rect.centerx - self.x_pos)**2 + (enemy.rect.centery - self.y_pos)**2)

                if distance < 0.2 * self.game.width:
                    damage = (-distance/self.game.width + 0.2) * 700

                    #angle = math.atan(distance/0.2 * self.game.width)
                    #enemy.recoil_x_vel += math.cos(angle) * 0.001 * self.game.width
                    #enemy.recoil_y_vel += math.sin(angle) * 0.001 * self.game.height/9*16

                else:
                    damage = 0
            
                enemy.health -= damage

            # for the player

            distance = math.sqrt((self.game.player.rect.centerx - self.x_pos)**2 + (self.game.player.rect.centery - self.y_pos)**2)

            if distance < 0.15 * self.game.width:
                damage = (-distance/self.game.width + 0.15) * 800 

            else:
                damage = 0
            self.game.player.health -= damage

        

        #explosion effect

        frame = self.ticks_since_explosion // 5 + 1
        self.ticks_since_explosion += 1

        
        
        if frame <= 5:
            self.image = self.game.assets[f'exp{frame}']
            self.image = pygame.transform.scale(self.image, (self.game.width * 0.25, self.game.height/9*16 * 0.25))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x_pos, self.y_pos)
            
        else:
            self.kill()
