import pygame
from pygamerogue.dialog import Dialog

POSITIVE_DIALOG_RESULT = pygame.USEREVENT + 2
NEGATIVE_DIALOG_RESULT = pygame.USEREVENT + 3

conversation_is_over = -1
conversation_result_positive = -2
conversation_result_negative = -3
dialogs = {
    'Barman Joe': [
        [
            # 0
            "How are you doing?",
            "I'm OK", 1,
            "Doing good. What about you?", 2,
        ],
        [
            # 1
            "Wonna drink?",
            "Sure", conversation_result_positive,
            "I don't drink", 3,
        ],
        [
            # 2
            "Are you OK?",
            "I'm OK", 1,
            "Bye", conversation_is_over,
        ],
        [
            # 3
            "Get out of here nerd!",
            "OK", conversation_result_negative,
            "Fine, give me a beer", conversation_result_positive,
        ],
    ],
    'Man in Black': [
        [
            # 0
            "Hey, pss",
            "Ah?", 1,
            "** no reaction **", conversation_is_over,
        ],
        [
            # 1
            "Do you want a secret job?",
            "Secret?", 2,
            "Have you seen restrooms sign?", conversation_is_over,
        ],
        [
            # 2
            "We pay real money",
            "That's what I was looking for", conversation_result_positive,
            "I happy with my life", conversation_result_negative,
        ],
    ],
}


class GameDialog(Dialog):
    def next_step(self, step_id):
        self.conversation_step = step_id
        if step_id == conversation_is_over:
            self.hide()
        elif step_id == conversation_result_positive:
            self.hide()
            pygame.event.post(pygame.event.Event(POSITIVE_DIALOG_RESULT))
        elif step_id == conversation_result_negative:
            self.hide()
            pygame.event.post(pygame.event.Event(NEGATIVE_DIALOG_RESULT))
        else:
            self.show_step()

    def start_for(self, dialog_id):
        self.name = dialog_id
        self.conversation_step = 0
        self.show_step()

    def show_step(self):
        conversation = dialogs[self.name]
        d = conversation[self.conversation_step]
        question = d[0]
        answer1 = d[1]
        answer1_cb = lambda: self.next_step(d[2])
        answer2 = d[3]
        answer2_cb = lambda: self.next_step(d[4])
        self.show_question(question, answer1, answer2, answer1_cb, answer2_cb)
