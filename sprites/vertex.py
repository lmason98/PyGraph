"""
File: sprites/vertex.py
Author: Luke Mason

Description: A graph vertex pygame sprite (TODO: Make these customizable)
"""
from settings import COLOR
from pygame.sprite import Sprite
from pygame import Surface, draw

class Vertex(Sprite):

	def __init__(self, x: int, y: int, color: (int, int, int) = COLOR.get('white'), radius: int = 10) -> None:
		"""
		Inits the vertex sprite
		"""
		Sprite.__init__(self)

		self.drag = False  # Drag state for the vertex (will be true when vertex is being moved)
		self.color = color
		self.radius = radius

		# TODO: Figure out how to draw a circle
		self.image = Surface((self.radius*2, self.radius*2))
		self.image.fill(self.color)
		draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)  # We want circular vertices

		# The position of the sprite, update position by inc/dec self.pos.x and self.pos.y
		self.rect = self.image.get_rect(center=(x, y))

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
