"""
File: main.py
Author: Luke Mason

Description: Inits Window object with global screen definition variables.
"""
from window import Window

SCREEN_WIDTH: int = 1920
SCREEN_HEIGHT: int = 1080
WIDTH: int = 800
HEIGHT: int = 900


def main() -> None:
    """
	Application entrypoint
	"""
    win = Window(w=WIDTH, h=HEIGHT, sw=SCREEN_WIDTH, sh=SCREEN_HEIGHT)

    win.display()


if __name__ == '__main__':
    main()

