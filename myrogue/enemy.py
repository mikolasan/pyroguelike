import pygame
from .enemy_pathfinder import EnemyPathfinder
from pygamerogue.game_object import GameObject


class Enemy(GameObject):
    def __init__(self, image, rect, tiled_map, player):
        super().__init__(image, rect)
        self.tiled_map = tiled_map
        self.player = player
        self.tile_size
        self.damage = 10
        self.last_update = pygame.time.get_ticks()
        self.update_delay = 300
        self.ai = EnemyPathfinder(self.tiled_map, self._position)

    def path_to_player(self):
        start = (self.position[0] // self.tile_size, self.position[1] // self.tile_size)
        goal = (self.player.position[0] // self.tile_size, self.player.position[1] // self.tile_size)
        if abs(start[0] - goal[0]) > 5 and abs(start[1] - goal[1]) > 5:
            return None
        return self.ai.astar(start, goal)

    def show_path(self):
        path = self.path_to_player()
        if path is None:
            pass
        else:
            start = (self.position[0] // self.tile_size, self.position[1] // self.tile_size)
            goal = (self.player.position[0] // self.tile_size, self.player.position[1] // self.tile_size)
            # print(start, goal, list(path))

    def update(self, dt):
        delta = pygame.time.get_ticks() - self.last_update
        if delta < self.update_delay:
            return
        #print(delta)
        self.attack_player()
        self.change_position()
        self._old_position = self._position[:]
        self.rect.topleft = self._position

    def change_position(self):
        dx = abs(self.rect.x - self.player.rect.x)
        dy = abs(self.rect.y - self.player.rect.y)
        if dx <= self.tile_size and dy <= self.tile_size:
            self.last_update = pygame.time.get_ticks()
            return
        else:
            path = self.path_to_player()
            if path is None:
                pass
            else:
                path = list(path)
                if len(path) > 2:
                    cell = path[1]
                    self.position = tuple(x * self.tile_size for x in cell)
                else:
                    print('i\'ll stay')

        self.last_update = pygame.time.get_ticks()

    def attack_player(self):
        dx = abs(self.rect.x - self.player.rect.x)
        dy = abs(self.rect.y - self.player.rect.y)
        if dx <= self.tile_size and dy <= self.tile_size:
            self.player.attacked(self.player, self.damage)
