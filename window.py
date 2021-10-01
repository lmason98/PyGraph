"""
File: window.py
Author: Luke Mason

Description: The main window object of the app, it holds pyqt window api calls to open the window.
Also includes code to manage the various screens on the app (i.e., main, settings, graph save screens).
"""
from message import log, success, error
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys


class Window:
	"""
	Window class
	"""

	def __init__(self, w: int, h: int, sw: int, sh: int) -> None:
		"""
		Set window dimensions
		"""
		self.width = w
		self.height = h
		self.screen_width = sw
		self.screen_height = sh
		self.screens = []

	def add_screen(self, screen: {name: str, screen: Screen}) -> None:
		"""
		Adds a screen to the screen list

		A screen object holds information to draw the screen on the window object
		"""
		self.screens.append(screen)

	def center(self) -> (int, int):
		"""
		Center the window in in the given screen width and height
		"""
		return (self.screen_width / 2) - (self.width / 2), (self.screen_height / 2) - (self.height / 2)

	def display(self) -> None:
		"""
		Builds the window
		"""
		x, y = self.center()

		app = QApplication(sys.argv)  # pass argv to pyqt
		win = QMainWindow()  # init window
		win.setGeometry(x, y, self.width, self.height)  # center window
		win.setWindowTitle('PyGraph')

		log('Window initiating...')
		win.show()  # show window

		error('PyGraph exiting...')
		sys.exit(app.exec_())
