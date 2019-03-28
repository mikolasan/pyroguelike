'''
https://gamedev.stackexchange.com/questions/126353/how-to-rotate-an-image-in-pygame-without-losing-quality-or-increasing-size-or-mo
'''

import pygame


class AdvancedSprite(pygame.sprite.Sprite):

    def __init__(self, imagepath, pos=(0, 0)):
        super(AdvancedSprite, self).__init__()
        self.original_image = pygame.image.load(imagepath).convert()
        self.image = self.original_image
        self.rect = self.image.get_rect().move(pos)
        self.angle = 0

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
