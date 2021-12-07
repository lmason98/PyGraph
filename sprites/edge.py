"""
File: sprites/edge.py
Author: Luke Mason

Description: A graph edge pygame sprite
"""
from settings import COLOR
from pygame.sprite import Sprite
from pygame import Surface, draw

TEXT = COLOR.get('white')


class Edge(Sprite):

	def __init__(self, v1, v2, color: (int, int, int) = TEXT):
		"""
		Inits the Edge sprite
		"""

		Sprite.__init__(self)

		self.color = color

		self.v1 = v1
		self.v2 = v2

		# Add the vertices to each other connected lists
		v1.add_connected_vertex(v2)
		v2.add_connected_vertex(v1)

	def __str__(self):
		"""
		Converts the edge class to string for print()
		"""
		x1, y1 = self.v1.get_pos()
		x2, y2 = self.v2.get_pos()

		return f'(x={x1}, y={y1}) -> (x={x2}, y={y2})'

	def __eq__(self, other):
		"""
		Have to overwrite this class == operator as it doesn't work by default
		"""
		return (self.v1.get_pos() == other.v1.get_pos() and self.v2.get_pos() == other.v2.get_pos()) or \
			   (self.v1.get_pos() == other.v2.get_pos() and self.v2.get_pos() == other.v1.get_pos())

	def set_color(self, color: (int, int, int)) -> None:
		"""
		Sets the vertex color
		"""
		self.color = color
