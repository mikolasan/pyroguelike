import math
import pygame
from pygame.transform import rotate


def rot_center(image, orig_rect, angle):
    """rotate an image while keeping its center and size
    https://www.pygame.org/wiki/RotateCenter?parent=CookBook
    """
    rot_image = rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image, rot_rect


def rot_center2(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect()
    return rot_image, rot_rect


class BallController:
    def __init__(self, objects):
        self.ball = objects[0]
        self.tiles = objects[1]
        self.speed = [2, 2]
        self.reset()

    def reset(self):
        pass

    def set_engine(self, engine):
        self.engine = engine

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.engine.stop()
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos[0], event.pos[1]
                self.ballrect = self.ball.rect
                c_x, c_y = self.ballrect.centerx, self.ballrect.centery
                angle = 0
                if x > c_x:
                    angle = math.atan((c_y - y) / (x - c_x))
                elif x == c_x:
                    angle = (math.pi / 2.) if y < c_y else (-math.pi / 2.)
                elif x < c_x:
                    angle = math.pi + math.atan((c_y - y) / (x - c_x))
                self.ball.angle = -90 + math.degrees(angle)

    def update(self, events):
        self.process_input(events)
        self.ball.update()
        # width, height = self.engine.size[0], self.engine.size[1]
        
        # self.ballrect = self.ballrect.move(self.speed)
        # if self.ballrect.left < 0 or self.ballrect.right > width:
        #     self.speed[0] = -self.speed[0]
        # if self.ballrect.top < 0 or self.ballrect.bottom > height:
        #     self.speed[1] = -self.speed[1]
       
        # self.ball, self.ballrect = rot_center2(
        #     self.original_ball,
        #     self.ballrect,
        #     math.degrees(self.angle)
        # )

        # self.ball, self.ballrect = rot_center(
        #     self.original_ball,
        #     self.original_ball.get_rect(),
        #     math.degrees(self.angle)
        # )
        
        # self.ballrect.left = width/2
        # self.ballrect.top = height/2

    def draw(self, screen):
        screen.blit(self.ball.image, self.ball.rect)
        for tile in self.tiles:
            tile.draw(screen)
