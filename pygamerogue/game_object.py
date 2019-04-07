'''
https://gamedev.stackexchange.com/questions/126353/how-to-rotate-an-image-in-pygame-without-losing-quality-or-increasing-size-or-mo
'''

import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        pygame.sprite.Sprite.__init__(self)
        self._position = [0, 0]
        self._old_position = self.position
        self.angle = 0
        self.original_image = image.copy()
        self.image = image
        self.rect = rect
        self.position = [rect.left, rect.top]

    def update(self, dt):
        self._old_position = self._position[:]
        self.rect.topleft = self._position
        # self.image = pygame.transform.rotate(self.original_image, self.angle)
        # x, y = self.rect.center
        # self.rect = self.image.get_rect()
        # self.rect.center = (x, y)

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)
