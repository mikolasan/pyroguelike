import os
import random
import pygame
from pygamerogue.game_object import GameObject
from pygamerogue.high_school import calc_angle_rad
from pygamerogue.utils import shift_rect
from .bullet import Bullet
from .enemy import Enemy
from .new_game import NewGame
from .enemy_pieces import EnemyPieces
from .npc_pieces import NpcPieces


ENEMY_SPAWN = pygame.USEREVENT
PLAYER_REPEAT_KEY = pygame.USEREVENT + 1
POSITIVE_DIALOG_RESULT = pygame.USEREVENT + 2
NEGATIVE_DIALOG_RESULT = pygame.USEREVENT + 3


class MedievalController:
    def __init__(self):
        self.tile_size = 16
        game = NewGame()
        self.game = game
        self.update_level()

    def update_level(self):
        game = self.game
        self.sprite_group = game.sprite_group
        self.player = self.get_objects_by_type('player')
        self.enemies = self.get_objects_by_type('enemy')
        self.game_over = game.game_over
        self.dialog = game.dialog
        self.ui = game.ui_group
        self.effects = []
        
        last_layer_id = len(self.sprite_group.layers())
        self.bullets = self.sprite_group.get_sprites_from_layer(last_layer_id)
        self.bullets_layer_id = last_layer_id
        self.effects_layer_id = last_layer_id + 1

    def get_objects_by_type(self, obj_type):
        return self.game.level_info[obj_type] if obj_type in self.game.level_info else []

    def to_map_position(self, view_position):
        view_rect = self.game.map_layer.view_rect
        return [view_rect.x + view_position[0], view_rect.y + view_position[1]]

    def test_rect_collision(self, rect, obj_type, callback=None):
        for i, obj_rect in enumerate(self.get_objects_by_type(obj_type)):
            if rect.colliderect(obj_rect):
                if callback is not None:
                    callback(self, i)
                return True
        return False

    def test_center_collision(self, center, obj_type, callback=None):
        for i, obj_rect in enumerate(self.get_objects_by_type(obj_type)):
            if obj_rect.collidepoint(center):
                if callback is not None:
                    callback(self, i)
                return True
        return False

    def test_wall_collision(self, rect):
        return self.test_rect_collision(rect, 'walls')

    def test_portal_collision(self, rect):
        def change_level(self, i):
            rect = self.get_objects_by_type('portal')[i]
            sprites = self.sprite_group.get_sprites_at(rect.center)
            if len(sprites) > 0:
                level_id = sprites[0].level_id
                self.game.world.set_current_level(level_id)
                self.game.load_level()
                self.update_level()

        return self.test_rect_collision(rect, 'portal', change_level)

    def test_npc_collision(self, rect):
        def start_dialog(self, i):
            rect = self.get_objects_by_type('NPC')[i]
            sprites = self.sprite_group.get_sprites_at(rect.center)
            if len(sprites) > 0:
                dialog_id = sprites[0].dialog_id
                self.dialog.start_for(dialog_id)
                self.player.pressed_keys = list()

        return self.test_rect_collision(rect, 'NPC', start_dialog)

    def test_ammo_collision(self, rect):
        def take_ammo(self, i):
            n = 4
            ammobar = self.player.ammobar
            if ammobar.ammo < ammobar.max_ammo:
                ammobar.inc_ammo(n)
                sprites = self.sprite_group.get_sprites_at(rect.center)
                for sprite in sprites:
                    sprite.kill()
                self.get_objects_by_type('ammo').pop(i)
        return self.test_rect_collision(rect, 'ammo', take_ammo)

    def test_cash_collision(self, rect):
        def take_cash(self, i):
            cashbar = self.player.cashbar
            sprites = self.sprite_group.get_sprites_at(rect.center)
            for sprite in sprites:
                n = sprite.amount if hasattr(sprite, 'amount') else 20
                cashbar.inc_cash(n)
                sprite.kill()
            self.get_objects_by_type('cash').pop(i)
        return self.test_rect_collision(rect, 'cash', take_cash)

    def test_medkit_collision(self, rect):
        def take_medkit(self, i):
            n = 20
            healthbar = self.player.healthbar
            healthbar.inc_health(n)
            sprites = self.sprite_group.get_sprites_at(rect.center)
            for sprite in sprites:
                sprite.kill()
            self.get_objects_by_type('health').pop(i)
        return self.test_rect_collision(rect, 'health', take_medkit)

    def test_wall_center_collision(self, obj_center):
        return self.test_center_collision(obj_center, 'walls')

    def test_solid_tiles(self, rect):
        return self.test_wall_collision(rect) or self.test_npc_collision(rect)

    def test_direction(self, direction):
        test_rect = self.player.rect.copy()
        test_rect = shift_rect(test_rect, direction, self.tile_size)
        return None if self.test_solid_tiles(test_rect) else test_rect

    def move_player(self, direction):
        if self.player.pressed_keys.count(direction) > 0:
            self.player.pressed_keys.remove(direction)
        self.player.pressed_keys.append(direction)
        new_rect = self.test_direction(direction)
        if new_rect:
            self.on_player_move(new_rect)

    def continue_player_movement(self):
        # print('continue_player_movement')
        i = 0
        while i < len(self.player.pressed_keys):
            direction = self.player.pressed_keys[i]
            new_rect = self.test_direction(direction)
            if new_rect:
                self.on_player_move(new_rect)
                return
            i += 1
        
    def stop_player_movement(self):
        self.player.stop_movement()

    def on_player_move(self, new_rect):
        pygame.time.set_timer(PLAYER_REPEAT_KEY, 300)
        self.player.position = (new_rect.x, new_rect.y)
        self.player.start_movement()
        self.test_ammo_collision(new_rect)
        self.test_cash_collision(new_rect)
        self.test_medkit_collision(new_rect)
        self.test_portal_collision(new_rect)

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
        bullet = Bullet(self.player.rect.center, self.player._angle)
        self.bullets.append(bullet)
        self.sprite_group.add(bullet, layer=self.bullets_layer_id)

    def ask_new_enemy(self):
        delay = int(random.uniform(1, 3) * 1000)
        pygame.time.set_timer(ENEMY_SPAWN, delay)

    def spawn_enemy(self):
        world_pos = (1, 2)
        new_enemy = Enemy(world_pos, self.world, self.player)
        self.enemies.append(new_enemy)

    def add_loot(self, loot, pos):
        for obj_type, amount in loot.items():
            path = os.path.join('resources', 'cash.png')
            image = pygame.image.load(path).convert_alpha()
            rect = image.get_rect().move(pos)
            self.game.save_object_rect(obj_type, rect)
            obj = GameObject(image, rect)
            obj.amount = amount
            self.sprite_group.add(obj)

    def test_bullet_in_enemy(self, bullet):
        center = bullet.rect.center
        for i, enemy in enumerate(self.enemies):
            if enemy.collidepoint(center):
                enemy_pos = enemy.center
                sprites = self.sprite_group.get_sprites_at(enemy.center)
                if len(sprites) > 0:
                    sprites[0].kill()
                self.enemies.pop(i)

                pieces = EnemyPieces(enemy_pos, bullet.angle)
                self.sprite_group.add(pieces, layer=self.effects_layer_id)
                return True
        return False

    def test_bullet_in_npc(self, bullet):
        center = bullet.rect.center
        level_npc = self.get_objects_by_type('NPC')
        for i, npc in enumerate(level_npc):
            if npc.collidepoint(center):
                npc_pos = npc.center
                sprites = self.sprite_group.get_sprites_at(npc.center)
                if len(sprites) > 0:
                    obj = sprites[0]
                    if obj.loot:
                        self.add_loot(obj.loot, npc.topleft)
                    obj.kill()
                level_npc.pop(i)

                pieces = NpcPieces(npc_pos, bullet.angle)
                self.sprite_group.add(pieces, layer=self.effects_layer_id)
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
        self.sprite_group.center(self.player.rect.center)
        self.player.update(dt)
        self.sprite_group.update(events)
        for sprite in self.sprite_group.get_sprites_from_layer(self.effects_layer_id):
            if sprite.over:
                sprite.kill()

        self.ui.update(events)
        if self.dialog.visible:
            return

        if not self.game_over.visible and self.check_mission_status():
            self.game_over.show('done')
        self.process_input(events)
        for i, bullet in enumerate(self.bullets):
            if (self.test_wall_center_collision(bullet.rect.center)
                    or self.test_bullet_in_enemy(bullet)
                    or self.test_bullet_in_npc(bullet)):
                bullet.kill()
                self.bullets.pop(i)

    def draw(self, screen, camera):
        self.sprite_group.draw(screen)
        for obj in self.effects:
            obj.update(screen)
        self.ui.draw(screen)

    def check_mission_status(self):
        return (self.player.cashbar.cash >= self.player.cashbar.max_cash
                and self.game.world.current_level == 'bar')

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
                self.player._angle = calc_angle_rad(self.to_map_position(event.pos), (obj.centerx, obj.centery))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.shoot_key_pressed()
            elif event.type == ENEMY_SPAWN:
                self.spawn_enemy()
                self.ask_new_enemy()
            elif event.type == PLAYER_REPEAT_KEY:
                if len(self.player.pressed_keys) > 0:
                    # print(self.player.pressed_keys)
                    self.continue_player_movement()
                else:
                    self.stop_player_movement()
