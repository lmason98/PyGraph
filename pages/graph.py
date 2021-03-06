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

# Python imports
from math import atan2, degrees, cos, sin


class GraphPage(Page):

	def __init__(self, screen):
		Page.__init__(self, screen)

		self.second_click = False
		self.moving = False
		self.collision = False
		self.selected_vertices = []
		self.selected_edges = []
		self.vertices = sprite.Group()
		self.edges = []  # Edges arent sprites in the same way that vertices are
		self.last_clicked_vertex = None
		self.show_labels = False

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

		v1.edges.append(e)
		v2.edges.append(e)

		success(f'Add edge {e}')

	def edge_count(self):
		"""
		Since self.edges is a list of dicts defining parallel edges, simply
		len(self.edges) is misleading.
		"""
		total_count = 0

		for edge in self.edges: total_count += edge.get('count')

		return total_count

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
			self.vertices.remove(sv)

			# Remove any edges connected to this removed vertex
			for e in self.edges:
				if e.get('edge') in sv.edges:
					self.edges.remove(e)
					
		self.last_clicked_vertex = None

	def delete_edges(self):
		for se in self.selected_edges:
			for e in self.edges:
				if e.get('edge') == se:
					log('deleteing se:', se)
					self.edges.remove(e)

	def stats(self, font):
		"""
		Draws the graph stats stats, i.e., total vertex and edge count
		"""

		v_count = f'N={len(self.vertices)}'  # N
		e_count = f'M={self.edge_count()}'  # M

		v_count_rendered = font.render(str(v_count), False, COLOR.get('white'), True)
		e_count_rendered = font.render(str(e_count), False, COLOR.get('white'), True)

		return {'text': v_count_rendered, 'size': font.size(str(v_count))}, \
			   {'text': e_count_rendered, 'size': font.size(str(e_count))}

	def handle_click(self, x, y):
		"""
		Handles the logic when mouse is clicked, this logic is quite complex as it includes,
		- placing a vertex (single click anywhere on app window where there does not already exist a vertex)
		- moving a vertex (click and drag a vertex)
		- adding an edge between two vertices (single click two vertices in a row)
		"""
		self.collision = False

		button_clicked = False
		edge_clicked = False
		for b in self.buttons:
			if b.hovered(x, y):
				log(f'button clicked={b}')
				b.onclick()
				button_clicked = True

		if not button_clicked:
			for e in self.edges:
				edge = e.get('edge')
				if edge.hovered(x, y):
					edge_clicked = True

		if not button_clicked and not edge_clicked:
			for v in self.vertices:
				if v.rect.collidepoint(x, y):
					self.collision = True

					log('====== vertex click:', v)

					# Handles vertex move (self.moving and v.drag flipped on MOUSEBUTTONUP)
					self.moving = True
					v.drag = True

					# Click to select
					v.selected = True
					v.set_color(COLOR.get('focus'))
					self.selected_vertices.clear()
					self.selected_edges.clear()
					self.selected_vertices.append(v)

					# If last clicked vertex
					if self.last_clicked_vertex and v and self.last_clicked_vertex != v:
						self.add_edge(self.last_clicked_vertex, v)
						self.last_clicked_vertex = None
						log('clear last clicked 1')
					elif self.last_clicked_vertex and v and self.last_clicked_vertex == v:
						log('ADD LOOP!')
					else:
						self.last_clicked_vertex = v
						log('set last clicked')

			# If selected vertex and not a collision, clear selected vertex
			if not self.collision and len(self.selected_vertices) > 0:
				self.selected_vertices.clear()
			# If selected edge and not a collision, clear selected edge
			elif not self.collision and len(self.selected_edges) > 0:
				self.selected_edges.clear()
			# Otherwise add new vertex
			elif not self.collision:
				self.add_vertex(x, y)  # Mousedown not moving, add vertex
				self.last_clicked_vertex = None

	def poll_events(self):
		"""
		Graph page event polling (Handles any sort of input)

		- Single click anywhere on screen to add a new vertex
		- Delete or backspace to delete selected vertex
		"""
		x, y = mouse.get_pos()

		for e in event.get():

			if e.type == QUIT:
				return _QUIT

			# Mouse down
			elif e.type == MOUSEBUTTONDOWN:

				self.handle_click(x, y)

			# Mouse up
			elif e.type == MOUSEBUTTONUP:
				# If mouse release and vertex is being dragged, stop dragging (placing a moved vertex)
				dragging = False
				for v in self.vertices:
					if v.drag:
						dragging = True
						v.drag = False
						self.moving = False

					if v.rect.collidepoint(x, y) and self.last_clicked_vertex and v and self.last_clicked_vertex != v:
						self.add_edge(self.last_clicked_vertex, v)


				# Handling edge placement on mouse button up, so we do not place an edge when draggin a vertex
				if not dragging:
					for e in self.edges:
						edge = e.get('edge')
						if edge.hovered(x, y):
							self.selected_edges.clear()
							self.selected_vertices.clear()
							self.selected_edges.append(edge)

			# Mouse moving
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

				for _e in self.edges:
					edge = _e.get('edge')
					if edge.hovered(x, y):
						edge.set_color(COLOR.get('focus'))
					elif edge not in self.selected_edges:
						edge.set_color(COLOR.get('white'))


			elif e.type == KEYDOWN:

				# (Delete or backspace key) Delete selected vertices
				if e.key == K_BACKSPACE or e.key == K_DELETE:
					self.delete_vertices()
					self.delete_edges()
					self.moving = False

	def draw_edges(self):
		"""
		Draw the edges (have to do this manually as pygame sprite did not quite fit for this use case)
		"""
		mult = 6  # distance between edges

		for e in self.edges:
			total_count = e.get('count')
			for c in range(0, e.get('count')):
				edge = e.get('edge')
				p1, p2 = edge.v1.get_pos(), edge.v2.get_pos()

				ang = degrees(atan2(p2[1] - p1[1], p2[0] - p1[0]))

				# Logic to place parallel edges in clear visible manner despite angle between
				# the vertices. (This angle will change as user moves vertices around)
				x_mult, y_mult = self.handle_point_angle_eq(ang, mult)

				p1 = (p1[0] + edge.v1.radius + x_mult*c, p1[1] + edge.v1.radius + y_mult*c)
				p2 = (p2[0] + edge.v2.radius + x_mult*c, p2[1] + edge.v2.radius + y_mult*c)

				draw.line(self.screen, edge.color, p1, p2)

	def handle_point_angle_eq(self, ang, dist) -> (int, int):
		"""
		Handles the angle point code to keep draw_edges function clean

		It returns x, y multiple for distance between parallel edges based on the
		angle between the vertices so that parallel edges can always be displayed
		as parallel.
		"""

		# Handles sign of ranges we check to reduce repeated code
		sign = 1
		if ang < 0:
			sign = -1

		# This algorithm is likely really ugly... I know there exists a more elegant way
		# to do this.
		if 45 <= ang <= 135 or -135 <= ang <= -45:
			return dist, 0
		elif -45 <= ang <= 45 or ang >= 135 or ang <= -135:
			return 0, dist
		else:
			print('======== other ang?')
			return dist, dist

	def toggle_labels(self):
		print('======== toggling labels')
		self.show_labels = not self.show_labels

	def draw_vertices(self, font):
		"""
		Draws the vertices and handles vertex labels
		"""
		self.vertices.draw(self.screen)  # Draw vertices

		if self.show_labels:
			i = 1
			for v in self.vertices:
				x, y = v.get_pos()

				text = font.render(str(i), False, COLOR.get('white'), True)
				self.screen.blit(text, (x + PAD*1.5, y - PAD*1.5))

				i += 1

	def think(self, font):
		"""
		Graph page think function, this function is called every tick
		"""
		q = self.poll_events()

		n, m = self.stats(font)  # n, m are dicts, take a look at render_stats to see structure

		self.screen.fill(COLOR.get('black'))  # Background color
		self.draw_vertices(font)
		self.draw_edges()  # Draw edges
		self.draw_buttons(font)  # Draw buttons (inherited from Page class)

		self.screen.blit(n.get('text'), (PAD, PAD))  # Draw N=vertex count and M=edge count
		self.screen.blit(m.get('text'), (WIDTH - PAD - m.get('size')[0], PAD))  # Set to right side of screen

		display.flip()  # Weird pygame call required to display window

		if q == _QUIT:
			return q
