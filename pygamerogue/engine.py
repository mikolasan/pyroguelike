import pygame


GAME_TITLE = 'Not your father\'s roguelike'

class Engine:
    def __init__(self, screen_size):
        self.playing = False
        pygame.init()
        pygame.font.init()
        self.size = screen_size
        flags = 0#pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(screen_size, flags)
        self.scenes = {}
        self.fps = 60.0

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
            clock.tick(self.fps)
            caption = "{} - FPS: {:.2f}".format(GAME_TITLE, clock.get_fps())
            pygame.display.set_caption(caption)
        pygame.quit()

    def stop(self):
        self.playing = False

    def reset(self):
        for scene_name, scene in self.scenes.items():
            scene['controller'].reset()

    def update(self, events):
        for scene_name, scene in self.scenes.items():
            if scene['visibility']:
                for obj in scene['objects'].values():
                    if type(obj) is list:
                        for o in obj:
                            o.update(events)
                    else:
                        obj.update(events)
                scene['controller'].update(events)

    def draw(self):
        black = 0, 0, 0
        self.screen.fill(black)
        for scene_name, scene in self.scenes.items():
            if scene['visibility']:
                for obj in scene['objects'].values():
                    if type(obj) is list:
                        for o in obj:
                            o.draw(self.screen)
                    else:
                        obj.draw(self.screen)
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
