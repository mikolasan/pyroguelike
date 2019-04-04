import random
import pygame
from pygamerogue.tile import Tile


class Enemy(Tile):
    def __init__(self, map_pos, world, player):
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
        self.world = world
        self.player = player
        self.damage = 10
        self.angle = 0
        self.directions = ['left', 'right', 'up', 'down']
        self.last_direction = None
        self.last_distance = (None, None)
        self.last_update = pygame.time.get_ticks()
        self.update_delay = 700

    def update(self, events):
        if pygame.time.get_ticks() - self.last_update < self.update_delay:
            return
        
        dx = abs(self.rect.x - self.player.rect.x)
        dy = abs(self.rect.y - self.player.rect.y)
        next_step = random.choice(self.directions)
        if dx <= self.size[0] and dy <= self.size[1]:
            print('update1', dx, dy)
            self.player.attacked(self.player, self.damage)
            self.last_update = pygame.time.get_ticks()
            return
        elif dx > dy:
            last_dx = self.last_distance[0]
            if last_dx is not None:
                if last_dx < dx:
                    if self.last_direction == 'left':
                        next_step = 'right'
                    else:
                        next_step = 'left'
                elif self.last_direction in ['left', 'right']:
                    next_step = self.last_direction
                else:
                    next_step = random.choice(['left', 'right'])
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
                elif self.last_direction in ['up', 'down']:
                    next_step = self.last_direction
                else:
                    next_step = random.choice(['up', 'down'])
            else:
                next_step = random.choice(['up', 'down'])

        x, y = self.map_pos[0], self.map_pos[1]
        if next_step == 'left':
            x -= 1
        elif next_step == 'right':
            x += 1
        elif next_step == 'up':
            y -= 1
        elif next_step == 'down':
            y += 1
        if self.world[y][x] in ['-', '|']:
            pass
        else:
            self.update_map_position((x, y))
            self.last_direction = next_step
            self.last_distance = (dx, dy)

        self.last_update = pygame.time.get_ticks()
        Tile.update(self, events)

        dx = abs(self.rect.x - self.player.rect.x)
        dy = abs(self.rect.y - self.player.rect.y)
        print('update2', dx, dy)
        if dx <= self.size[0] and dy <= self.size[1]:
            self.player.attacked(self.player, self.damage)
