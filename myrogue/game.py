from .controller import BallController
from pygamerogue.advanced_sprite import AdvancedSprite
from pygamerogue.tile import RogueTile

class TestGame:
    def __init__(self):
        self.ball = AdvancedSprite("icon.png", pos=(200, 200))
        self.tile = RogueTile((10, 10))
        self.controller = BallController(self.ball)

    def link(self, engine):
        self.controller.set_engine(engine)
        engine.add_scene('logo', self.ball, self.controller)
        engine.show_scene('logo')
