import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup
from pytmx.util_pygame import load_pygame
from pygamerogue.rogue_renderer import RogueRenderer


class NewWorld(object):
    def __init__(self):
        self.levels = {
            'bar': {
                'tmx_file': 'lobby.tmx',
                'start_points': ['entrance'],
            },
        }
        self.load_levels()
        self.previous_level = None
        self.current_level = 'bar'

    def set_current_level(self, name):
        self.previous_level = self.current_level
        self.current_level = name

    def get_level_info(self, name=None):
        return self.levels[self.current_level if name is None else name]

    def load_levels(self):
        for level_name, level_info in self.levels.items():
            self.load_level(level_info)

    def load_level(self, level_info):
        tiled_map = load_pygame(level_info['tmx_file'])
        map_data = pyscroll.data.TiledMapData(tiled_map)
        map_layer = RogueRenderer(map_data, [800, 600], clamp_camera=False, tall_sprites=0)
        map_layer._redraw_cutoff = 24
        map_layer.zoom = 4
        sprite_group = PyscrollGroup(map_layer=map_layer, default_layer=0)
        level_info['tiled_map'] = tiled_map
        level_info['map_layer'] = map_layer
        level_info['sprite_group'] = sprite_group
