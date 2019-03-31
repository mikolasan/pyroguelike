import random
import pygame
from pygamerogue.tile import Tile


class Enemy(Tile):
    def __init__(self, map_pos, player):
        Tile.__init__(
            self,
            size=(48, 48),
            map_pos=map_pos,
            pos=None,
            background_color=(10, 10, 250),
            border_color=(250, 0, 0),
            symbol='e',
            padding=[0, 0],
            text_color=(0, 0, 0))
        self.player = player
        self.angle = 0
        self.directions = ['left', 'right', 'up', 'down']
        self.last_direction = None
        self.last_distance = (None, None)
        self.last_update = pygame.time.get_ticks()
        self.update_delay = 700
        self.speed = 48

    def update(self, events):
        if pygame.time.get_ticks() - self.last_update < self.update_delay:
            return

        dx = abs(self.rect.x - self.player.rect.x)
        dy = abs(self.rect.y - self.player.rect.y)
        next_step = random.choice(self.directions)
        if dx == 0 and dy == 0:
            return
        elif dx > dy:
            last_dx = self.last_distance[0]
            if last_dx is not None:
                if last_dx < dx:
                    if self.last_direction == 'left':
                        next_step = 'right'
                    else:
                        next_step = 'left'
                else:
                    next_step = self.last_direction
            else:
                next_step = random.choice(['left', 'right'])
        else:
            last_dy = self.last_distance[1]
            if last_dy is not None:
                if last_dy < dy:
                    if self.last_direction == 'up':
                        next_step = 'down'
                    else:
                        next_step = 'up'
                else:
                    next_step = self.last_direction
            else:
                next_step = random.choice(['up', 'down'])

        if next_step == 'left':
            self.position['x'] -= self.speed
        elif next_step == 'right':
            self.position['x'] += self.speed
        elif next_step == 'up':
            self.position['y'] -= self.speed
        elif next_step == 'down':
            self.position['y'] += self.speed

        self.last_direction = next_step
        self.last_distance = (dx, dy)
        self.last_update = pygame.time.get_ticks()
        Tile.update(self, events)
