import os
import pygame as pg
from particle import Emitter


class EnemyPieces(pg.sprite.Sprite):
    def __init__(self, pos, angle):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((500, 500), flags=pg.SRCALPHA)
        self.rect = self.image.get_rect()

        self.angle = angle
        path = os.path.join('resources', 'particle.png')
        self.square = pg.image.load(path).convert_alpha()
        self.generator = self.make_emitter(self.rect.center)
        self.tick = pg.time.get_ticks()
        self.start_time = self.tick
        self.duration = 1500
        self.over = False

        self.rect.center = pos

    def make_emitter(self, center_pos):
        kwarg_dict = {
            'texture': self.square,
            'angle': self.angle,
            'speed': (0.7, 1.7),
            'size': (5, 24),
            'life_span': 1.0,
            'start_color': (225, 180, 21),
            'end_color': (0, 180, 21, 0)
        }
        slots = 10
        return Emitter(center_pos, slots, **kwarg_dict)

    def update(self, dt):
        if self.duration < pg.time.get_ticks() - self.start_time:
            self.over = True
        elif not self.over:
            self.generator.update(self.image, self.tick)
            self.tick = pg.time.get_ticks()
