import pygame
from .action_controller import ActionController
from .world import get_world
from pygamerogue.tile import RogueTile


class TestGame:
    def __init__(self):
        self.world = get_world()
        self.objects = {
            'tiles': [],
            'walls': [],
            'enemies': []
        }
        for y, row in enumerate(self.world):
            for x, s in enumerate(row):
                if s == '@':
                    self.objects['player'] = RogueTile((x, y), s)
                elif s == '|' or s == '-':
                    self.objects['walls'].append(RogueTile((x, y), s))
                else:
                    self.objects['tiles'].append(RogueTile((x, y), s))
        self.controller = ActionController(self.objects)

    def link(self, engine):
        self.controller.set_engine(engine)
        engine.add_scene('dungeon', self.objects, self.controller)
        engine.show_scene('dungeon')
