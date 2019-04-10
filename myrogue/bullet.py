import math
import pygame
from pygamerogue.game_object import GameObject


class Bullet(GameObject):
    def __init__(self, position, angle):
        image = pygame.image.load('bullet.png').convert()
        rect = image.get_rect().move(position)
        super().__init__(image, rect)
        self.speed = 5
        self.angle = angle
        self.image.set_colorkey((255, 255, 255))

    def update(self, dt):
        self._position[0] += math.cos(self.angle) * self.speed
        self._position[1] -= math.sin(self.angle) * self.speed
        self._old_position = self._position[:]
        self.rect.topleft = self._position
        if self.angle is not None:
            width = self.original_rect.width
            height = self.original_rect.height
            x1, y1 = width / 2, height / 2
            self.image = pygame.transform.rotate(self.original_image, math.degrees(self.angle))
            x2, y2 = self.image.get_rect().center
            
            #print(x1, y1, x2, y2)
            cropped = pygame.Surface((width, height))
            cropped.set_colorkey((255, 255, 255))
            cropped.blit(self.image, (0, 0), area=pygame.Rect(x2 - x1,  y2 - y1, width, height))
            self.image = cropped
