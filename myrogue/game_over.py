import pygame


class GameOver(pygame.sprite.Sprite):
    def __init__(self, ui_group, visible):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((800, 600))
        self.bg_color = (0, 0, 0, 50)
        self.text_color = (250, 0, 0)
        self.font = pygame.font.Font('font.ttf', 40)
        self.text = self.font.render('Game Over', True, self.text_color)
        self.image.fill(self.bg_color)
        self.image.blit(self.text, [200, 200])
        self.rect = self.image.get_rect()

        self.group = ui_group
        if visible:
            self.show()
        else:
            self.hide()

    def show(self):
        self.visible = True
        self.add(self.group)

    def hide(self):
        self.visible = False
        self.remove(self.group)

    def update(self, events):
        pass

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)
