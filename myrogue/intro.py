import pygame


class Intro(pygame.sprite.Sprite):
    def __init__(self, ui_group, visible):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((800, 600))
        self.rect = self.image.get_rect()
        self.bg_color = (0, 0, 0, 50)
        
        self.group = ui_group

    def show(self):
        self.visible = True
        self.add(self.group)

    def hide(self):
        self.visible = False
        self.remove(self.group)
