#!/usr/bin/env python

from pygamerogue.engine import Engine
from myrogue.game_controller import GameController
from myrogue.main_controller import MainController


def main():
    size = (800, 600)
    engine = Engine(size)
    engine.add(GameController())
    engine.add(MainController())
    engine.run()


# if python says run, then we should run
if __name__ == '__main__':
    main()
