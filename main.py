"""
File: main.py
Author: Luke Mason

Description: Inits Window object with global screen definition variables.
"""

# Application imports
from message import log, error, success
from settings import APP_NAME, COLOR, FONT, FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, WIDTH, HEIGHT, PAD
from sprites.vertex import Vertex

# Pygame imports
from pygame import font, sprite, event, mouse, display, init, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION, QUIT,\
    KEYDOWN, K_BACKSPACE, K_DELETE

import sys

init()  # pygame.init()

screen = display.set_mode((WIDTH, HEIGHT))

vertices = sprite.Group()  # pygame list for sprites
edges = sprite.Group()
text = []

selected_vertex = None  # Track the selected vertex


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
        success(f'Adding vertex x={x} y={y}')
        vertices.add(v)

    return not collision


def render_stats(_font: font.SysFont):
    """
    Draws the app stats, i.e., total vertex and edge count
    """

    v_count = f'N={len(vertices)}'  # N
    e_count = f'M={len(edges)}'  # M

    v_count_rendered = _font.render(str(v_count), False, COLOR.get('white'), True)
    e_count_rendered = _font.render(str(e_count), False, COLOR.get('white'), True)

    return {'text': v_count_rendered, 'size': _font.size(str(v_count))},\
           {'text': e_count_rendered, 'size': _font.size(str(e_count))}


def poll_events() -> None:
    """
    Pygame event polling (Handles any sort of input)
    """
    global selected_vertex
    moving = False
    x, y = mouse.get_pos()

    for e in event.get():
        if e.type == QUIT:
            error("PyGame quitting.")

            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            # Handles vertex move
            for v in vertices:
                if v.rect.collidepoint(x, y):
                    moving = True
                    v.selected = v.drag = True
                    v.set_color(COLOR.get('selected'))
                    selected_vertex = v

            if not moving:
                add_vertex(x, y)  # Mousedown not moving, add vertex

            for v in vertices:
                if v is not selected_vertex:
                    v.selected = False
                    v.set_color(COLOR.get('white'))


        elif e.type == MOUSEBUTTONUP:
            # If mousedown and vertex is being dragged, stop dragging (new vertex position)
            for v in vertices:
                if v.drag: v.drag = False

        elif e.type == MOUSEMOTION:
            for v in vertices:
                if v.drag:
                    v.set_pos(x, y)

        elif e.type == KEYDOWN:

            if e.key == K_BACKSPACE or e.key == K_DELETE:
                x, y = selected_vertex.get_pos()
                n = len(vertices)
                vertices.remove(selected_vertex)

                if len(vertices) < n:
                    success(f'Removed vertex x={x} y={y}')


def think(_font: font.SysFont) -> None:
    """
    Application think function, this function is called every tick
    """
    poll_events()

    n, m = render_stats(_font)  # n, m are dicts, take a look at render_stats to see structure

    screen.fill(COLOR.get('black'))
    vertices.draw(screen)

    screen.blit(n.get('text'), (PAD, PAD))
    screen.blit(m.get('text'), (WIDTH - PAD - m.get('size')[0], PAD))  # Set to right side of screen

    display.flip()


def main() -> None:
    """
    Application entrypoint
    """
    font.init()
    sc_font = font.SysFont(FONT, FONT_SIZE)

    while 1:
        think(sc_font)


if __name__ == '__main__':
    main()
