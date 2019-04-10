import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup
from pytmx.util_pygame import load_pygame
from pygamerogue.rogue_renderer import RogueRenderer


class World(object):
    def __init__(self):
        self.tiled_map = load_pygame('test2.tmx')
        map_data = pyscroll.data.TiledMapData(self.tiled_map)
        self.map_layer = RogueRenderer(map_data, [800, 600], clamp_camera=True, tall_sprites=0)
        self.map_layer._redraw_cutoff = 100
        self.map_layer.zoom = 1
        self.sprite_group = PyscrollGroup(map_layer=self.map_layer, default_layer=0)
