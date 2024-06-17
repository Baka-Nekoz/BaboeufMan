import pygame
from pygame.locals import *
import math

class Background:
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(0, 0, self.game.width, self.game.height)
        
        self.game.assets['sun'] = pygame.transform.scale(self.game.assets['sun'], (self.game.width * 0.05, self.game.width * 0.05))
        self.image_sun = self.game.assets['sun']
        self.rect_sun = self.image_sun.get_rect()

        self.image_sunrays = self.game.assets['sunrays']
        self.image_sunrays = pygame.transform.scale(self.image_sunrays, (self.game.width * 0.2, self.game.width * 0.2))
        self.rect_sunrays = self.image_sunrays.get_rect()

        self.game.assets['moon'] = pygame.transform.scale(self.game.assets['moon'], (self.game.width * 0.04, self.game.width * 0.04))
        self.image_moon = self.game.assets['moon']
        self.rect_moon = self.image_moon.get_rect()

        self.image_moonrays = self.game.assets['moonrays']
        self.image_moonrays = pygame.transform.scale(self.image_moonrays, (self.game.width * 0.07, self.game.width * 0.07))
        self.rect_moonrays = self.image_moonrays.get_rect()

        self.image_sunset = self.game.assets['sunset']
        self.image_sunset = pygame.transform.scale(self.image_sunset, (self.game.width * 0.8, self.game.height))
        self.rect_sunset = self.image_sunset.get_rect()
        


        self.night_sky = (20, 24, 82)
        self.day_sky = (113, 188, 225) 
        self.twilight_sky = (66, 106, 153)

        self.color = [0,0,255]

        self.cycle = 10800

        self.start_color = self.night_sky
        self.final_color = self.day_sky



    def update(self):
        progress_in_sequence = (self.game.tick) / (self.cycle/8)
        progress_in_sequence = progress_in_sequence - math.floor(progress_in_sequence)
        sequence = math.floor(self.game.tick / (self.cycle / 8) % 8)


        #sky

        if sequence == 0: #nuit à jour part 2
            self.start_color = self.twilight_sky
            self.final_color = self.day_sky

            self.rect_sunset.center = (0, self.game.height*0.9)
            self.image_sunset.set_alpha((1-progress_in_sequence)*255)

        elif sequence == 3: #jour à nuit part 1
            self.start_color = self.day_sky
            self.final_color = self.twilight_sky

            self.rect_sunset.center = (self.game.width, self.game.height*0.9)
            self.image_sunset.set_alpha(progress_in_sequence*255)

        elif sequence == 4: #jour à nuit part 2
            self.start_color = self.twilight_sky
            self.final_color = self.night_sky

            self.rect_sunset.center = (self.game.width, self.game.height*0.9)
            self.image_sunset.set_alpha((1-progress_in_sequence)*255)

        elif sequence == 7: #nuit à jour part 1
            self.start_color = self.night_sky
            self.final_color = self.twilight_sky

            self.rect_sunset.center = (0, self.game.height*0.9)
            self.image_sunset.set_alpha(progress_in_sequence*255)

        else:
            self.start_color = self.final_color
        
        
        self.color_shift(progress_in_sequence)


        sun_progress = (self.game.tick) / (self.cycle/2)
        sun_progress = sun_progress - math.floor(sun_progress)

        if sequence <= 3: # si c'est le jour
            #sun
            self.rotate_sun_moon(True)
            self.rect_sun.center = (sun_progress * self.game.width, self.y(sun_progress - 0.5) * self.game.height)
            self.rect_sunrays.center = self.rect_sun.center

            self.rect_moon.x = self.game.width
            self.rect_moonrays.x = self.game.width

        else: # si c'est la nuit
            self.rotate_sun_moon(False)
            self.rect_moon.center = (sun_progress * self.game.width, self.y(sun_progress - 0.5) * self.game.height)
            self.rect_moonrays.center = self.rect_moon.center

            self.rect_sun.x = self.game.width
            self.rect_sunrays.x = self.game.width


        


    def y(self,x):
        return 3 * x**2 + 0.2

        
    def color_shift(self,coef):
        for i in range(3):
            diff = self.final_color[i] - self.start_color[i]
            self.color[i] = self.start_color[i] + diff * coef

    
    def alpha_shift(self,coef):
        pass
        
        
    def display(self):
        pygame.draw.rect(self.game.screen, self.color, self.rect)
        self.game.screen.blit(self.image_sunrays, self.rect_sunrays)
        self.game.screen.blit(self.image_sun, self.rect_sun)
        self.game.screen.blit(self.image_moonrays, self.rect_moonrays)
        self.game.screen.blit(self.image_moon, self.rect_moon)
        self.game.screen.blit(self.image_sunset, self.rect_sunset)
        

    def rotate_sun_moon(self,sun):
        if sun: # si c'est le jour
            self.image_sun = self.game.assets['sun']
            self.image_sun = pygame.transform.rotate(self.image_sun, - self.game.tick * 0.03)
            self.rect_sun = self.image_sun.get_rect()
        
        else:
            self.image_moon = self.game.assets['moon']
            self.image_moon = pygame.transform.rotate(self.image_moon, - self.game.tick * 0.03)
            self.rect_moon = self.image_moon.get_rect()