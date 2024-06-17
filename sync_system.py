import pygame
from pygame import locals
import time
import math



class SyncSystem():
    def __init__(self, game):
        self.game = game

        self.start = time.time()

        self.bpm = 150

        self.interval = 1/(self.bpm/60) / 4 #1/16 note interval
        self.intervals_done = 0

        self.on_interval = False



    def update(self):
        current_time = time.time()

        if self.on_interval:
            self.on_interval = False

        if math.floor((current_time - self.start) / self.interval) > self.intervals_done:
            self.on_interval = True
            self.intervals_done += 1



    def can_do_event(self, event_interval):
        if self.on_interval:
            
            if self.intervals_done % event_interval == 0:
                return True

        return False
