"""
File: views/view.py
Author: Luke Mason
Description: Base view class to be inherited by other views
"""


class View:
	def __init__(self, bg: str, tc: str, title: str, w: int, h: int):
		"""
		To keep it simple, colors in this app are the css keywords
		"""
		self.background_color: str = bg
		self.text_color: str = tc
		self.title: str = title
		self.width: int = w
		self.height: int = h

	def display(self, win):
		"""
		Draws the actual screen
		"""
		win.setStyleSheet(f'background-color: {self.background_color}')
		win.setWindowTitle(self.title)
		win.setGeometry(0, 0, self.width, self.height)

		self.draw()

		win.show()

	def draw(self):
		"""
		This method is set when the view is actually created
		"""
		pass
