"""
File: main.py
Author: Luke Mason

Description: Inits Window object with global screen definition variables.
"""
from message import log, error, success
from settings import APP_NAME, BLACK

import sys, pygame
pygame.init()

SCREEN_WIDTH: int = 1920
SCREEN_HEIGHT: int = 1080
WIDTH: int = 800
HEIGHT: int = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))


def add_vertex(x: int, y: int) -> None:
    success('Adding vertex x=%s y=%s' % (x, y))


def poll_events() -> None:
    """
    Main event polling
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            error("PyGame quitting.")

            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()

            success("PyGame click! x=%s y=%s" % (x, y))


def think() -> None:
    """
    Application think function, this function is called every tick
    """
    poll_events()

    # log('Thinking!')
    screen.fill(BLACK)
    pygame.display.flip()


def main() -> None:
    """
    Application entrypoint
    """
    while 1:
        think()


if __name__ == '__main__':
    main()
