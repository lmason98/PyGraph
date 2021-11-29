"""
File: pages/page.py
Author: Luke Mason

Description: Main part of the application, the actual graph page.
"""
# Application imports
from message import log, error, success
from settings import APP_NAME, COLOR, FONT, FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, WIDTH, HEIGHT, PAD, _QUIT
from sprites.vertex import Vertex
from pages.page import Page

# Pygame imports
from pygame import sprite, event, mouse, display, init, key, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION, QUIT, \
	KEYDOWN, K_BACKSPACE, K_DELETE, KMOD_SHIFT


class Graph(Page):

	def __init__(self, screen):
		Page.__init__(self)

		self.screen = screen  # Main pygame screen

		self.second_click = False
		self.moving = False
		self.collision = False
		self.selected_vertices = []
		self.vertices = sprite.Group()
		self.edges = sprite.Group()
		self.last_clicked_vertex = None

	def add_vertex(self, x: int, y: int):
		"""
		Attempts to add a new vertex, returns True if successful, False if it is colliding with an existing vertex.
		"""
		new_v = Vertex(x=x, y=y)

		self.collision = False
		for v in self.vertices:
			if sprite.collide_rect(new_v, v):
				error("Vertex placement collision detected!")
				self.collision = True

		if not self.collision:
			success(f'Adding vertex x={x} y={y}')
			self.vertices.add(new_v)

		return not self.collision

	def add_edge(self):
		pass

	def delete_vertices(self):
		for sv in self.selected_vertices:
			log('deleting sv :', sv)
			x, y = sv.get_pos()
			n = len(self.vertices)
			self.vertices.remove(sv)

			if len(self.vertices) < n:
				success(f'Removed vertex x={x} y={y}')

	def stats(self, font):
		"""
		Draws the graph stats stats, i.e., total vertex and edge count
		"""

		v_count = f'N={len(self.vertices)}'  # N
		e_count = f'M={len(self.edges)}'  # M

		v_count_rendered = font.render(str(v_count), False, COLOR.get('white'), True)
		e_count_rendered = font.render(str(e_count), False, COLOR.get('white'), True)

		return {'text': v_count_rendered, 'size': font.size(str(v_count))}, \
			   {'text': e_count_rendered, 'size': font.size(str(e_count))}

	def poll_events(self):
		"""
		Graph page event polling (Handles any sort of input)

		- Double click vertices to select (can select more than one)
		- Single click anywhere on screen to add a new vertex
		- Delete or backspace to delete selected vertices
		"""
		x, y = mouse.get_pos()
		double_click = False

		for e in event.get():

			if e.type == QUIT:
				return _QUIT

			elif e.type == MOUSEBUTTONDOWN:

				# Handles vertex move
				for v in self.vertices:
					if v.rect.collidepoint(x, y):
						self.moving = True
						v.drag = True

						# Shift click select
						if key.get_mods() & KMOD_SHIFT:
							v.selected = True
							v.set_color(COLOR.get('selected'))
							self.selected_vertices.append(v)

						# If last clicked vertex
						if self.last_clicked_vertex:
							log('ADD EDGE')

						log('set last clicked')
						self.last_clicked_vertex = v

				if not self.moving:
					self.add_vertex(x, y)  # Mousedown not moving, add vertex
					self.last_clicked_vertex = None
					log('clear last clicked')

			elif e.type == MOUSEBUTTONUP:
				# If mousedown and vertex is being dragged, stop dragging (new vertex position)
				for v in self.vertices:
					if v.drag: v.drag = False

			elif e.type == MOUSEMOTION:
				for v in self.vertices:
					if v.drag:
						v.set_pos(x, y)

			elif e.type == KEYDOWN:

				if e.key == K_BACKSPACE or e.key == K_DELETE:
					self.delete_vertices()
					self.moving = False

	def think(self, font):
		"""
		Graph page think function, this function is called every tick
		"""
		q = self.poll_events()

		n, m = self.stats(font)  # n, m are dicts, take a look at render_stats to see structure

		self.screen.fill(COLOR.get('black'))
		self.vertices.draw(self.screen)

		self.screen.blit(n.get('text'), (PAD, PAD))
		self.screen.blit(m.get('text'), (WIDTH - PAD - m.get('size')[0], PAD))  # Set to right side of screen

		display.flip()

		if q == _QUIT:
			return q
