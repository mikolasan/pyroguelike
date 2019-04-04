import os
import math
import pygame as pg
from particle import Emitter


class TestParticles(object):
    def __init__(self, engine, pos, angle):
        self.screen_rect = engine.screen.get_rect()
        self.angle = angle
        self.path = os.path.join("resources", "fuzzball.png")
        self.fuzz = pg.image.load(self.path).convert_alpha()
        self.generator = self.make_emitter()
        self.generator.pos = pos
        self.tick = pg.time.get_ticks()
        self.start_time = self.tick
        self.duration = 500
        self.over = False

    def make_emitter(self):
        kwarg_dict = {
            "texture"     : self.fuzz,
            "angle"       : self.angle,
            "speed"       : (0.5,0.7),
            "size"        : (15,20),
            "life_span"   : 1.0,
            "start_color" : (255,10,15)
        }
        return Emitter(self.screen_rect.center, 50, **kwarg_dict)

    def update(self, events):
        if self.duration < pg.time.get_ticks() - self.start_time:
            self.over = True

    def draw(self, screen, camera):
        if not self.over:
            self.generator.update(screen, self.tick)
            self.tick = pg.time.get_ticks()
