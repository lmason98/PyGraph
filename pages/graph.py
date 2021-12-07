"""
File: pages/page.py
Author: Luke Mason

Description: Main part of the application, the actual graph page.
"""
# Application imports
from message import log, error, success
from settings import APP_NAME, COLOR, FONT, FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, WIDTH, HEIGHT, PAD, _QUIT
from sprites.vertex import Vertex
from sprites.edge import Edge
from pages.page import Page
from graph import Graph as G

# Pygame imports
from pygame import draw, sprite, event, mouse, display, init, key, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION, QUIT, \
	KEYDOWN, K_BACKSPACE, K_DELETE, KMOD_SHIFT


class GraphPage(Page):

	def __init__(self, screen):
		Page.__init__(self)

		self.screen = screen  # Main pygame screen

		self.second_click = False
		self.moving = False
		self.collision = False
		self.selected_vertices = []
		self.vertices = sprite.Group()
		self.edges = []  # Edges arent sprites in the same way that vertices are
		self.last_clicked_vertex = None

		self.graph = G()  # Actual graph logic

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
			success(f'Adding vertex {new_v}')
			self.vertices.add(new_v)

		return not self.collision

	def add_edge(self, v1: Vertex, v2: Vertex) -> None:
		"""
		Adds an edge between vertices v1 and v2

		Here edges in the list are a dict={'edge': edge, 'count': n}
		"""

		e = Edge(v1, v2)

		found = False
		# Try to find in list and update count
		for _e in self.edges:
			if _e.get('edge') == e:  # We can do this with the __eq__ definition on the Edge class
				_e.update({'count': int(_e.get('count'))+1})
				# log(f'{_e} update count={_e.get("count")}')
				found = True
				break

		# Otherwise insert with count=1
		if not found:
			self.edges.append({'edge': e, 'count': 1})
			# log(f'{e} insert count=1')

		success(f'Add edge {e}')

	def remove_edge(self, edge) -> bool:
		"""
		Removes an edge from the edge list
		"""
		found = False
		for e in self.edges:
			if e.get('edge') == edge:
				self.edges.remove(e)
				found = True
				break

		return found

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

	def handle_vertex_click(self, x: int, y: int):
		"""
		Handles the logic when a vertex is clicked, this logic is quite complex as it includes,
		- placing a vertex (single click anywhere on app window where there does not already exist a vertex)
		- moving a vertex (click and drag a vertex)
		- adding an edge between two vertices (single click two vertices in a row)
		"""

		for v in self.vertices:
			if v.rect.collidepoint(x, y):

				log('====== vertex click:', v)

				# Handles vertex move (self.moving and v.drag flipped on MOUSEBUTTONUP)
				self.moving = True
				v.drag = True

				# Click to select
				v.selected = True
				v.set_color(COLOR.get('focus'))
				self.selected_vertices.clear()
				self.selected_vertices.append(v)

				# If last clicked vertex
				if self.last_clicked_vertex and v and self.last_clicked_vertex != v:
					self.add_edge(self.last_clicked_vertex, v)
					self.last_clicked_vertex = None
					log('clear last clicked 1')
				else:
					self.last_clicked_vertex = v
					log('set last clicked')

		if not self.moving:
			self.add_vertex(x, y)  # Mousedown not moving, add vertex
			self.last_clicked_vertex = None
			log('clear last clicked 3')

	def poll_events(self):
		"""
		Graph page event polling (Handles any sort of input)

		- Single click anywhere on screen to add a new vertex
		- Delete or backspace to delete selected vertex
		"""
		x, y = mouse.get_pos()
		# double_click = False

		for e in event.get():

			if e.type == QUIT:
				return _QUIT

			elif e.type == MOUSEBUTTONDOWN:

				self.handle_vertex_click(x, y)

			elif e.type == MOUSEBUTTONUP:
				# If mouse release and vertex is being dragged, stop dragging (placing a moved vertex)
				for v in self.vertices:
					if v.drag:
						v.drag = False

			elif e.type == MOUSEMOTION:

				for v in self.vertices:

					# Handles vertex drag as it is being dragged
					if v.drag:
						v.set_pos(x, y)

					# Focus if mouseover
					if v.rect.collidepoint(x, y):
						v.set_color(COLOR.get('focus'))
					elif v not in self.selected_vertices:
						v.set_color(COLOR.get('white'))

			elif e.type == KEYDOWN:

				# Delete selected vertices
				if e.key == K_BACKSPACE or e.key == K_DELETE:
					self.delete_vertices()
					self.moving = False

	def draw_edges(self) -> None:
		"""
		Draw the edges (have to do this manually as pygame sprite did not quite fit for this use case)
		"""
		for e in self.edges:
			total_count = e.get('count')
			for c in range(0, e.get('count')):
				edge = e.get('edge')
				p1, p2 = edge.v1.get_pos(), edge.v2.get_pos()

				p1 = (p1[0] + edge.v1.radius + 2*c, p1[1] + edge.v1.radius + 2*c)
				p2 = (p2[0] + edge.v2.radius + 2*c, p2[1] + edge.v2.radius + 2*c)

				draw.line(self.screen, edge.color, p1, p2)

	def think(self, font):
		"""
		Graph page think function, this function is called every tick
		"""
		q = self.poll_events()

		n, m = self.stats(font)  # n, m are dicts, take a look at render_stats to see structure

		self.screen.fill(COLOR.get('black'))  # Background color
		self.vertices.draw(self.screen)  # Draw vertices
		self.draw_edges()  # Draw edges

		self.screen.blit(n.get('text'), (PAD, PAD))  # Draw N=vertex count and M=edge count
		self.screen.blit(m.get('text'), (WIDTH - PAD - m.get('size')[0], PAD))  # Set to right side of screen

		display.flip()  # Weird pygame call required to display window

		if q == _QUIT:
			return q
