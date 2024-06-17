import pygame
from pygame.locals import *
import os
import sys
import time
from sprites import player, background, ground, pointer, lifebar, button, fire
from sprites.enemies import shooter
import sync_system
from random import randint


class Game:
    def __init__(self, main):

        pygame.mouse.set_visible(False)

        screenInfos = pygame.display.Info()
        screenInfos = pygame.display.Info()
        self.width = main.width
        self.height = main.height
        self.screen = main.screen
        self.main = main





        #assets
        self.assets = {}
        self.assets['blue_bullet'] = pygame.image.load('assets/images/bullets/blue_bullet.png').convert_alpha()
        self.assets['bullet_bazooka'] = pygame.image.load('assets/images/bullets/bullet_bazooka.png').convert_alpha()
        self.assets['white_bullet'] = pygame.image.load('assets/images/bullets/white_bullet.png').convert_alpha()
        self.assets['dark_eggman_stand'] = pygame.image.load('assets/images/enemies_sprites/dark_baboeuf/dark_eggman_stand.png').convert_alpha()
        self.assets['dark_eggman_walk1'] = pygame.image.load('assets/images/enemies_sprites/dark_baboeuf/dark_eggman_walk1.png').convert_alpha()
        self.assets['dark_eggman_walk3'] = pygame.image.load('assets/images/enemies_sprites/dark_baboeuf/dark_eggman_walk3.png').convert_alpha()
        self.assets['dark_eggarm_pistol'] = pygame.image.load('assets/images/enemies_sprites/dark_baboeuf/dark_eggarm_pistol.png').convert_alpha()
        self.assets['sun'] = pygame.image.load('assets/images/sun.png').convert_alpha()
        self.assets['sunrays'] = pygame.image.load('assets/images/sunrays.png').convert_alpha()
        self.assets['moon'] = pygame.image.load('assets/images/moon.png').convert_alpha()
        self.assets['moonrays'] = pygame.image.load('assets/images/moonrays.png').convert_alpha()
        self.assets['sunset'] = pygame.image.load('assets/images/sunset.png').convert_alpha()
        self.assets['exp1'] = pygame.image.load('assets/images/bullets/exp1.png').convert_alpha()
        self.assets['exp2'] = pygame.image.load('assets/images/bullets/exp2.png').convert_alpha()
        self.assets['exp3'] = pygame.image.load('assets/images/bullets/exp3.png').convert_alpha()
        self.assets['exp4'] = pygame.image.load('assets/images/bullets/exp4.png').convert_alpha()
        self.assets['exp5'] = pygame.image.load('assets/images/bullets/exp5.png').convert_alpha()
        self.assets['gameover'] = pygame.image.load('assets/images/gameover.png').convert_alpha()


        #init groups
        self.ennemies = pygame.sprite.Group()
        self.ennemies_arms = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.ennemy_bullets = pygame.sprite.Group()
        self.grenades = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()


        self.mouse = pygame.mouse.get_pos()
        self.background = background.Background(self)
        self.ground = ground.Ground(self)
        self.pointer = pointer.Pointer(self, self.mouse)
        self.player = player.Player(self.screen, self)
        self.lifebar = lifebar.Lifebar(self)
        

        self.clock = pygame.time.Clock()
        self.tick = 0

        self.ennemies.add(shooter.Shooter(self, False))
        self.ennemies.add(shooter.Shooter(self, True))

        self.scroll = 0
        self.keys_pressed = []
        self.mouse_buttons = []

        pygame.mixer.init()
        pygame.mixer.music.load('assets/sounds/music.wav')
        pygame.mixer.music.play(loops=-1)
        self.sync_system = sync_system.SyncSystem(self)

        self.replay = False
        self.paused = False
        self.button1 = button.Button((100,0,255), self.width * 0.4, self.height * 0.2, self.width * 0.2, self.height * 0.1, 'Reprendre')
        self.button2 = button.Button((100,0,255), self.width * 0.4, self.height * 0.4, self.width * 0.2, self.height * 0.1, 'Rejouer')
        self.button3 = button.Button((100,0,255), self.width * 0.4, self.height * 0.6, self.width * 0.2, self.height * 0.1, 'Menu principal')

        self.running = True

        while self.running:
            self.clock.tick(60) 

            self.handle_events()
            self.update()
            self.display()

            
    def display(self):
        self.background.display()
        self.screen.blit(self.ground.image, self.ground.rect)
        self.lifebar.display_rect()
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.player.arm.image, self.player.arm.rect)
        
        self.player_bullets.draw(self.screen)
        self.ennemy_bullets.draw(self.screen)
        
        self.ennemies.draw(self.screen)
        self.ennemies_arms.draw(self.screen)
        self.grenades.draw(self.screen)
        
        for particle in self.particles.sprites():
            particle.display()

        self.screen.blit(self.pointer.image, self.pointer.rect)

        if self.paused and not self.player.is_dead():
            grey_screen = pygame.Surface((self.width, self.height))
            grey_screen.set_alpha(100)
            grey_screen.fill((0,0,0))
            self.screen.blit(grey_screen, (0,0))

            self.button1.draw(self.screen, (0,255,0))
            self.button2.draw(self.screen, (0,255,0))
            self.button3.draw(self.screen, (0,255,0))

        elif self.player.is_dead():
            grey_screen = pygame.Surface((self.width, self.height))
            grey_screen.set_alpha(100)
            grey_screen.fill((0,0,0))
            self.screen.blit(grey_screen, (0,0))


            if self.time_till_decreasing > 0:
                self.game_over_size_add += 0.03
                self.time_till_decreasing -= 1
            else:
                self.game_over_size_add *= 0.95

            if self.sync_system.can_do_event(32):
                self.game_over_size_add = 0
                self.time_till_decreasing = 3
            self.image_game_over = pygame.transform.scale(self.assets['gameover'], (self.width * 0.7 * (1+self.game_over_size_add), self.height * 0.28 * (1+self.game_over_size_add)))
            rect = self.image_game_over.get_rect()
            rect.center = (0.5 * self.width, 0.19 * self.height)
            self.screen.blit(self.image_game_over, rect)

            self.button2.draw(self.screen, (0,255,0))
            self.button3.draw(self.screen, (0,255,0))

        pygame.display.flip()
            

    def handle_events(self):
        self.scroll = 0
        self.mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:                        
                    self.paused = not self.paused
                else:
                    self.keys_pressed.append(event.key)

            elif event.type == KEYUP:
                if event.key in self.keys_pressed:                        
                    self.keys_pressed.remove(event.key)

            elif event.type == MOUSEWHEEL:
                self.scroll = event.y 


    def update(self):
        if not self.player.is_dead():
            if not self.paused:
                if pygame.mouse.get_visible():
                    pygame.mouse.set_visible(False)
                self.tick += 1


                if self.tick % 400 == 0 and len(self.ennemies) < 3:
                    self.ennemies.add(shooter.Shooter(self, bool(randint(0,1))))


                self.sync_system.update()
                self.background.update()
                self.player.update(self.keys_pressed, self.mouse)
                self.ennemies.update(self.player.rect.center)
                self.player_bullets.update()
                self.ennemy_bullets.update()
                self.grenades.update()
                self.particles.update()
                self.pointer.update(self.mouse)
                self.lifebar.update()
                

                

                if self.player.is_dead():
                    self.player.kill()
                    self.game_over_size_add = 0
                    self.image_game_over = self.assets['gameover']
                    self.time_till_decreasing = 0

            else:
                self.sync_system.update()
                if not pygame.mouse.get_visible():
                    pygame.mouse.set_visible(True)

                if self.button1.isOver(self.mouse):
                    self.button1.color = (255,0,0)
                    if pygame.mouse.get_pressed()[0]:
                        self.paused = False
                elif self.button2.isOver(self.mouse):
                    self.button2.color = (255,0,0)
                    if pygame.mouse.get_pressed()[0]:
                        self.replay = True
                        self.running = False
                elif self.button3.isOver(self.mouse):
                    self.button3.color = (255,0,0)
                    if pygame.mouse.get_pressed()[0]:
                        self.replay = False
                        self.running = False
                else:
                    self.button1.color = (100,0,255)
                    self.button2.color = (100,0,255)
                    self.button3.color = (100,0,255)

        else:
            pygame.mouse.set_visible(True)
            self.sync_system.update()

            if self.button2.isOver(self.mouse):
                self.button2.color = (255,0,0)
                if pygame.mouse.get_pressed()[0]:
                    self.replay = True
                    self.running = False
            elif self.button3.isOver(self.mouse):
                self.button3.color = (255,0,0)
                if pygame.mouse.get_pressed()[0]:
                    self.replay = False
                    self.running = False
            else:
                self.button2.color = (100,0,255)
                self.button3.color = (100,0,255)


    def choose_weapons_menu(self):
        image_pistol = 0

        running = True
        while running:
            pass
