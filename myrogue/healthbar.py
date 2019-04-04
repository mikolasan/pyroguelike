import math
import pygame


class HealthBar:
    def __init__(self):
        self.pos = (10, 10)
        self.max_width = 200
        self.size = (self.max_width, 20)
        self.max_health = 100
        self.health = self.max_health
        self.bg_color = (0, 40, 0)
        self.bar_color = (240, 10, 0)
        self.background = pygame.Surface(self.size)
        self.background.fill(self.bg_color)
        self.bg_rect = self.background.get_rect()
        self.bg_rect.move_ip(self.pos)
        self.bar = pygame.Surface(self.size)
        self.bar.fill(self.bar_color)
        self.bar_rect = self.bar.get_rect()
        self.bar_rect.move_ip(self.pos)

    def inc_health(self, plus):
        self.health += plus

    def dec_health(self, minus):
        self.health -= minus

    def update(self, events):
        new_bar_rect = self.bar_rect.copy()
        new_bar_rect.width = math.floor((self.health / self.max_health) * self.max_width)
        #self.bar.set_clip(new_bar_rect)
        #print(self.bar_rect, new_bar_rect)

    def draw(self, screen, camera):
        #print(self.bg_rect, self.bar_rect)
        #screen.blit(self.background, self.bg_rect)
        new_bar_rect = pygame.Rect((0, 0), self.size)
        new_bar_rect.width = math.floor((self.health / self.max_health) * self.max_width)

        self.bar.fill(self.bg_color)
        self.bar.fill(self.bar_color, rect=new_bar_rect)
        screen.blit(self.bar, self.bar_rect)
