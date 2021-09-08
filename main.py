from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from message import log, success, error

SW, SH = 1920, 1080
X, Y, W, H = 100, 100, SW-200, SH-200


def main():
    """
    Application entrypoint
    """
    window()


def window():
    """
    Builds the main window
    """
    app = QApplication(sys.argv)  # pass some info to pyqt
    win = QMainWindow()  # Build window
    win.setGeometry(X, Y, W, H)
    win.setWindowTitle('PyGraph')

    win.show()  # Show window
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

