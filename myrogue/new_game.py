import os
import pygame
from .player import Player
from .enemy import Enemy
from .game_over import GameOver
from .ammobar import AmmoBar
from .cashbar import CashBar
from .healthbar import HealthBar
from .new_world import NewWorld
from pygamerogue.game_object import GameObject
from .game_dialogs import GameDialog


FLOOR_ID = [33, 34, 35, 256, 257]


class NewGame(object):
    def __init__(self):
        self.create_essentials()
        self.world = NewWorld()  # load levels
        self.load_level()

    def load_level(self):
        self.level_info = self.world.get_level_info()
        self.map_layer = self.level_info['map_layer']
        self.sprite_group = self.level_info['sprite_group']
        self.tiled_map = self.level_info['tiled_map']
        self.start_points = self.level_info['start_points']
        if 'level_loaded' not in self.level_info:
            self.load_walls()
            self.load_objects()
            self.level_info['player'] = self.player
            self.sprite_group.add(self.player)
            self.level_info['level_loaded'] = True
        self.move_player_to_start()

    def create_player(self):
        player = Player()
        player.pressed_keys = list()
        return player
        
    def create_essentials(self):
        self.ui_group = pygame.sprite.Group()
        # intro = Intro(self.ui_group, True)
        dialog = GameDialog(self.ui_group, False)
        game_over = GameOver(self.ui_group, False)
        ammobar = AmmoBar(self.ui_group, True)
        healthbar = HealthBar(self.ui_group, True)
        cashbar = CashBar(self.ui_group, True)
        player = self.create_player()        
        player.healthbar = healthbar
        player.ammobar = ammobar
        player.cashbar = cashbar

        def attacked(self, damage):
            self.healthbar.dec_health(damage)
            if self.healthbar.health <= 0:
                self.killed(self, self.healthbar.health)

        def killed(self, health):
            if not game_over.visible:
                game_over.show('killed')

        player.attacked = attacked
        player.killed = killed
        self.player = player
        self.game_over = game_over
        self.dialog = dialog

    def load_walls(self):
        self.level_info['walls'] = list()
        tile_height = self.tiled_map.tileheight
        tile_width = self.tiled_map.tilewidth
        for x, y, gid in self.tiled_map.get_layer_by_name('floor'):
            if gid in FLOOR_ID:
                self.level_info['walls'].append(
                    pygame.Rect(
                        x * tile_width, y * tile_height,
                        tile_width, tile_height
                    )
                )

    def save_object_rect(self, obj_type, obj_rect):
        """
        https://stackoverflow.com/a/3483652/1104612
        """
        self.level_info.setdefault(obj_type, []).append(obj_rect)

    def create_game_object(self, obj_type, name, image, rect):
        if obj_type == 'enemy':
            return Enemy(image, rect, self.tiled_map, self.player)
        elif obj_type == 'NPC':
            obj = GameObject(image, rect)
            obj.dialog_id = name
            if name == 'Roger':
                obj.loot = {'cash': 100}
            elif name == 'Elmo':
                obj.loot = {'cash': 300}
            elif name == 'Gregory':
                obj.loot = {'cash': 150}
            elif name == 'Zero':
                obj.loot = {'cash': 500}
            elif name == 'Jim':
                obj.loot = {'cash': 200}
            elif name == 'Edmund':
                obj.loot = {'cash': 1000}
            elif name == 'Man in Black':
                self.mib = obj
            return obj
        elif obj_type == 'portal':
            obj = GameObject(image, rect)
            obj.level_id = name
            return obj
        else:
            return GameObject(image, rect)

    def load_tiled_object(self, tiled_object):
        rect = pygame.Rect(
            tiled_object.x, tiled_object.y,
            tiled_object.width, tiled_object.height
        )
        self.save_object_rect(tiled_object.type, rect)
        obj = self.create_game_object(
            tiled_object.type,
            tiled_object.name,
            tiled_object.image,
            rect
        )
        self.sprite_group.add(obj)

    def load_objects(self):
        for tiled_object in self.tiled_map.objects:
            self.load_tiled_object(tiled_object)

    def move_player_to_start(self):
        previous_level = self.world.previous_level
        if previous_level and previous_level in self.start_points:
            start_point_id = previous_level
        else:
            start_point_id = self.start_points[0]
        start_point = self.tiled_map.get_object_by_name(start_point_id)
        self.player.position = [start_point.x, start_point.y]
