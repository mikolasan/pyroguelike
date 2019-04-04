import math
from pygamerogue.tile import Tile


class Bullet(Tile):
    def __init__(self, pos, angle):
        Tile.__init__(
            self,
            size=(10, 10),
            map_pos=None,
            pos=pos,
            background_color=(250, 250, 250),
            border_color=(0, 0, 0),
            symbol='',
            padding=[0, 0],
            text_color=(0, 0, 0))
        self.angle = angle
        self.speed = 5

    def update(self, events):
        self.pos['x'] += math.cos(self.angle) * self.speed
        self.pos['y'] -= math.sin(self.angle) * self.speed
        Tile.update(self, events)
