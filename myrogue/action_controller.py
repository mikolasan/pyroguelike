import random
import pygame
from pygamerogue.high_school import calc_angle_rad
from .bullet import Bullet
from .enemy import Enemy
from .test_particles import TestParticles


ENEMY_SPAWN = pygame.USEREVENT


class ActionController:
    def __init__(self, objects):
        self.objects = objects
        self.player = objects['player']
        self.tiles = objects['tiles']
        self.enemies = objects['enemies']
        walls = objects['walls']
        self.walls = []
        for tile in walls:
            self.walls.append(tile.rect)
        self.speed = 48
        self.bullets = []
        self.ask_new_enemy()

    def set_engine(self, engine):
        self.engine = engine

    def left_key_pressed(self):
        self.player.position['x'] -= self.speed

    def right_key_pressed(self):
        self.player.position['x'] += self.speed

    def up_key_pressed(self):
        self.player.position['y'] -= self.speed

    def down_key_pressed(self):
        self.player.position['y'] += self.speed

    def shoot_key_pressed(self):
        bullet = Bullet(self.player.rect.center, self.player.angle)
        self.bullets.append(bullet)

    def ask_new_enemy(self):
        delay = int(random.uniform(1, 3) * 1000)
        pygame.time.set_timer(ENEMY_SPAWN, delay)

    def spawn_enemy(self):
        world_pos = (1, 1)
        new_enemy = Enemy(world_pos, self.player)
        self.enemies.append(new_enemy)

    def test_wall_collision(self, obj_rect):
        for wall in self.walls:
            if obj_rect.colliderect(wall):
                return True
        return False

    def test_enemy_collision(self, bullet):
        for i, enemy in enumerate(self.enemies):
            if bullet.rect.colliderect(enemy):
                self.tiles.append(TestParticles(self.engine, enemy.rect.center, bullet.angle))
                self.enemies.pop(i)
                return True
        return False

    def update(self, events):
        self.process_input(events)
        self.player.update(events)
        for bullet in self.bullets:
            bullet.update(events)
        self.bullets[:] = (x for x in self.bullets if not (self.test_wall_collision(x.rect) or self.test_enemy_collision(x)))

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left_key_pressed()
                elif event.key == pygame.K_RIGHT:
                    self.right_key_pressed()
                elif event.key == pygame.K_UP:
                    self.up_key_pressed()
                elif event.key == pygame.K_DOWN:
                    self.down_key_pressed()
                elif event.key == pygame.K_f:
                    self.shoot_key_pressed()
            elif event.type == pygame.MOUSEMOTION:
                obj = self.player.rect
                self.player.angle = calc_angle_rad(event.pos, (obj.centerx, obj.centery))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.shoot_key_pressed()
            elif event.type == ENEMY_SPAWN:
                self.spawn_enemy()
                self.ask_new_enemy()
