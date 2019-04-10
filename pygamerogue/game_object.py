'''
https://gamedev.stackexchange.com/questions/126353/how-to-rotate-an-image-in-pygame-without-losing-quality-or-increasing-size-or-mo
'''
import math
import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        pygame.sprite.Sprite.__init__(self)
        self._position = [0, 0]
        self._old_position = self.position
        self.angle = None
        self.original_image = image.copy()
        self.image = image
        self.original_rect = rect.copy()
        self.rect = rect
        self.position = [rect.left, rect.top]

    def update(self, dt):
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
            cropped.blit(self.image, (0, 0), area=pygame.Rect(x2 - x1,  y2 - y1, width, height))
            self.image = cropped
            # self.rect = self.image.get_rect()
            # self.rect.center = (x, y)
            # self._position = self.rect.topleft

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)
