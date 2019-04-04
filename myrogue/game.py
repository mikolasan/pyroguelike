from .action_controller import ActionController
from .game_over import GameOver
from .healthbar import HealthBar
from .world import get_world
from pygamerogue.tile import RogueTile


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
        for y, row in enumerate(self.world):
            for x, s in enumerate(row):
                if s == '@':
                    player.update_map_position((x, y))
                    self.objects['player'] = player
                elif s == '|' or s == '-':
                    self.objects['walls'].append(RogueTile((x, y), s))
                else:
                    self.objects['tiles'].append(RogueTile((x, y), s))
        self.controller = ActionController(self.world, self.objects)

    def link(self, engine):
        self.controller.set_engine(engine)
        engine.add_scene('dungeon', self.objects, self.controller)
        engine.show_scene('dungeon')
