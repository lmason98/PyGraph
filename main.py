"""
File: main.py
Author: Luke Mason

Description: Inits Window object with global screen definition variables.
"""
from message import log, error, success
from settings import APP_NAME, BLACK, WHITE
from pygame import sprite, event, mouse, display, init, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION, QUIT
from sprites.vertex import Vertex

import sys

init()  # pygame.init()

SCREEN_WIDTH: int = 1920
SCREEN_HEIGHT: int = 1080
WIDTH: int = 800
HEIGHT: int = 900

screen = display.set_mode((WIDTH, HEIGHT))

vertices = sprite.Group()  # pygame list for sprites


def add_vertex(x: int, y: int) -> bool:
    """
    Attempts to add a new vertex, returns True if successful, False if it is colliding with an existing vertex.
    """
    v = Vertex(x=x, y=y)

    collision = False
    for _v in vertices:
        if sprite.collide_rect(v, _v):
            error("Vertex placement collision detected!")
            collision = True

    if not collision:
        success('Adding vertex x=%s y=%s' % (x, y))
        vertices.add(v)

    return not collision


def poll_events() -> None:
    """
    Pygame event polling (Handles any sort of input)
    """
    x, y = mouse.get_pos()

    for e in event.get():
        if e.type == QUIT:
            error("PyGame quitting.")

            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            # Handles vertex move
            for v in vertices:
                if v.rect.collidepoint(x, y): v.drag = True

            add_vertex(x, y)

        elif e.type == MOUSEBUTTONUP:
            # If mousedown and vertex is being dragged, stop dragging (new vertex position)
            for v in vertices:
                if v.drag: v.drag = False

        elif e.type == MOUSEMOTION:
            for v in vertices:
                if v.drag:
                    v.set_pos(x, y)


def think() -> None:
    """
    Application think function, this function is called every tick
    """
    poll_events()

    screen.fill(BLACK)
    vertices.draw(screen)

    display.flip()


def main() -> None:
    """
    Application entrypoint
    """
    while 1:
        think()


if __name__ == '__main__':
    main()
