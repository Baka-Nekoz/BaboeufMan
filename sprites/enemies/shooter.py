import pygame
from pygame.locals import *
from random import randint, random
from sprites import fire
from sprites.enemies import shooterarm
import math

class Shooter(pygame.sprite.Sprite):
    def __init__(self, game, right):
        self.game = game
        pygame.sprite.Sprite.__init__(self)

        self.sprite_w = self.game.width * 0.025
        self.sprite_h = self.sprite_w/10*27

        self.image_stand = self.game.assets['dark_eggman_stand']
        self.image_walk1 = self.game.assets['dark_eggman_walk1']
        self.image_walk3 = self.game.assets['dark_eggman_walk3']

        self.image_stand = pygame.transform.scale(self.image_stand, (self.sprite_w, self.sprite_h))
        self.image_walk1 = pygame.transform.scale(self.image_walk1, (self.sprite_w, self.sprite_h))
        self.image_walk3 = pygame.transform.scale(self.image_walk3, (self.sprite_w, self.sprite_h))

        self.image = self.image_stand
        self.rect = self.image.get_rect()


        self.arm = shooterarm.Arm(self.game, self.sprite_w, False)
        self.game.ennemies_arms.add(self.arm)


        if right:
            self.x_pos = - 0.1 * self.game.width
            self.y_pos = 0.8 * self.game.height
            
            self.rect.centerx = self.x_pos
            self.rect.y = self.y_pos - self.sprite_h
            self.flipped = False

        else:
            self.x_pos = 1.1 * self.game.width
            self.y_pos =0.8 * self.game.height

            self.rect.centerx = self.x_pos
            self.rect.y = self.y_pos - self.sprite_h
            self.flipped = True

        
        self.input_x_vel = 0
        self.input_y_vel = 0
        self.vel_cap = 1
        self.recoil_x_vel = 0
        self.recoil_y_vel = 0

        self.touching_fire_since = 0 
        self.on_fire = False
        self.walking_since = 0
        self.health = 100

        self.pixels_to_erase = []
        self.alpha = 255
        self.image_to_fade = pygame.image.load('assets/images/enemies_sprites/dark_baboeuf/dark_eggman_stand.png').convert_alpha()   


    def update(self, player_pos):
        
        if self.health > 0:
            
            self.IA(player_pos)

            #change frame
            if self.input_x_vel != 0:
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



            self.input_y_vel += self.game.width * 0.0005

            if self.rect.y + self.sprite_h + self.input_y_vel + self.recoil_y_vel > self.game.ground.level: #ground collision
                self.rect.y = self.game.ground.level - self.sprite_h
                self.input_y_vel = 0
                self.recoil_y_vel = 0


            
            can_move_horizontally = True
            can_move_vertically = True
            for sprite in self.game.ennemies.sprites():
                if self == sprite or sprite.health <= 0:
                    continue
                if sprite.rect.colliderect(pygame.Rect(self.rect.left + self.input_x_vel + self.recoil_x_vel, self.rect.top, self.rect.width, self.rect.height)):
                    can_move_horizontally = False
                    self.walking_since = 0
                    self.image = self.image_stand
                if sprite.rect.colliderect(pygame.Rect(self.rect.left, self.rect.top + self.input_y_vel + self.recoil_y_vel, self.rect.width, self.rect.height)):
                    can_move_vertically = False
            
            if can_move_horizontally:
                self.x_pos += self.input_x_vel + self.recoil_x_vel
                self.rect.centerx = self.x_pos
            if can_move_vertically:
                self.y_pos += self.input_y_vel + self.recoil_y_vel
                self.rect.y = self.y_pos - self.sprite_h

            self.recoil_x_vel *= 0.7
            self.recoil_y_vel *= 0.7

            self.flipped = player_pos[0] < self.x_pos

            if self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)


            vel = (self.input_x_vel + self.recoil_x_vel, self.input_y_vel + self.recoil_y_vel)
            self.arm.update(self.rect.center, player_pos, self.flipped, vel)


            for bullet in self.game.player_bullets.sprites():
                if bullet.rect.colliderect(self.rect):
                    self.health -= bullet.damage
                    self.recoil_x_vel += bullet.x_vel * 0.5
                    self.recoil_y_vel += bullet.y_vel * 0.5
                    bullet.kill()


            particles_touched = 0
            for particle in self.game.particles.sprites():
                if particle.can_damage_mobs and self.rect.colliderect(particle.rect):
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
                    

        if self.health <= 0:
                self.arm.kill()
                self.fade()


    def IA(self, player_pos):

        if player_pos[0] + 0.2 * self.game.width < self.x_pos: # joueur à gauche
            self.flipped = False
            if self.input_x_vel > - self.vel_cap:
                self.input_x_vel -= 1
                    

        elif self.x_pos < player_pos[0] - 0.2 * self.game.width: # joueur à droite
            self.flipped = True
            
            if self.input_x_vel < self.vel_cap:
                self.input_x_vel += 1
                    

        else:
            if self.input_x_vel > 0:
                self.input_x_vel -= 1
            elif self.input_x_vel < 0:
                self.input_x_vel += 1

        
    def fade(self):
        pixel_array = pygame.PixelArray(self.image_to_fade)
        width, height = pixel_array.shape


        if self.pixels_to_erase == []:
            for y in range(height):
                for x in range(width):
                    self.pixels_to_erase.append((x,y))

        
        if len(self.pixels_to_erase) > 0:

            if len(self.pixels_to_erase) >= 5:
                num_to_erase = 5
            else:
                num_to_erase = len(self.pixels_to_erase)

            while num_to_erase > 0:
                i = randint(0,len(self.pixels_to_erase) - 1)
                pixel = self.pixels_to_erase[i]
                self.pixels_to_erase.pop(i)

                pixel_array[pixel] = (0, 0, 0, 0)
                num_to_erase -= 1


            self.image = pygame.transform.scale(pixel_array.make_surface(), (self.sprite_w, self.sprite_h))
            if self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)
            
            self.image.set_alpha(self.alpha)
                
            if self.alpha > 0:
                self.alpha -= 3

            if abs(self.recoil_x_vel) > 10:
                self.recoil_y_vel *= 10/abs(self.recoil_x_vel)
                if self.recoil_x_vel > 0:
                    self.recoil_x_vel = 10
                else:
                    self.recoil_x_vel = -10

            if abs(self.recoil_y_vel) > 10:
                self.recoil_x_vel *= 10/abs(self.recoil_y_vel)
                if self.recoil_y_vel > 0:
                    self.recoil_y_vel = 10
                else:
                    self.recoil_y_vel = -10

            self.input_x_vel *= 0.98
            self.input_y_vel *= 0.98
            self.recoil_x_vel *= 0.98
            self.recoil_y_vel *= 0.98
            self.x_pos += self.input_x_vel + self.recoil_x_vel
            self.y_pos += self.input_y_vel + self.recoil_y_vel
            self.rect.centerx = self.x_pos
            self.rect.y = self.y_pos - self.sprite_h


        if len(self.pixels_to_erase) == 0:
            self.kill()
