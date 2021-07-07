#!/usr/bin/env python

from pygamerogue.engine import Engine
from myrogue.medieval_controller import MedievalController
from myrogue.game_controller import GameController
from myrogue.exit_controller import ExitController


def main():
    size = (800, 600)
    engine = Engine(size)
    engine.add(MedievalController())
    # engine.add(GameController())
    engine.add(ExitController())
    engine.run()


# if python says run, then we should run
if __name__ == '__main__':
    main()
