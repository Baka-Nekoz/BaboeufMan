import pygame
from pygame.locals import *
from sprites import bullet,bazooka_bullet,fire
import random



class Pistol:
    def __init__(self, game, player_w):
        self.game = game

        self.image = pygame.image.load('assets/images/player_sprites/eggarm_pistol.png').convert_alpha()
        width = player_w/10*27
        self.image = pygame.transform.scale(self.image, (width,width))

        self.damage = 30
        self.bullet_velocity = 0.008
        self.shoot_interval = 8
        self.recoil = 0.003

    def can_attack(self):
        return self.game.sync_system.can_do_event(self.shoot_interval)
        
    def shoot(self,pos,angle,flipped,vel):
        self.game.player_bullets.add(bullet.Bullet(self.game, pos=pos, angle=angle, left=flipped, entity_vel=vel, damage=self.damage, vel=self.bullet_velocity))



class Ak:
    def __init__(self, game, player_w):
        self.game = game

        self.image = pygame.image.load('assets/images/player_sprites/eggarm_ak.png').convert_alpha()
        width = player_w/10*27
        self.image = pygame.transform.scale(self.image, (width,width))

        self.damage = 5
        self.bullet_velocity = 0.008
        self.shoot_interval = 1
        self.recoil = 0.003

    def can_attack(self):
        return self.game.sync_system.can_do_event(self.shoot_interval)
        
    def shoot(self,pos,angle,flipped,vel):
        self.game.player_bullets.add(bullet.Bullet(self.game, pos=pos, angle=angle, left=flipped, entity_vel=vel, damage=self.damage, vel=self.bullet_velocity))



class Grenade_Launcher:
    def __init__(self, game, player_w):
        self.game = game

        self.image = pygame.image.load('assets/images/player_sprites/eggarm_bazooka.png').convert_alpha()
        width = player_w/10*27
        self.image = pygame.transform.scale(self.image, (width,width))

        self.shoot_interval = 32
        self.recoil = 0.008

    def can_attack(self):
        return self.game.sync_system.can_do_event(self.shoot_interval)
        
    def shoot(self,pos,angle,flipped,vel):
        self.game.grenades.add(bazooka_bullet.BazookaBullet(self.game, pos, angle, flipped, vel))



class Knife:
    def __init__(self, game, player_w):
        self.game = game

        self.image = pygame.image.load('assets/images/player_sprites/eggarm_knife.png').convert_alpha()
        width = player_w/10*27
        self.image = pygame.transform.scale(self.image, (width,width))

        self.damage = 100
        self.bullet_velocity = 0.008
        self.shoot_interval = 8
        self.recoil = -0.008

    def can_attack(self):
        return self.game.sync_system.can_do_event(self.shoot_interval)
        
    def shoot(self,pos,angle,flipped,vel):
        pass



class Shotgun:
    def __init__(self, game, player_w):
        self.game = game

        self.image = pygame.image.load('assets/images/player_sprites/eggarm_shotgun.png').convert_alpha()
        width = player_w/10*27
        self.image = pygame.transform.scale(self.image, (width,width))

        self.damage = 10
        self.bullet_velocity = 0.008
        self.shoot_interval = 16
        self.recoil = 0.008

    def can_attack(self):
        return self.game.sync_system.can_do_event(self.shoot_interval)
        
    def shoot(self,pos,angle,flipped,vel):
        shots = [random.randint(-20, 20) for i in range(10)]
        for i in shots:
            self.game.player_bullets.add(bullet.Bullet(self.game, pos=pos, angle=angle+i, left=flipped, entity_vel=vel, damage=self.damage, vel=self.bullet_velocity))



class Sniper:
    def __init__(self, game, player_w):
        self.game = game

        self.image = pygame.image.load('assets/images/player_sprites/eggarm_sniper.png').convert_alpha()
        width = player_w/10*27
        self.image = pygame.transform.scale(self.image, (width,width))

        self.damage = 100
        self.bullet_velocity = 0.012
        self.shoot_interval = 32
        self.recoil = 0.008

    def can_attack(self):
        return self.game.sync_system.can_do_event(self.shoot_interval)
        
    def shoot(self,pos,angle,flipped,vel):
        self.game.player_bullets.add(bullet.Bullet(self.game, pos=pos, angle=angle, left=flipped, entity_vel=vel, damage=self.damage, vel=self.bullet_velocity))



class Flamethrower:
    def __init__(self, game, player_w):
        self.game = game
        self.image = pygame.image.load('assets/images/player_sprites/eggarm_flamethrower.png').convert_alpha()
        width = player_w/10*27
        self.image = pygame.transform.scale(self.image, (width,width))

        self.bullet_velocity = 0.006
        self.recoil = 0.0002

    def can_attack(self):
        return True
        
    def shoot(self,pos,angle,flipped,vel):
        angle = -angle
        if flipped:
            angle = 180 - angle

        for i in range(15):
            self.game.particles.add(fire.FireParticle(self.game, angle=angle, pos=pos, inertia=vel, can_damage_player=False ,can_damage_mobs=True, collision=True, lifetime=30, vel=self.bullet_velocity))