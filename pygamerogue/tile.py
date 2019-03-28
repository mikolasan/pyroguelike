import pygame


class Tile:
    def __init__(self, size, pos, background_color, border_color, symbol, padding, text_color):
        self.size = size
        self.position = pos
        self.background_color = background_color
        self.border_color = border_color
        self.symbol = symbol
        self.text_padding = padding
        self.text_color = text_color
        self.make_image()

    def make_image(self):
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]
        self.font = pygame.font.Font('font.ttf', 40)
        self.image.fill(self.background_color)
        self.rendered_symbol = self.font.render(self.symbol, True, self.text_color)
        self.image.blit(self.rendered_symbol, self.text_padding)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


TileDB = {
    '-': {
        'background': (60, 60, 60),
        'border': (50, 100, 0),
        'text': (235, 235, 100),
        'symbol': '-',
        'padding': [0, 0],
    },
    '|': {
        'background': (50, 50, 50),
        'border': (50, 100, 0),
        'text': (235, 235, 100),
        'symbol': '|',
        'padding': [0, 0],
    },
    '.': {
        'background': (0, 0, 0),
        'border': (50, 100, 0),
        'text': (235, 235, 100),
        'symbol': '.',
        'padding': [0, 0],
    },
    '@': {
        'background': (50, 150, 50),
        'border': (50, 100, 0),
        'text': (235, 235, 100),
        'symbol': '@',
        'padding': [0, 0],
    },
    '!': {
        'background': (50, 50, 50),
        'border': (250, 0, 0),
        'text': (235, 5, 1),
        'symbol': '!',
        'padding': [0, 0],
    },
    '?': {
        'background': (50, 50, 50),
        'border': (250, 100, 0),
        'text': (235, 235, 100),
        'symbol': '?',
        'padding': [0, 0],
    },
    '$': {
        'background': (0, 250, 0),
        'border': (0, 200, 0),
        'text': (0, 235, 100),
        'symbol': '$',
        'padding': [0, 0],
    },
}

rogue_size = (48, 48)


class RogueTile(Tile):
    def __init__(self, world_pos, tile_id):
        preset = TileDB[tile_id]
        x = world_pos[0] * rogue_size[0]
        y = world_pos[1] * rogue_size[1]
        Tile.__init__(
            self,
            size=rogue_size,
            pos=(x, y),
            background_color=preset['background'],
            border_color=preset['border'],
            symbol=preset['symbol'],
            padding=preset['padding'],
            text_color=preset['text'])
