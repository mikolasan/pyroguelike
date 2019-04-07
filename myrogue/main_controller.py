import pygame


class MainController:
    def __init__(self):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.engine.stop()

    def draw(self, screen, camera):
        pass
