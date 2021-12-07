"""
File: sprites/vertex.py
Author: Luke Mason

Description: A graph vertex pygame sprite
"""
from settings import COLOR
from pygame.sprite import Sprite
from pygame import Surface, draw

TEXT = COLOR.get('white')


class Vertex(Sprite):

	def __init__(self, x: int, y: int, color: (int, int, int) = TEXT, radius: int = 10) -> None:
		"""
		Inits the vertex sprite
		"""
		Sprite.__init__(self)

		self.drag = False  # Drag state for the vertex (will be true when vertex is being moved)
		self.selected = False
		self.color = color
		self.radius = radius

		self.connected_vertices = []

		# TODO: Figure out how to draw a circle
		self.image = Surface((self.radius*2, self.radius*2))
		self.image.fill(self.color)
		draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)  # We want circular vertices

		# The position of the sprite, update position by inc/dec self.pos.x and self.pos.y
		self.rect = self.image.get_rect(center=(x, y))

	def __str__(self):
		"""
		Converts the vertex class to string for print()
		"""
		x, y = self.get_pos()

		return f'(x={x}, y={y})'

	def set_pos(self, x: int, y: int) -> None:
		"""
		Sets the position of the vertex, this should only be called when placing or moving a vertex
		"""
		self.rect.x = x - (self.radius / 2)
		self.rect.y = y - (self.radius / 2)

	def get_pos(self) -> (int, int):
		"""
		Returns vertex position
		"""
		return self.rect.x, self.rect.y

	def set_color(self, color: (int, int, int)) -> None:
		"""
		Sets the vertex color
		"""
		self.color = color
		self.image.fill(self.color)

	def add_connected_vertex(self, v) -> None:
		"""
		Adds a vertex to the connected vertices list, this is used for tracking edges.

		self.connected_vertices = [{'vertex': v0, 'count': 1}, {'vertex: v1, 'count': 3}]
		For any count > 0, there will be parallel edges
		"""

		found = False
		for cv in self.connected_vertices:

			# If vertex exists, update count
			if cv.get('vertex') == v:
				cv.update({'count': cv.get('count', 0) + 1})
				found = True

		# Otherwise insert with count=1
		if not found:
			self.connected_vertices.append({'vertex': v, 'count': 1})

	def remove_connected_vertex(self, v) -> None:
		"""
		Removes a vertex from the connected vertices list, this is used for tracking edges.

		Returns True/False based on if the passed vertex actually existed in the list
		"""
		found = False
		for cv in self.connected_vertices:

			if cv.get('vertex') == v:
				self.connected_vertices.remove(cv)
				found = True
				break

		return found
