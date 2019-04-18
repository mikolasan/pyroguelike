import os
import pygame


class Dialog(pygame.sprite.Sprite):
    def __init__(self, ui_group, visible):
        pygame.sprite.Sprite.__init__(self)
        self.text_color = (50, 90, 90)
        self.selected_color = (50, 190, 90)
        self.font = pygame.font.Font('troika.ttf', 20)
        path = os.path.join('resources', 'dialog_back.png')
        self.back = pygame.image.load(path).convert()
        self.image = self.back.copy()
        self.selection = pygame.Surface((700, 65))
        self.selection_color = (80, 70, 60)
        self.selection.fill(self.selection_color)
        self.rect = self.image.get_rect().move((50, 320))

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

    def update_text(self):
        self.image.blit(self.back, [0, 0])
        rect = self.display_name.get_rect()
        rect.right = self.rect.right - 60
        rect.top = 20
        self.image.blit(self.display_name, rect)
        self.image.blit(self.question, [20, 70])
        self.image.blit(self.selection, [0, 120 + self.selection_id * 65])
        self.answer1 = self.font.render(self.text1, True, self.selected_color if self.selection_id == 0 else self.text_color)
        self.answer2 = self.font.render(self.text2, True, self.selected_color if self.selection_id == 1 else self.text_color)
        self.image.blit(self.answer1, [20, 140])
        self.image.blit(self.answer2, [20, 205])

    def show_question(self, name, question, answer1, answer2, answer1_cb, answer2_cb):
        self.display_name = self.font.render(name, True, self.text_color)
        self.question = self.font.render(question, True, self.text_color)
        self.text1 = answer1
        self.text2 = answer2
        self.answer1 = self.font.render(answer1, True, self.selected_color)
        self.answer2 = self.font.render(answer2, True, self.text_color)
        self.answer1_cb = answer1_cb
        self.answer2_cb = answer2_cb
        self.selection_id = 0
        self.update_text()
        self.show()

    def update(self, events):
        self.process_input(events)

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.selection_id = (self.selection_id + 1) % 2
                    self.update_text()
                elif event.key == pygame.K_s:
                    self.selection_id = abs((self.selection_id - 1) % 2)
                    self.update_text()
                elif event.key == pygame.K_RETURN:
                    if self.selection_id == 0:
                        self.answer1_cb()
                    else:
                        self.answer2_cb()
