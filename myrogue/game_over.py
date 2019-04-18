import pygame


def text_generator(text):
    '''
    https://stackoverflow.com/questions/31381169/pygame-scrolling-dialogue-text
    '''
    tmp = ''
    for letter in text:
        tmp += letter
        # don't pause for spaces
        if letter != ' ':
            yield tmp


def empty_generator():
    """
    https://stackoverflow.com/a/6395088/1104612
    """
    return
    yield


SCROLL_TEXT_UPDATE = pygame.USEREVENT + 4


game_over_text = {
    'killed': {
        'title': 'Game Over',
        'epilogue': """
This was a long life suddenly
ended by extraterrestrial
creature with big red eyes...

As soon as it is really hardcore
roguelike, you have to restart
this repl to start over
"""
    },
    'done': {
        'title': 'The End',
        'epilogue': """
It happened to be a good day.
Tomorrow and may be a whole next
week Jeff can live without
any worries...

To try another walkthrough
you have to restart
this repl to start over
"""
    }
}


class GameOver(pygame.sprite.Sprite):
    def __init__(self, ui_group, visible):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((800, 600))
        self.rect = self.image.get_rect()
        self.title_font = pygame.font.Font('troika.ttf', 40)
        self.font = pygame.font.Font('troika.ttf', 20)
        self.bg_color = (0, 0, 0, 50)
        self.title_color = (250, 0, 0)
        self.text_color = (250, 250, 250)

        self.visible = False
        self.group = ui_group

    def show(self, result):
        self.result = result
        self.visible = True
        self.add(self.group)
        pygame.time.set_timer(SCROLL_TEXT_UPDATE, 100)
        self.displayed_text = text_generator(game_over_text[self.result]['epilogue'])

    def hide(self):
        self.visible = False
        self.remove(self.group)

    def blit_text(self, surface, text, pos, font, color=pygame.Color('black')):
        """
        https://stackoverflow.com/a/42015712/1104612
        """
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        max_height -= 100
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height + 15  # Start on new row.

    def rewind(self):
        self.displayed_text = empty_generator()

    def update(self, events):
        for event in events:
            if event.type == SCROLL_TEXT_UPDATE:
                self.image.fill(self.bg_color)
                self.title = self.title_font.render(game_over_text[self.result]['title'], True, self.title_color)
                self.title_rect = self.title.get_rect()
                self.title_rect.centerx = self.rect.centerx
                self.title_rect.top = 80
                self.image.blit(self.title, self.title_rect)
                try:
                    message = next(self.displayed_text)
                except StopIteration:
                    pygame.time.set_timer(SCROLL_TEXT_UPDATE, 0)
                    message = game_over_text[self.result]['epilogue']
                self.blit_text(self.image, message, (100, 150), self.font, self.text_color)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.rewind()
