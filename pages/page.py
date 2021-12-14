"""
File: pages/page.py
Author: Luke Mason

Description: Base page class for application pages
"""
from settings import COLOR
from pygame import mouse, draw

# Base button class
class Button:

	def __init__(self, x, y, text, onclick, w=100, h=35):

		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.text = text
		self.onclick = onclick

	def hovered(self, x, y):
		"""
		Returns if the button is currently hovered
		"""
		x_range = range(self.x, self.x + self.w)
		y_range = range(self.y, self.y + self.h)

		if x in x_range and y in y_range:
			hovered = True
		else:
			hovered = False

		return hovered

	def draw(self, x, y, screen):
		"""
		Draws the button as white outline, black background and white text. Inverts this if the button is
		pressed.
		"""
		if self.hovered(x, y):
			draw.rect(screen, COLOR.get('white'), (self.x, self.y, self.w, self.h))
		else:
			draw.rect(screen, COLOR.get('white'), (self.x, self.y, self.w, self.h), 4)



# Base page class
class Page:

	def __init__(self, screen):

		self.screen = screen  # Main pygame screen
		self.buttons = []

	def add_button(self, x, y, text, onclick):
		self.buttons.append(Button(x, y, text, onclick))

	def draw_buttons(self):
		"""
		Draw buttons on the screen
		"""
		x, y = mouse.get_pos()

		for b in self.buttons:
			b.draw(x, y, self.screen)
