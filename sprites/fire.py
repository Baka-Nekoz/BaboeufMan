import pygame
from pygame.locals import *
import math
import random
from perlin_noise import PerlinNoise



class AltFireParticle(pygame.sprite.Sprite):
    def __init__(self, game, pos=(500,500), radius=5, x_vel=10, y_vel=0):
        self.game = game
        super(AltFireParticle, self).__init__()
        self.x, self.y = pos
        self.radius = radius
        
        self.x_vel = x_vel
        self.y_vel = y_vel + random.randint(1, 9)
        self.burn_rate = 0.1
        
        self.layers = 2
        self.glow = 2
        
        surf_size = 2 * self.radius * self.layers * self.layers * self.glow
        self.surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
        
    def update(self):
        random_x_vel = random.randint(-int(self.radius), int(self.radius))
        self.x += self.x_vel + random_x_vel
        self.y -= self.y_vel
        
        self.radius -= self.burn_rate
        if self.radius <= 0:
            self.radius = 0.01
        
        surf_size = 2 * self.radius * self.layers * self.layers * self.glow
        self.surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
        
        for i in range(self.layers, -1, -1):
            alpha = 255 - i * (255 // self.layers - 5)
            if alpha <= 0:
                alpha = 0.01
            radius = int(self.radius * self.glow * i * i)
             
            if self.radius >3.5:
                color = 255, 0, 0
            elif self.radius > 2.5:
                color = 255, 150, 0
            else:
                color = 50, 50, 50
            color = (*color, alpha)
        
            pygame.draw.circle(self.surf, color, (self.surf.get_width() // 2, self.surf.get_height() // 2), radius)

        if self.radius <= 0.1:
            self.kill()


    def display(self):
        self.game.screen.blit(self.surf, self.surf.get_rect(center=(self.x, self.y)))




class FireParticle(pygame.sprite.Sprite):
    def __init__(self, game, pos=(500,500), angle=0, vel=0.006, inertia=(0,0), can_damage_player=False, can_damage_mobs=True, collision=True, lifetime=20):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.x_pos, self.y_pos = pos


        self.x_vel = math.cos(math.radians(angle)) * vel * self.game.width
        self.y_vel = math.sin(math.radians(angle)) * vel * self.game.height/9*16



        self.rect = pygame.Rect(pos[0], pos[1], self.game.width * 0.003, self.game.height/9*16 * 0.003)

        self.glow_radius = 1.5 * self.rect.width

        self.can_damage_player = can_damage_player
        self.can_damage_mobs = can_damage_mobs
        self.collision = collision

        self.lifetime = lifetime

        color = random.randint(0,2)
        if color == 0: # red
            self.color = (255, 0, 0)
            self.diffusion = 0.007
        elif color == 1: # orange
            self.color = (255, 165, 0)
            self.diffusion = 0.005
        else: # yellow
            self.color = (255, 255, 0)
            self.diffusion = 0.003


    def update(self):
        x_to_move = self.x_vel + (random.random()-0.5) * self.diffusion * self.game.width
        y_to_move = self.y_vel + (random.random()-0.5) * self.diffusion * self.game.height/9*16

        if self.collision:
            can_move_horizontally = True
            can_move_vertically = True
        
            if self.rect.bottom + y_to_move > self.game.ground.level:
                can_move_vertically = False

            if not can_move_horizontally:
                self.x_vel = 0
            if not can_move_vertically:
                self.y_vel = 0


        self.x_pos += x_to_move
        self.y_pos += y_to_move
        self.rect.center = (self.x_pos, self.y_pos)

        if self.lifetime < 0 and random.randint(0, 5) == 0:
            self.kill()

        self.lifetime -= 1


    def display(self):
        tmp_suface = pygame.Surface((self.glow_radius*2, self.glow_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(tmp_suface, (*self.color, 35), (self.glow_radius, self.glow_radius), self.glow_radius)
        

        self.game.screen.blit(tmp_suface,(self.rect.centerx - self.glow_radius, self.rect.centery - self.glow_radius))
        pygame.draw.rect(self.game.screen, self.color, self.rect)
        
        




