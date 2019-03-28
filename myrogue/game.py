from .controller import BallController
from .world import get_world
from pygamerogue.advanced_sprite import AdvancedSprite
from pygamerogue.tile import RogueTile

class TestGame:
    def __init__(self):
        self.ball = AdvancedSprite("icon.png", pos=(200, 200))
        self.ball.angle = -90
        self.world = get_world()
        self.tiles = []
        for y, row in enumerate(self.world):
            for x, s in enumerate(row):
                self.tiles.append(RogueTile((x,y), s))
        #self.tile = RogueTile((10, 10), 'wall')
        self.controller = BallController([self.ball, self.tiles])

    def link(self, engine):
        self.controller.set_engine(engine)
        engine.add_scene('logo', self.ball, self.controller)
        engine.show_scene('logo')
