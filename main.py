"""
File: main.py
Author: Luke Mason

Description: Inits Window object with global screen definition variables.
"""
from message import error
from settings import APP_NAME
from window import Window
from message import log
from PyQt5.QtWidgets import QApplication

import sys

SCREEN_WIDTH: int = 1920
SCREEN_HEIGHT: int = 1080
WIDTH: int = 800
HEIGHT: int = 900


def main() -> None:
    """
    Application entrypoint
    """
    app = QApplication(sys.argv)  # pass argv to pyqt
    win = Window(w=WIDTH, h=HEIGHT, sw=SCREEN_WIDTH, sh=SCREEN_HEIGHT)

    win.display()

    # I don't really understand this sys.exist app.exec_ line, but it came straight
    # from the pyqt docs so I trust it
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

