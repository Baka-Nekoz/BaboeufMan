import pygame
from pygame.locals import *
import math
from sprites import arm,fire
from random import random

class Player(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.sprite_w = self.game.width * 0.025
        self.sprite_h = self.sprite_w/10*27

        
        #chargement des images
        self.image_stand = pygame.image.load('assets/images/player_sprites/eggman_stand.png').convert_alpha()
        self.image_walk1 = pygame.image.load('assets/images/player_sprites/eggman_walk1.png').convert_alpha()
        self.image_walk3 = pygame.image.load('assets/images/player_sprites/eggman_walk3.png').convert_alpha()
        self.image_crouch = pygame.image.load('assets/images/player_sprites/eggman_crouch.png').convert_alpha()

        self.image_stand = pygame.transform.scale(self.image_stand, (self.sprite_w, self.sprite_h))
        self.image_walk1 = pygame.transform.scale(self.image_walk1, (self.sprite_w, self.sprite_h))
        self.image_walk3 = pygame.transform.scale(self.image_walk3, (self.sprite_w, self.sprite_h))
        self.image_crouch = pygame.transform.scale(self.image_crouch, (self.sprite_w, self.sprite_h))

        self.image = self.image_stand
        self.rect = self.image.get_rect()


        self.walking_since = 0
        self.jumping_since = 0

        

        self.rect.centerx = self.game.width * 0.5
        self.rect.y = self.game.height * 0.8 - self.sprite_h


        self.input_x_vel = 0
        self.input_y_vel = 0
        self.input_vel_cap = 8

        self.recoil_x_vel = 0
        self.recoil_y_vel = 0


        self.arm = arm.Arm(self.game, self.sprite_w)

        self.touching_fire_since = 0 
        self.on_fire = False
        self.health = 100


    def update(self, keys_pressed, mouse):


        if K_q in keys_pressed and K_d in keys_pressed: 

            if self.input_x_vel > 0:
                self.input_x_vel -= 1
            elif self.input_x_vel < 0:
                self.input_x_vel += 1

        else :

            if K_q in keys_pressed:

                if self.input_x_vel >= -self.input_vel_cap:
                    self.input_x_vel -= 1

            elif K_d in keys_pressed:

                if self.input_x_vel <= self.input_vel_cap:
                    self.input_x_vel += 1

            else:
                if self.input_x_vel > 0:
                    self.input_x_vel -= 1
                elif self.input_x_vel < 0:
                    self.input_x_vel += 1


        #change frame
        if (K_q in keys_pressed) ^ (K_d in keys_pressed):
            self.walking_since += 1
            frame = math.floor(self.walking_since / 8 % 4)
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
        


        #gravity :
        self.input_y_vel += self.game.width * 0.0005

        if self.rect.y + self.sprite_h + self.input_y_vel + self.recoil_y_vel > self.game.ground.level: #fast ground collision (à changer) (ou pas)
            self.rect.y = self.game.ground.level - self.sprite_h
            self.input_y_vel = 0
            self.recoil_y_vel = 0


            if K_SPACE in keys_pressed and self.jumping_since == 0: #jump
                self.jumping_since = 1
                

        if self.jumping_since > 0: # crouch then jump
            self.image = self.image_crouch
            self.jumping_since += 1
            if self.jumping_since == 10:
                self.input_y_vel = - 20
                self.jumping_since = 0
                self.image = self.image_stand


        #bordures
        if self.rect.left + self.input_x_vel + self.recoil_x_vel < 0:
            self.rect.left = 0
            self.input_x_vel = 0
            self.recoil_x_vel = 0
        
        elif self.rect.x + self.sprite_w + self.input_x_vel + self.recoil_x_vel > self.game.width:
            self.rect.x = self.game.width - self.sprite_w
            self.input_x_vel = 0
            self.recoil_x_vel = 0


        vel = (self.input_x_vel + self.recoil_x_vel, self.input_y_vel + self.recoil_y_vel)
        self.move(vel)

        self.recoil_x_vel *= 0.7
        self.recoil_y_vel *= 0.7

        flipped = mouse[0] < self.rect.centerx
        if flipped:
            self.image = pygame.transform.flip(self.image, True, False)
            

        #arm
        self.arm.update((self.rect.centerx, self.rect.centery), mouse, flipped, vel)
        

        for bullet in self.game.ennemy_bullets.sprites():
                if bullet.rect.colliderect(self.rect):
                    self.health -= bullet.damage
                    self.recoil_x_vel += bullet.x_vel * 0.5
                    self.recoil_y_vel += bullet.y_vel * 0.5
                    bullet.kill()

        
        particles_touched = 0
        for particle in self.game.particles.sprites():
            if particle.can_damage_player and self.rect.colliderect(particle.rect):
                particles_touched += 1
                
        if particles_touched > 10:
            
            self.health -= 0.75
            if self.touching_fire_since >= 17 and particles_touched > 20:
                self.on_fire = True
            else:
                self.touching_fire_since += 1
            
        else:
            if self.touching_fire_since > 0:
                self.touching_fire_since -= 0.10
            else:
                self.on_fire = False

        if self.on_fire:
            self.game.particles.add(fire.FireParticle(self.game,pos=(self.rect.x + random()*self.rect.width, self.rect.y + random()*self.rect.height), angle=-90, vel=0.002, can_damage_mobs=False))
            self.health -= 0.1
        
        

            
            

    def move(self,vel):

        self.rect = self.rect.move(vel)
        

    def is_dead(self):
        if self.health <= 0:
            return True
        else:
            return False
