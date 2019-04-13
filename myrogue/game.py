import pygame
from .enemy import Enemy
from .game_over import GameOver
from .ammobar import AmmoBar
from .cashbar import CashBar
from .healthbar import HealthBar
from .world import World
from pygamerogue.game_object import GameObject

FLOOR_ID = [2]


class TestGame(object):
    def __init__(self):
        game_over = GameOver()
        ammobar = AmmoBar()
        healthbar = HealthBar()
        cashbar = CashBar()
        player_image = pygame.image.load('player.png').convert_alpha()
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
        world = World()
        self.map_layer = world.map_layer
        self.sprite_group = world.sprite_group
        self.objects = {
            'walls': [],
            'ammo': [],
            'health': [],
            'cash': [],
            'enemy': [],
            'door': [],
            'portal': [],
            'player': player,
            'ui': [healthbar, ammobar, cashbar, game_over]
        }
        self.solid_objects = self.objects['walls'] + self.objects['enemy']
        tiled_map = world.tiled_map
        self.tiled_map = tiled_map
        start_point = tiled_map.get_object_by_name('level0')
        player.position = [start_point.x, start_point.y]
        
        tile_height = tiled_map.tileheight
        tile_width = tiled_map.tilewidth
        for x, y, gid in tiled_map.get_layer_by_name('floor'):
            if gid in FLOOR_ID:
                # print('wall:', x, y)
                self.objects['walls'].append(
                    pygame.Rect(
                        x * tile_width, y * tile_height,
                        tile_width, tile_height
                    )
                )

        only_one = False
        for tiled_object in tiled_map.objects:
            # print(tiled_object.x, tiled_object.y, tiled_object.type)
            rect = pygame.Rect(
                tiled_object.x, tiled_object.y,
                tiled_object.width, tiled_object.height
            )
            self.objects[tiled_object.type].append(rect)
            
            if tiled_object.type == 'enemy':
                if not only_one:
                    obj = Enemy(tiled_object.image, rect, tiled_map, player)
                    only_one = True
            else:
                obj = GameObject(tiled_object.image, rect)
            self.sprite_group.add(obj)
            # if tiled_object.name == 'level0':
            #     print(tiled_object.x, tiled_object.y)

        self.sprite_group.add(player)
        self.sprite_group.add(ammobar)
        self.sprite_group.add(cashbar)
        self.sprite_group.add(healthbar)

        #world_width *= 48
        screen_width = 800
        screen_height = 600

        # def simple_camera_controller(
        #         camera: pygame.Vector2,
        #         target_rect: pygame.Rect) -> pygame.Vector2:
        #     x = screen_width / 2 - target_rect.centerx
        #     y = screen_height / 2 - target_rect.centery
        #     return pygame.Vector2(x, y)
        #     # return camera + (pygame.Vector2((x, y)) - camera) * 0.02

        # def complex_camera_controller(
        #         camera: pygame.Vector2,
        #         target_rect: pygame.Rect) -> pygame.Vector2:
        #     x = screen_width / 2 - target_rect.centerx
        #     y = screen_height / 2 - target_rect.centery
        #     camera += (pygame.Vector2((x, y)) - camera) * 0.02
        #     camera.x = max(-world_width + screen_width, min(0, camera.x))
        #     camera.y = max(-world_height + screen_height, min(0, camera.y))
        #     return camera

        # self.camera = Camera(complex_camera_controller, world_width,
        #                      world_height)
        # self.controller.world = self.world
        
