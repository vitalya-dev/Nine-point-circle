from manim import *

class CircumcenterScene(Scene):
	def get_line_intersection(self, line1_start, line1_end, line2_start, line2_end):
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
			t = np.linalg.solve(A, b)[0]
			return p1 + t * v1
		except np.linalg.LinAlgError:
			return None

	def construct(self):
		# 1. Define the triangle and get its vertices
		triangle = Polygon((-3, -2, 0), (4, -1, 0), (1, 3, 0), color=BLUE)
		vertices = triangle.get_vertices()
		v1, v2, v3 = vertices[0], vertices[1], vertices[2]

		self.play(Create(triangle))
		self.wait(0.5)

		# 2. Get all three midpoints and mark them
		m1 = (v1 + v2) / 2
		m2 = (v2 + v3) / 2
		m3 = (v3 + v1) / 2
		midpoints = VGroup(
			Dot(m1, color=YELLOW),
			Dot(m2, color=YELLOW),
			Dot(m3, color=YELLOW)
		)
		
		self.play(Create(midpoints))
		self.wait(0.5)

		# 3. Create all three perpendicular bisectors
		side1_vec = v2 - v1
		perp1_vec = rotate_vector(side1_vec, PI / 2)
		perp_line1 = Line(m1 - perp1_vec * 2, m1 + perp1_vec * 2, color=RED)

		side2_vec = v3 - v2
		perp2_vec = rotate_vector(side2_vec, PI / 2)
		perp_line2 = Line(m2 - perp2_vec * 2, m2 + perp2_vec * 2, color=RED)

		side3_vec = v1 - v3
		perp3_vec = rotate_vector(side3_vec, PI / 2)
		perp_line3 = Line(m3 - perp3_vec * 2, m3 + perp3_vec * 2, color=RED)

		self.play(
			Create(perp_line1),
			Create(perp_line2),
			Create(perp_line3)
		)
		self.wait(0.5)

		# 4. Calculate the circumcenter
		circumcenter_point = self.get_line_intersection(
			perp_line1.get_start(), perp_line1.get_end(),
			perp_line2.get_start(), perp_line2.get_end()
		)
		
		# 5. Check if an intersection was found before drawing
		if circumcenter_point is not None:
			# All code that uses the center point now goes inside this block
			circumcenter_dot = Dot(circumcenter_point, color=ORANGE, radius=0.1)
			
			self.play(FadeIn(circumcenter_dot, scale=0.5))
			self.wait(0.5)

			radius = float(np.linalg.norm(circumcenter_point - v1))
			circumcircle = Circle(radius=radius, arc_center=circumcenter_point, color=ORANGE)

			self.play(Create(circumcircle))
			self.wait(2)
		else:
			# Optional: Show a message if no center is found
			self.play(Text("Lines are parallel, no circumcenter.").scale(0.5))
			self.wait(2)