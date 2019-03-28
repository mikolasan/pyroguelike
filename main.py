#!/usr/bin/env python


from pygamerogue.engine import Engine
from myrogue.game import TestGame
from myrogue.main_controller import MainController


def main():
    size = (800, 600)
    engine = Engine(size)
    engine.load(TestGame())
    controller = MainController(engine)
    engine.run(controller)


# if python says run, then we should run
if __name__ == '__main__':
    main()
