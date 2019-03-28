import os
import pygame


class Tile:
    def __init__(self, size, pos, background_color, border_color, symbol, padding, text_color):
        self.size = size
        self.background_color = background_color
        self.border_color = border_color
        self.symbol = symbol
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        #font_file = os.path.join('..', 'rc', 'font.ttf')
        self.font = pygame.font.Font('font.ttf', 40)
        self.text_padding = padding
        self.text_color = text_color
        self.rendered_symbol = self.font.render(self.symbol, True, self.text_color)

    def make_image(self):
        self.image.fill(self.background_color)
        self.image.blit(self.rendered_symbol, self.text_padding)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


TileDB = {
    'wall': {
        
    }
}


class RogueTile(Tile):
    def __init__(self, pos):
        Tile.__init__(
            self,
            size=(48, 48),
            pos=pos,
            background_color=(0, 0, 0),
            border_color=(255, 255, 255),
            symbol='.',
            padding=[0, 0],
            text_color=(255, 255, 255))
