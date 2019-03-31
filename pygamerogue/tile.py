import pygame


rogue_size = (48, 48)


def map_to_pixel(x, y):
    return x * rogue_size[0], y * rogue_size[1]


class Tile:
    def __init__(self, size, map_pos, pos, background_color, border_color, symbol, padding, text_color):
        self.size = size
        if map_pos is not None:
            x, y = map_to_pixel(map_pos[0], map_pos[1])
            self.position = {'x': x, 'y': y}
        else:
            self.position = {'x': pos[0], 'y': pos[1]}
        self.background_color = background_color
        self.border_color = border_color
        self.symbol = symbol
        self.text_padding = padding
        self.text_color = text_color
        self.angle = 0
        self.make_image()

    def make_image(self):
        self.font = pygame.font.Font('font.ttf', 40)
        self.rendered_symbol = self.font.render(self.symbol, True, self.text_color)
        self.original_image = pygame.Surface(self.size)
        self.original_image.fill(self.background_color)
        self.original_image.blit(self.rendered_symbol, self.text_padding)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = map_to_pixel(self.position['x'], self.position['y'])

    def update(self, events):
        self.rect.left, self.rect.top = map_to_pixel(self.position['x'], self.position['y'])

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


class RogueTile(Tile):
    def __init__(self, map_pos, tile_id):
        preset = TileDB[tile_id]
        Tile.__init__(
            self,
            size=rogue_size,
            map_pos=map_pos,
            pos=None,
            background_color=preset['background'],
            border_color=preset['border'],
            symbol=preset['symbol'],
            padding=preset['padding'],
            text_color=preset['text'])
