from manim import *
import numpy as np

class CombinedCircleSceneWithFade(Scene):
	"""
	A Manim scene that constructs the circumcircle, incircle, centroid, and
	orthocenter of a triangle, and finally draws the Euler Line.
	"""
	def get_line_intersection(self, line1_start, line1_end, line2_start, line2_end):
		"""
		Calculates the intersection point of two lines in 2D space.
		Returns the intersection point or None if the lines are parallel.
		"""
		p1, p2 = line1_start, line1_end
		p3, p4 = line2_start, line2_end
		v1 = p2 - p1
		v2 = p4 - p3
		
		A = np.array([
			[v1[0], -v2[0]],
			[v1[1], -v2[1]]
		])
		b = (p3 - p1)[:2]
		
		try:
			# Solve for the intersection parameter t
			t = np.linalg.solve(A, b)[0]
			# Return the intersection point
			return p1 + t * v1
		except np.linalg.LinAlgError:
			# Lines are parallel
			return None

	def construct(self):
		# 1. Define the triangle and get its vertices
		triangle = Polygon((-3, -2, 0), (4, -1, 0), (1, 3, 0), color=BLUE)
		vertices = triangle.get_vertices()
		v1, v2, v3 = vertices[0], vertices[1], vertices[2]

		self.play(Create(triangle))
		self.wait(1)

		# --- Initialize point variables ---
		circumcenter_point, incenter_point, centroid_point, orthocenter_point = None, None, None, None

		# --- Part 1: Circumcenter and Circumcircle ---
		m1, m2, m3 = (v1 + v2) / 2, (v2 + v3) / 2, (v3 + v1) / 2
		midpoints = VGroup(Dot(m1), Dot(m2), Dot(m3)).set_color(YELLOW)
		self.play(Create(midpoints))
		self.wait(1)
		
		perp_line1 = Line(m1, m1 + rotate_vector(v2 - v1, PI / 2), color=RED).scale(3)
		perp_line2 = Line(m2, m2 + rotate_vector(v3 - v2, PI / 2), color=RED).scale(3)
		perp_line3 = Line(m3, m3 + rotate_vector(v1 - v3, PI / 2), color=RED).scale(3)
		perp_lines = VGroup(perp_line1, perp_line2, perp_line3)

		self.play(Create(perp_lines))
		self.wait(1)
		circumcenter_point = self.get_line_intersection(
			perp_line1.get_start(), perp_line1.get_end(),
			perp_line2.get_start(), perp_line2.get_end()
		)
		if circumcenter_point is not None:
			circumcenter_dot = Dot(circumcenter_point, color=ORANGE, radius=0.1)
			self.play(FadeIn(circumcenter_dot, scale=0.5))
			self.wait(1)
			radius = float(np.linalg.norm(circumcenter_point - v1))
			circumcircle = Circle(radius=radius, arc_center=circumcenter_point, color=ORANGE)
			self.play(Create(circumcircle))
			self.wait(2)
			self.play(FadeOut(perp_lines), FadeOut(midpoints), FadeOut(circumcircle))
			self.wait(1)

		# --- Part 2: Incenter and Incircle ---
		bisector1 = Line(v1, v1 + normalize(normalize(v2 - v1) + normalize(v3 - v1)) * 15, color=GREEN)
		bisector2 = Line(v2, v2 + normalize(normalize(v1 - v2) + normalize(v3 - v2)) * 15, color=GREEN)
		bisector3 = Line(v3, v3 + normalize(normalize(v1 - v3) + normalize(v2 - v3)) * 15, color=GREEN)
		angle_bisectors = VGroup(bisector1, bisector2, bisector3)
		
		self.play(Create(angle_bisectors), run_time=2)
		self.wait(1)
		incenter_point = self.get_line_intersection(
			bisector1.get_start(), bisector1.get_end(),
			bisector2.get_start(), bisector2.get_end()
		)
		if incenter_point is not None:
			incenter_dot = Dot(incenter_point, color=PURPLE, radius=0.1)
			self.play(FadeIn(incenter_dot, scale=0.5))
			self.wait(1)
			side_vec = v2 - v1
			incenter_to_vertex_vec = incenter_point - v1
			radius = float(np.linalg.norm(np.cross(side_vec, incenter_to_vertex_vec)) / np.linalg.norm(side_vec))
			incircle = Circle(radius=radius, arc_center=incenter_point, color=PURPLE)
			self.play(Create(incircle))
			self.wait(2)
			self.play(FadeOut(angle_bisectors), FadeOut(incircle))
			self.wait(1)
			
		# --- Part 3: Centroid and Medians ---
		m1, m2, m3 = (v1 + v2) / 2, (v2 + v3) / 2, (v3 + v1) / 2
		median1 = Line(v1, m2, color=TEAL)
		median2 = Line(v2, m3, color=TEAL)
		median3 = Line(v3, m1, color=TEAL)
		medians = VGroup(median1, median2, median3)

		self.play(Create(medians), run_time=2)
		self.wait(1)
		centroid_point = self.get_line_intersection(
			median1.get_start(), median1.get_end(),
			median2.get_start(), median2.get_end()
		)
		if centroid_point is not None:
			centroid_dot = Dot(centroid_point, color=PINK, radius=0.1)
			self.play(FadeIn(centroid_dot, scale=0.5))
			self.wait(1)
			self.play(FadeOut(medians))
			self.wait(1)

		# --- Part 4: Orthocenter and Altitudes ---
		altitude1 = Line(v1, v1 + rotate_vector(v3 - v2, PI / 2), color=GOLD).scale(5)
		altitude2 = Line(v2, v2 + rotate_vector(v1 - v3, PI / 2), color=GOLD).scale(5)
		altitude3 = Line(v3, v3 + rotate_vector(v2 - v1, PI / 2), color=GOLD).scale(5)
		altitudes = VGroup(altitude1, altitude2, altitude3)

		self.play(Create(altitudes), run_time=2)
		self.wait(1)
		orthocenter_point = self.get_line_intersection(
			altitude1.get_start(), altitude1.get_end(),
			altitude2.get_start(), altitude2.get_end()
		)
		if orthocenter_point is not None:
			orthocenter_dot = Dot(orthocenter_point, color=RED, radius=0.1)
			self.play(FadeIn(orthocenter_dot, scale=0.5))
			self.wait(1)
			self.play(FadeOut(altitudes))
			self.wait(1)
		
		# --- Part 5: The Euler Line ---
		
		# First, check that all three required points exist
		assert circumcenter_point is not None
		assert orthocenter_point is not None
		assert centroid_point is not None




		# Create the line that passes through the points
		euler_line = Line(
			circumcenter_point, 
			orthocenter_point, 
			color=WHITE, 
			stroke_width=6
		).scale(10) # Scale it to extend past the points
		
		# Create a label for the line
		self.play(
			Create(euler_line),
			run_time=2
		)
		self.wait(5)