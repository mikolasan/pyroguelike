import os
import pygame
from .enemy import Enemy
from .game_over import GameOver
from .ammobar import AmmoBar
from .cashbar import CashBar
from .healthbar import HealthBar
from .world import World
from pygamerogue.game_object import GameObject
from .game_dialogs import GameDialog


FLOOR_ID = [1, 2]


class TestGame(object):
    def __init__(self):
        self.create_essentials()
        self.world = World()  # load levels
        self.load_level()

    def load_level(self):
        self.level_info = self.world.get_level_info()
        self.map_layer = self.level_info['map_layer']
        self.sprite_group = self.level_info['sprite_group']
        self.tiled_map = self.level_info['tiled_map']
        self.start_point = self.level_info['start_point']
        self.load_objects()
        self.fill_level()

    def create_essentials(self):
        self.ui_group = pygame.sprite.Group()
        dialog = GameDialog(self.ui_group, False)
        game_over = GameOver(self.ui_group, False)
        ammobar = AmmoBar(self.ui_group, True)
        healthbar = HealthBar(self.ui_group, True)
        cashbar = CashBar(self.ui_group, True)
        path = os.path.join('resources', 'player.png')
        player_image = pygame.image.load(path).convert_alpha()
        player = GameObject(player_image, player_image.get_rect())
        player.pressed_keys = list()
        player.healthbar = healthbar
        player.ammobar = ammobar
        player.cashbar = cashbar

        def attacked(self, damage):
            self.healthbar.dec_health(damage)
            if self.healthbar.health <= 0:
                self.killed(self, self.healthbar.health)

        def killed(self, health):
            game_over.show()

        player.attacked = attacked
        player.killed = killed
        self.player = player
        self.game_over = game_over
        self.dialog = dialog

    def load_objects(self):
        self.objects = {
            'NPC': [],
            'walls': [],
            'ammo': [],
            'health': [],
            'cash': [],
            'enemy': [],
            'door': [],
            'portal': [],
        }

        tile_height = self.tiled_map.tileheight
        tile_width = self.tiled_map.tilewidth
        for x, y, gid in self.tiled_map.get_layer_by_name('floor'):
            if gid in FLOOR_ID:
                self.objects['walls'].append(
                    pygame.Rect(
                        x * tile_width, y * tile_height,
                        tile_width, tile_height
                    )
                )

        for tiled_object in self.tiled_map.objects:
            rect = pygame.Rect(
                tiled_object.x, tiled_object.y,
                tiled_object.width, tiled_object.height
            )
            self.objects[tiled_object.type].append(rect)
            if tiled_object.type == 'enemy':
                obj = Enemy(tiled_object.image, rect, self.tiled_map, self.player)
            elif tiled_object.type == 'NPC':
                print('NPC', rect)
                obj = GameObject(tiled_object.image, rect)
                obj.dialog_id = tiled_object.name
                if obj.dialog_id == 'Man in Black':
                    self.mib = obj
            elif tiled_object.type == 'portal':
                obj = GameObject(tiled_object.image, rect)
                obj.level_id = tiled_object.name
            else:
                obj = GameObject(tiled_object.image, rect)
            self.sprite_group.add(obj)

    def fill_level(self):
        player = self.player
        start_point = self.tiled_map.get_object_by_name(self.start_point)
        player.position = [start_point.x, start_point.y]
        self.objects['player'] = player
        self.sprite_group.add(player)
