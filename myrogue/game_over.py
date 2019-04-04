import pygame


class GameOver:
    def __init__(self):
        self.image = pygame.Surface((800, 600))
        self.bg_color = (0, 0, 0, 50)
        self.text_color = (250, 0, 0)
        self.font = pygame.font.Font('font.ttf', 40)
        self.text = self.font.render('Game Over', True, self.text_color)
        self.image.fill(self.bg_color)
        self.image.blit(self.text, [200, 200])
        self.visible = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self, events):
        pass

    def draw(self, screen, camera):
        if self.visible:
            screen.blit(self.image, self.image.get_rect())
