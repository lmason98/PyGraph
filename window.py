"""
File: window.py
Author: Luke Mason
Deviewiption: The main window object of the app, it holds pyqt window api calls to open the window.
Also includes code to manage the various views on the app (i.e., main, settings, graph save views).
"""
from settings import APP_NAME
from message import log, success, error
from view import View
from views import home

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSizePolicy, QGridLayout
from PyQt5.QtCore import Qt

import sys


class Window(QMainWindow):

	def __init__(self: QMainWindow, w: int, h: int, sw: int, sh: int) -> None:
		"""
		Set window dimensions
		"""
		super().__init__()
		self.title = ""
		self.width = w
		self.height = h
		self.view_width = sw
		self.view_height = sh
		self.views = []
		self.current_view = None  # Left None here, set in set_view method

	def center(self: QMainWindow) -> (int, int):
		"""
		Center the window in the given view width and height
		"""
		return (self.view_width / 2) - (self.width / 2), (self.view_height / 2) - (self.height / 2)

	def add_view(self: QMainWindow, view: dict) -> None:
		"""
		Adds a view to the view list

		A view object holds information to draw the view on the window object

		view: {name: str, view: View}
		"""
		self.views.append(view)

	def set_view(self: QMainWindow, view: View) -> None:
		log(f'Set view to {view.title}')
		self.current_view = view

	def get_view(self, view_name: str) -> View:
		"""
		Gets a view with a given name (title)
		"""
		view: Optional[View] = None

		for v in self.views:
			print(f'title={v.get("name")} name={view_name}')
			if v.get('name') == view_name: view = v

		if view is not None:
			return view
		else:
			error(f'Could not find view with name {view_name}')

	def show_view(self, view_name: str) -> None:
		"""
		Shows the view with a given name, view names correspond to the views files without the .py extension
		(besides View of course, this is not an actual view)
		"""
		view: View = self.get_view(view_name)

		if view: view.get('view').display(self)  # Passing self here which is a QMainWindow that view.display draws on

	def load_views(self, x: int, y: int) -> None:
		"""
		Loads the different app views
		"""
		kwargs: dict = {'width': self.width, 'height': self.height}

		views: [dict] = [
			{'name': 'home', 'view': home(x, y, self.width, self.height, **kwargs)},
		]

		log('Loading views...')
		for view in views:
			self.add_view(view)

	def load(self, x: int, y: int) -> None:
		log(f'{APP_NAME} initiating...')
		# These are inherited QMainWindow methods
		self.setGeometry(x, y, self.width, self.height)  # center window

		title = QLabel()

		title.setText("Hello World!")
		title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		title.setAlignment(Qt.AlignCenter)
		title.setStyleSheet('QLabel {background-color: red;}')

		self.layout = QGridLayout()
		self.layout.addWidget(title, 0, 0)

		self.setLayout(self.layout)

		self.load_views(x, y)

	def display(self: QMainWindow) -> None:
		"""
		Builds the window
		"""
		log('Centering window...')
		x, y = self.center()

		self.load(x, y)  # Load the app, set the geometry and title

		log('Showing home view...')
		self.show_view('home')  # show window (.show() being a QMainWindow method)
