'''
https://stackoverflow.com/a/14357169/1104612
'''

import pygame


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def apply(self, target):
        return target.rect.move(self.offset)

    def applyrect(self, target_rect):
        return target_rect.move(self.offset)

    def update(self, target):
        self.offset = self.camera_func(self.offset, target.rect)
