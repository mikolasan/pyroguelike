import random
import pygame
from pygamerogue.high_school import calc_angle_rad
from pygamerogue.utils import shift_rect
from .bullet import Bullet
from .enemy import Enemy
from .game import TestGame
from .game_over import GameOver
from .test_particles import TestParticles


ENEMY_SPAWN = pygame.USEREVENT
PLAYER_REPEAT_KEY = pygame.USEREVENT + 1


class GameController:
    def __init__(self):
        game = TestGame()
        self.game = game
        self.sprite_group = game.sprite_group
        self.objects = game.objects
        self.player = game.objects['player']
        # self.hero = hero
        # self.tiles = game.objects['tiles']
        self.enemies = game.objects['enemy']
        self.game_over = next(
            x for x in game.objects['ui'] if isinstance(x, GameOver))
        self.walls = game.objects['walls']
        # self.camera = game.camera
        self.tile_size = 48

        last_layer_id = len(self.sprite_group.layers())
        self.bullets = self.sprite_group.get_sprites_from_layer(last_layer_id)
        self.bullets_layer_id = last_layer_id
        #self.ask_new_enemy()

    def to_map_position(self, view_position):
        view_rect = self.game.map_layer.view_rect
        return [view_rect.x + view_position[0], view_rect.y + view_position[1]]

    def test_tile(self, x, y, predicate):
        return False

    def test_tile_wall(self, rect):
        #return self.test_tile(x, y, lambda: x == 'wall')
        for wall in self.walls:
            if rect.colliderect(wall):
                return True
        return False

    def test_tile_ammo(self, rect):
        for i, ammo in enumerate(self.game.objects['ammo']):
            if rect.colliderect(ammo):
                n = 2
                ammobar = self.player.ammobar
                if ammobar.ammo < ammobar.max_ammo:
                    ammobar.inc_ammo(n)
                    sprites = self.sprite_group.get_sprites_at(rect.center)
                    for sprite in sprites:
                        sprite.kill()
                    self.objects['ammo'].pop(i)
                    return True
        return False

    def test_tile_cash(self, rect):
        for i, cash in enumerate(self.game.objects['cash']):
            if rect.colliderect(cash):
                n = random.uniform(5, 20)
                cashbar = self.player.cashbar
                cashbar.inc_cash(n)
                sprites = self.sprite_group.get_sprites_at(rect.center)
                for sprite in sprites:
                    sprite.kill()
                self.game.objects['cash'].pop(i)
                return True
        return False

    def test_tile_health(self, rect):
        for i, health in enumerate(self.game.objects['health']):
            if rect.colliderect(health):
                n = 10
                cashbar = self.player.healthbar
                cashbar.inc_health(n)
                sprites = self.sprite_group.get_sprites_at(rect.center)
                for sprite in sprites:
                    sprite.kill()
                self.game.objects['health'].pop(i)
                return True
        return False

    def test_wall_collision(self, obj_rect):
        for wall in self.walls:
            if obj_rect.colliderect(wall):
                return True
        return False

    def test_direction(self, direction):
        test_rect = self.player.rect.copy()
        test_rect = shift_rect(test_rect, direction)
        return None if self.test_tile_wall(test_rect) else test_rect

    def move_player(self, direction):
        if direction is None:
            i = 0
            while i < len(self.player.pressed_keys):
                direction = self.player.pressed_keys[i]
                new_rect = self.test_direction(direction)
                if new_rect:
                    pygame.time.set_timer(PLAYER_REPEAT_KEY, 300)
                    self.player.position = (new_rect.x, new_rect.y)
                    self.test_tile_ammo(new_rect)
                    self.test_tile_cash(new_rect)
                    self.test_tile_health(new_rect)
                    return
                i += 1
        else:
            if self.player.pressed_keys.count(direction) > 0:
                self.player.pressed_keys.remove(direction)
            self.player.pressed_keys.append(direction)
            new_rect = self.test_direction(direction)
            if new_rect:
                pygame.time.set_timer(PLAYER_REPEAT_KEY, 150)
                self.player.position = (new_rect.x, new_rect.y)
                self.test_tile_ammo(new_rect)
                self.test_tile_cash(new_rect)
                self.test_tile_health(new_rect)

    def left_key_pressed(self):
        self.move_player('left')

    def right_key_pressed(self):
        self.move_player('right')

    def up_key_pressed(self):
        self.move_player('up')

    def down_key_pressed(self):
        self.move_player('down')

    def shoot_key_pressed(self):
        # print('shoot_key_pressed', self.player.rect.center, self.player.angle)
        if self.player.ammobar.ammo <= 0:
            return
        self.player.ammobar.dec_ammo(1)
        bullet = Bullet(self.player.rect.center, self.player.angle)
        self.bullets.append(bullet)
        self.sprite_group.add(bullet, layer=self.bullets_layer_id)

    def ask_new_enemy(self):
        delay = int(random.uniform(1, 3) * 1000)
        pygame.time.set_timer(ENEMY_SPAWN, delay)

    def spawn_enemy(self):
        world_pos = (1, 2)
        new_enemy = Enemy(world_pos, self.world, self.player)
        self.enemies.append(new_enemy)

    def test_enemy_collision(self, bullet):
        for i, enemy in enumerate(self.enemies):
            if bullet.rect.colliderect(enemy):
                # self.tiles.append(TestParticles(self.engine, enemy.rect.center, bullet.angle))
                sprites = self.sprite_group.get_sprites_at(enemy.center)
                if len(sprites) > 0:
                    sprites[0].kill()
                self.enemies.pop(i)
                return True
        return False

    def show_enemys_path(self, map_position):
        """Show enemy's path"""
        sprites = self.sprite_group.get_sprites_at(map_position)
        if len(sprites) > 0:
            sprite = sprites[0]
            sprite.show_path()
        else:
            print('no sprites detected')

    def update(self, dt, events):
        self.process_input(events)
        # for bullet in self.bullets:
        #     bullet.update(dt)
        # self.camera.update(self.player)
        self.sprite_group.center(self.player.rect.center)
        view_rect = self.game.map_layer.view_rect
        self.player.ammobar.pos = (view_rect.right, view_rect.top)
        self.player.cashbar.pos = (view_rect.left, view_rect.top)
        self.player.healthbar.pos = (view_rect.left, view_rect.top)
        self.player.update(events)
        self.sprite_group.update(dt)
        for bullet in self.bullets:
            if (self.test_wall_collision(bullet.rect)
                    or self.test_enemy_collision(bullet)):
                bullet.kill()

    def draw(self, screen, camera):
        self.sprite_group.draw(screen)
        # for bullet in self.bullets:
        #     bullet.draw(screen, camera)

    def reset(self):
        hp = self.player.healthbar
        hp.health = hp.max_health
        self.bullets.clear()
        self.enemies.clear()
        self.game_over.hide()

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.left_key_pressed()
                elif event.key == pygame.K_d:
                    self.right_key_pressed()
                elif event.key == pygame.K_w:
                    self.up_key_pressed()
                elif event.key == pygame.K_s:
                    self.down_key_pressed()
                elif event.key == pygame.K_f:
                    self.shoot_key_pressed()
                elif event.key == pygame.K_RETURN:
                    if self.game_over.visible:
                        self.engine.reset()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player.pressed_keys.remove('left')
                elif event.key == pygame.K_d:
                    self.player.pressed_keys.remove('right')
                elif event.key == pygame.K_w:
                    self.player.pressed_keys.remove('up')
                elif event.key == pygame.K_s:
                    self.player.pressed_keys.remove('down')
            elif event.type == pygame.MOUSEMOTION:
                obj = self.player.rect
                self.player.angle = calc_angle_rad(self.to_map_position(event.pos), (obj.centerx, obj.centery))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print('click', event.pos)
                # map_position = self.to_map_position(event.pos)
                # print('on map', map_position)
                # for enemy in self.enemies:
                #     if enemy.collidepoint(map_position):
                #         layer_x = enemy.x // self.tile_size
                #         layer_y = enemy.y // self.tile_size
                #         print('collide with:', enemy, layer_x, layer_y)
                #         self.show_enemys_path(map_position)
                self.shoot_key_pressed()
            elif event.type == ENEMY_SPAWN:
                self.spawn_enemy()
                self.ask_new_enemy()
            elif event.type == PLAYER_REPEAT_KEY:
                if len(self.player.pressed_keys) > 0:
                    self.move_player(None)
