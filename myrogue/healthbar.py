import math
import pygame


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, ui_group, visible):
        pygame.sprite.Sprite.__init__(self)
        self.offset = (10, 10)
        self.pos = (0, 0)
        self.max_width = 250
        self.size = (self.max_width, 20)
        self.max_health = 100
        self.health = self.max_health
        self.bg_color = (0, 40, 0)
        self.bar_color = (240, 10, 0)
        self.background = pygame.Surface(self.size)
        self.background.fill(self.bg_color)
        self.bg_rect = self.background.get_rect()
        self.bg_rect.move_ip(self.pos)
        self.font = pygame.font.Font('font.ttf', 20)

        self.bar = pygame.Surface(self.size)
        self.bar.fill(self.bar_color)
        self.bar_rect = self.bar.get_rect()
        self.bar_rect.move_ip(self.pos)

        self.image = self.bar
        self.rect = self.bar_rect

        self.group = ui_group
        self.add(self.group)

    def inc_health(self, plus):
        self.health += plus

    def dec_health(self, minus):
        self.health -= minus

    def update(self, dt):
        self.bar_rect.left = self.pos[0] + self.offset[0]
        self.bar_rect.top = self.pos[1] + self.offset[1]
        new_bar_rect = self.bar_rect.copy()
        new_bar_rect.width = math.floor((self.health / self.max_health) * self.max_width)
        new_bar_rect = pygame.Rect((0, 0), self.size)
        new_bar_rect.width = math.floor((self.health / self.max_health) * self.max_width)

        self.title_image = self.font.render('Health ', True, (240, 240, 240))
        self.bar.fill(self.bg_color)
        self.bar.fill(self.bar_color, rect=new_bar_rect)
        self.bar.blit(self.title_image, [0,0])
