import os
import pygame
from pygamerogue.game_object import GameObject

def load_image(name):
    path = os.path.join('resources', 'knight', name)
    image = pygame.image.load(path).convert_alpha()
    return image


class Player(GameObject):
    def __init__(self):
        image = load_image('knight_m_idle_anim_f0.png')
        super().__init__(image, image.get_rect())
        self.idle_anim = []
        self.idle_anim.append(load_image('knight_m_idle_anim_f0.png'))
        self.idle_anim.append(load_image('knight_m_idle_anim_f1.png'))
        self.idle_anim.append(load_image('knight_m_idle_anim_f2.png'))
        self.idle_anim.append(load_image('knight_m_idle_anim_f3.png'))

        self.run_anim = []
        self.run_anim.append(load_image('knight_m_run_anim_f0.png'))
        self.run_anim.append(load_image('knight_m_run_anim_f1.png'))
        self.run_anim.append(load_image('knight_m_run_anim_f2.png'))
        self.run_anim.append(load_image('knight_m_run_anim_f3.png'))

        self.hit_anim = []
        self.hit_anim.append(load_image('knight_m_hit_anim_f0.png'))

        self.state_anim = self.idle_anim
        self.index = 0
        self.animation_time = 0.1
        self.time = 0
        self.image = self.state_anim[self.index]
        # self.rect = pygame.Rect(0, 0, 16, 28)

    def start_movement(self):
        self.state_anim = self.run_anim

    def stop_movement(self):
        self.state_anim = self.idle_anim

    def update(self, dt):
        super().update(dt)
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        if type(dt) is not float:
            return
        self.time += dt
        if self.time > self.animation_time:
            self.index += 1
            if self.index >= len(self.state_anim):
                self.index = 0
            self.image = self.state_anim[self.index]
            self.time = 0