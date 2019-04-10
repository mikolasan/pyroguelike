import pygame
from .camera import Camera

GAME_TITLE = 'Not your father\'s roguelike'


class Engine:
    def __init__(self, screen_size):
        self.playing = False
        pygame.init()
        pygame.font.init()
        # pygame.key.set_repeat(200, 100) # Doesn't work on repl.it
        self.size = screen_size
        flags = 0#pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(screen_size, flags)
        self.fps = 60.0
        self.camera = Camera(lambda: True, screen_size[0], screen_size[1])
        self.controllers = list()

    def add(self, controller):
        self.controllers.append(controller)
        controller.engine = self

    def run(self):
        self.playing = True
        clock = pygame.time.Clock()
        while self.playing:
            dt = clock.tick(self.fps) / 1000.
            events = pygame.event.get()
            self.update(dt, events)
            self.draw(self.screen, None)
            caption = "{} - FPS: {:.2f}".format(GAME_TITLE, clock.get_fps())
            pygame.display.set_caption(caption)
        pygame.quit()

    def stop(self):
        self.playing = False

    def reset(self):
        for c in self.controllers:
            c.reset()

    def update(self, dt, events):
        for c in self.controllers:
            c.update(dt, events)

    def draw(self, screen, camera):
        back = 14, 19, 25
        screen.fill(back)
        for c in self.controllers:
            c.draw(screen, camera)
        pygame.display.flip()
