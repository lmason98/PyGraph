"""
File: main.py
Author: Luke Mason

Description: Inits Window object with global screen definition variables.
"""

# Application imports
from message import log, error, success
from settings import APP_NAME, COLOR, FONT, FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, WIDTH, HEIGHT, PAD, _QUIT
from sprites.vertex import Vertex
from pages.graph import GraphPage

# Pygame imports
from pygame import font, display, init, time

import sys

init()  # pygame.init()

screen = display.set_mode((WIDTH, HEIGHT))


def main() -> None:
    """
    Application entrypoint
    """
    font.init()
    sc_font = font.SysFont(FONT, FONT_SIZE)
    clock = time.Clock()
    tick = 0

    graph = GraphPage(screen=screen)

    while 1:
        q = graph.think(sc_font)

        tick += 1

        if q == _QUIT:
            error("PyGraph quitting.")
            sys.exit()


if __name__ == '__main__':
    main()
