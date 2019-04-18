import pygame


class CashBar(pygame.sprite.Sprite):
    def __init__(self, ui_group, visible):
        pygame.sprite.Sprite.__init__(self)
        self.offset = (10, 40)
        self.pos = (0, 0)
        self.max_width = 250
        self.size = (self.max_width, 22)
        self.max_cash = 100
        self.cash = 0
        self.bg_color = (0, 40, 0)

        self.text_color = (0, 250, 0)
        self.font = pygame.font.Font('font.ttf', 20)
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()

        self.update_text()

        self.group = ui_group
        self.add(self.group)

    def update_text(self):
        self.text = '$%d.00' % self.cash
        self.text_image = self.font.render(self.text, True, self.text_color)
        self.title_image = self.font.render('Cash', True, (240, 240, 240))
        self.image.fill(self.bg_color)
        self.image.blit(self.title_image, [0,0])
        text_rect = self.text_image.get_rect()
        self.image.blit(self.text_image, [self.max_width - text_rect.width - 1, 1])

    def inc_cash(self, plus):
        self.cash += plus
        self.update_text()

    def dec_cash(self, minus):
        self.cash -= minus
        self.update_text()

    def update(self, dt):
        self.rect.left = self.pos[0] + self.offset[0]
        self.rect.top = self.pos[1] + self.offset[1]
