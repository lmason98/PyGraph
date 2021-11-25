"""
File: main.py
Author: Luke Mason

Description: Inits Window object with global screen definition variables.
"""
from message import log
from settings import APP_NAME, BLACK

import sys, pygame
pygame.init()

SCREEN_WIDTH: int = 1920
SCREEN_HEIGHT: int = 1080
WIDTH: int = 800
HEIGHT: int = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))


def poll_events() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()


def think() -> None:
    """
    Application think function, this function is called every tick
    """
    poll_events()

    log('Thinking!')
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

