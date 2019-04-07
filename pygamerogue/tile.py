import pygame


rogue_size = (48, 48)


def map_to_pixel(x, y):
    return x * rogue_size[0], y * rogue_size[1]


class Tile:
    def __init__(self, size, map_pos, pos, background_color, border_color, symbol, padding, text_color):
        self.size = size
        self.pos = {}
        if map_pos is not None:
            self.update_map_position(map_pos)
        else:
            self.set_rect_position(pos)
        self.background_color = background_color
        self.border_color = border_color
        self.symbol = symbol
        self.text_padding = padding
        self.text_color = text_color
        self.angle = 0
        self.make_image()

    def set_rect_position(self, position):
        self.pos['x'] = position[0]
        self.pos['y'] = position[1]
        self.map_pos = (position[0] // rogue_size[0], position[1] // rogue_size[1])
        self.update_rect_position()

    def update_map_position(self, map_pos):
        self.map_pos = map_pos
        self.pos['x'], self.pos['y'] = map_to_pixel(map_pos[0], map_pos[1])

    def update_rect_position(self):
        if hasattr(self, 'rect'):
            self.rect.left, self.rect.top = self.pos['x'], self.pos['y']

    def make_image(self):
        self.font = pygame.font.Font('font.ttf', 40)
        self.rendered_symbol = self.font.render(self.symbol, True, self.text_color)
        self.original_image = pygame.Surface(self.size)
        self.original_image.fill(self.background_color)
        self.original_image.blit(self.rendered_symbol, self.text_padding)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.update_rect_position()

    def update(self, events):
        self.update_rect_position()

    def draw(self, screen, camera):
        screen.blit(self.image, camera.applyrect(self.rect))


wall = {
    'background': (44, 61, 81),
    'border': (0, 0, 0),
    'text': (146, 154, 162),
    'symbol': '-',
    'padding': [0, 0],
}

TileDB = {
    '-': {
        **wall,
        'symbol': '-',
    },
    '|': {
        **wall,
        'symbol': '|',
    },
    '<': {
        **wall,
        'symbol': '<',
    },
    '.': {
        'background': (113, 118, 138),
        'border': (0, 0, 0),
        'text': (226, 199, 192),
        'symbol': '.',
        'padding': [0, 0],
    },
    '@': {
        'background': (44, 44, 44),
        'border': (50, 100, 0),
        'text': (91, 198, 208),
        'symbol': '@',
        'padding': [0, 0],
    },
    '!': {
        'background': (208, 221, 240),
        'border': (250, 0, 0),
        'text': (110, 25, 32),
        'symbol': '!',
        'padding': [0, 0],
    },
    '/': {
        'background': (92, 102, 15),
        'border': (250, 0, 0),
        'text': (249, 199, 52),
        'symbol': 'a',
        'padding': [0, 0],
    },
    '+': {
        'background': (146, 154, 162),
        'border': (250, 100, 0),
        'text': (44, 61, 81),
        'symbol': '+',
        'padding': [0, 0],
    },
    '$': {
        'background': (224, 219, 225),
        'border': (0, 200, 0),
        'text': (96, 106, 53),
        'symbol': '$',
        'padding': [0, 0],
    },
    'e': {
        'background': (254, 160, 47),
        'border': (250, 0, 0),
        'text': (222, 102, 0),
        'symbol': 'e',
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
