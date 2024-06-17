import pygame
from pygame.locals import *
import os
import sys
import time
from sprites import menu_player, menu_background, titletext, press, menuarm, button, fire
from game import Game
from random import random


class Main:
    def __init__(self):

        pygame.init()
        pygame.mouse.set_visible(True)

        screenInfos = pygame.display.Info()
        screenInfos = pygame.display.Info()
        self.width = screenInfos.current_w
        self.height = screenInfos.current_h
        self.screen = pygame.display.set_mode((self.width, self.height))

        #assets
        self.assets = {}
        self.assets['bullet_pistol'] = pygame.image.load('assets/images/bullets/bullet_pistol.png').convert_alpha()
        self.assets['white_bullet'] = pygame.image.load('assets/images/bullets/white_bullet.png').convert_alpha()
        self.assets['sunset'] = pygame.image.load('assets/images/sunset.png').convert_alpha()


        #init groups
        self.particles = pygame.sprite.Group()


        self.mouse = pygame.mouse.get_pos()
        self.titletext = titletext.Title(self)
        self.menu_background = menu_background.MenuBackground(self)
        self.menu_player = menu_player.MenuPlayer(self.screen, self)

        self.clock = pygame.time.Clock()

        self.tick = 0
        self.scroll = 0
        self.keys_pressed = []
        self.mouse_buttons = []

        self.running = True
        bouton1 = button.Button((100,0,255), screenInfos.current_w * 0.5, screenInfos.current_h * 0.4, screenInfos.current_w * 0.2, screenInfos.current_h * 0.1, 'Jouer !')
        self.bouton1 = bouton1
        bouton2 = button.Button((100,0,255), screenInfos.current_w * 0.5, screenInfos.current_h * 0.6, screenInfos.current_w * 0.2, screenInfos.current_h * 0.1, 'Quitter')
        self.bouton2 = bouton2

        while self.running:
            self.clock.tick(60)
            
            self.handle_events()
            self.update()
            self.display()

            
    def display(self):

        self.menu_background.display()
        self.screen.blit(self.menu_player.image, self.menu_player.rect)
        self.screen.blit(self.menu_player.menuarm.image, self.menu_player.menuarm.rect)
        self.screen.blit(self.titletext.image, self.titletext.rect)
        self.bouton1.draw(self.screen, (0,255,0))
        self.bouton2.draw(self.screen, (0,255,0))
        for particle in self.particles.sprites():
            particle.display()
        
        pygame.display.flip()
            

    def handle_events(self):
        self.tick += 1
        self.scroll = 0
        self.mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.game = Game(self)
                    while self.game.replay:
                        self.game = Game(self)
                else:
                    self.keys_pressed.append(event.key)

            elif event.type == KEYUP:
                if event.key in self.keys_pressed:                        
                    self.keys_pressed.remove(event.key)

            elif event.type == MOUSEWHEEL:
                self.scroll = event.y

            elif event.type == MOUSEMOTION:
                pass

    

    def update(self):
        self.menu_player.update(self.mouse)
        for particle in self.particles.sprites():
            particle.update()

        if self.bouton1.isOver(self.mouse):
            self.bouton1.color = (255,0,0)
            self.particles.add(fire.FireParticle(self,pos=(self.bouton1.x + self.bouton1.width * random(), self.bouton1.y + self.bouton1.height * random()),
                                angle=-90, vel= 0.002, collision=False))

            if pygame.mouse.get_pressed()[0]:
                self.game = Game(self)
                while self.game.replay:
                    self.bouton1.color = (100,0,255)
                    self.game = Game(self)

        elif self.bouton2.isOver(self.mouse):
            self.bouton2.color = (255,0,0)
            self.particles.add(fire.FireParticle(self,pos=(self.bouton2.x + self.bouton2.width * random(), self.bouton2.y + self.bouton2.height * random()),
                                angle=-90, vel= 0.002, collision=False))

            if pygame.mouse.get_pressed()[0]:
                self.running = False
                pygame.quit()
                sys.exit()
        else:
            self.bouton1.color = (100,0,255)
            self.bouton2.color = (100,0,255)



if __name__ == '__main__':
    Main()
    sys.exit()
