"""
File: views.py
Author: Luke Mason
Description: Not to be described with view.py, the base view class. This file defines the views of the
app, i.e., home view, saved graphs view, settings view and graph interact view.
"""
from settings import APP_NAME
from message import success
from view import View
from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtCore import Qt

BG = 'black'  # Background color
TC = 'white'  # Text color

def home(x: int, y: int, w: int, h: int, **kwargs):
	"""
	Creates the home-screen and returns it
	"""
	h = View(bg=BG,
			 tc=TC,
			 title=f'{APP_NAME} - {kwargs.get("title")}',  # No choice but to use " here :(
			 w=kwargs.get('width'),
			 h=kwargs.get('height'))

	# I know this is ugly and probably unpythonic but its the best way I could think of doing this
	# without repeating code
	def display_home(self=h):
		print('====== display home!')
		title = QLabel()

		title.setText("Hello World!")
		title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		title.setAlignment(Qt.AlignCenter)
		title.setStyleSheet('QLabel {background-color: red;}')

	h.draw = display_home

	success('Home screen initialized')
	return h
