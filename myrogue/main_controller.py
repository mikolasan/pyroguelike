import pygame


class MainController:
    def __init__(self, engine):
        self.engine = engine

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.engine.reset()
