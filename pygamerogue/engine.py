import pygame


class Engine:
    def __init__(self, screen_size):
        self.playing = False
        pygame.init()
        pygame.font.init()
        self.size = screen_size
        flags = 0 #pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(screen_size, flags)
        self.scenes = {}

    def load(self, game):
        game.link(self)

    def run(self, controller):
        self.playing = True
        clock = pygame.time.Clock()
        while self.playing:
            events = pygame.event.get()
            controller.update(events)
            self.update(events)
            self.draw()
            clock.tick(50)
        pygame.quit()

    def stop(self):
        self.playing = False

    def reset(self):
        for scene_name, scene in self.scenes.items():
            scene['controller'].reset()

    def update(self, events):
        for scene_name, scene in self.scenes.items():
            if scene['visibility']:
                scene['controller'].update(events)

    def draw(self):
        black = 0, 0, 0
        self.screen.fill(black)
        for scene_name, scene in self.scenes.items():
            if scene['visibility']:
                scene['controller'].draw(self.screen)
        pygame.display.update()

    def add_scene(self, name, objects, controller):
        self.scenes[name] = {
            'objects': objects,
            'controller': controller,
            'visibility': False
        }

    def show_scene(self, name):
        self.scenes[name]['visibility'] = True
