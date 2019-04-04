import pygame
from .action_controller import ActionController
from .game_over import GameOver
from .healthbar import HealthBar
from .enemy import Enemy
from .world import get_world
from pygamerogue.tile import RogueTile
from pygamerogue.camera import Camera


class TestGame:
    def __init__(self):
        game_over = GameOver()
        healthbar = HealthBar()
        player = RogueTile((0, 0), '@')
        player.healthbar = healthbar

        def attacked(self, damage):
            self.healthbar.dec_health(damage)
            if self.healthbar.health <= 0:
                self.killed(self, self.healthbar.health)

        def killed(self, health):
            game_over.show()

        player.attacked = attacked
        player.killed = killed
        self.world = get_world()
        self.objects = {
            'tiles': [],
            'walls': [],
            'enemies': [],
            'ui': [healthbar, game_over]
        }
        world_height = len(self.world) * 48
        world_width = 0
        for y, row in enumerate(self.world):
            world_width = max(world_width, len(row))
            for x, s in enumerate(row):

                if s == ' ':
                    pass
                elif s == '@':
                    player.update_map_position((x, y))
                    self.objects['player'] = player
                    self.objects['tiles'].append(RogueTile((x, y), '.'))
                elif s == '|' or s == '-':
                    self.objects['walls'].append(RogueTile((x, y), s))
                elif s == 'e':
                    self.objects['enemies'].append(
                        Enemy((x, y), self.world, player)
                    )
                    self.objects['tiles'].append(RogueTile((x, y), '.'))
                else:
                    self.objects['tiles'].append(RogueTile((x, y), s))

        world_width *= 48
        screen_width = 800
        screen_height = 600

        def simple_camera_controller(camera: pygame.Vector2, target_rect: pygame.Rect) -> pygame.Vector2:
            x = screen_width/2 - target_rect.centerx
            y = screen_height/2 - target_rect.centery
            return pygame.Vector2(x, y)
            # return camera + (pygame.Vector2((x, y)) - camera) * 0.02

        def complex_camera_controller(camera: pygame.Vector2, target_rect: pygame.Rect) -> pygame.Vector2:
            x = screen_width/2 - target_rect.centerx
            y = screen_height/2 - target_rect.centery
            camera += (pygame.Vector2((x, y)) - camera) * 0.02
            camera.x = max(-world_width + screen_width, min(0, camera.x))
            camera.y = max(-world_height + screen_height, min(0, camera.y))
            return camera

        self.camera = Camera(complex_camera_controller, world_width, world_height)
        self.controller = ActionController()
        self.controller.world = self.world
        self.controller.objects = self.objects
        self.controller.player = self.objects['player']
        self.controller.tiles = self.objects['tiles']
        self.controller.enemies = self.objects['enemies']
        self.controller.game_over = next(x for x in self.objects['ui'] if isinstance(x, GameOver))
        self.controller.walls = []
        for tile in self.objects['walls']:
            self.controller.walls.append(tile.rect)
        self.controller.camera = self.camera

    def link(self, engine):
        engine.camera = self.camera
        self.controller.set_engine(engine)
        engine.add_scene('dungeon', self.objects, self.controller)
        engine.show_scene('dungeon')
