// Define three variables to hold the vector positions of the triangle's corners.
let vertex1, vertex2, vertex3;

// --- New variables for animation ---
// 'phase' tracks which part of the animation we're in.
// 0 = drawing line 1, 1 = drawing line 2, 2 = drawing line 3, 3 = finished
let phase = 0;

// 'progress' tracks the completion of the current line being drawn (from 0.0 to 1.0).
let progress = 0;

// 'animationSpeed' controls how fast the lines are drawn.
const animationSpeed = 0.02; // You can make this faster (e.g., 0.05) or slower (e.g., 0.01)

/**
 * The setup() function runs once when the program starts.
 * It's used to create the canvas and define initial properties.
 */
function setup() {
	// Create a 600x400 pixel canvas.
	createCanvas(600, 400);

	// Define the position of each vertex using createVector(x, y).
	// The positions are calculated relative to the canvas size.
	vertex1 = createVector(width / 2, height / 4);       // Top vertex
	vertex2 = createVector(width / 4, height * 3 / 4);   // Bottom-left vertex
	vertex3 = createVector(width * 3 / 4, height * 3 / 4);// Bottom-right vertex
}

/**
 * The draw() function runs in a loop and is used for animation.
 */
function draw() {
	// Set the background color.
	background(40, 44, 52);

	// --- Draw the vertices ---
	// We'll always show the points so we can see the animation's start and end points.
	stroke(97, 218, 251);    // A light blue color for the points
	strokeWeight(8);         // Make the points nice and visible
	point(vertex1.x, vertex1.y);
	point(vertex2.x, vertex2.y);
	point(vertex3.x, vertex3.y);

	// --- Style for the animated lines ---
	strokeWeight(3); // A thicker line for the outline

	// --- Animate the triangle drawing ---
	// This block handles the progressive drawing of the triangle's sides.

	// Phase 0: Draw the line from vertex1 to vertex2
	if (phase === 0) {
		animateLine(vertex1, vertex2);
	}

	// Phase 1: Draw the line from vertex2 to vertex3
	// First, draw the completed first line, then animate the second.
	if (phase === 1) {
		line(vertex1.x, vertex1.y, vertex2.x, vertex2.y); // Draw static first line
		animateLine(vertex2, vertex3);
	}

	// Phase 2: Draw the line from vertex3 back to vertex1
	// First, draw the two completed lines, then animate the final line.
	if (phase === 2) {
		line(vertex1.x, vertex1.y, vertex2.x, vertex2.y); // Draw static first line
		line(vertex2.x, vertex2.y, vertex3.x, vertex3.y); // Draw static second line
		animateLine(vertex3, vertex1);
	}
	
	// Phase 3: The triangle is complete
// Phase 3: The triangle is complete
	if (phase === 3) {
		// Add this line to disable the fill for the final shape
		noFill();

		// Set the style for the triangle's outline
		stroke(97, 218, 251); // Light blue
		strokeWeight(3);

		// Draw the final, complete triangle shape
		beginShape();
		vertex(vertex1.x, vertex1.y);
		vertex(vertex2.x, vertex2.y);
		vertex(vertex3.x, vertex3.y);
		endShape(CLOSE);

		// Calculate the midpoint for each side
		let mid1 = p5.Vector.lerp(vertex1, vertex2, 0.5);
		let mid2 = p5.Vector.lerp(vertex2, vertex3, 0.5);
		let mid3 = p5.Vector.lerp(vertex3, vertex1, 0.5);

		// Set a different style for the midpoints
		stroke(255, 70, 70); // A nice red color
		strokeWeight(7);     // Make them slightly smaller than the main vertices

		// Draw the midpoint on each side
		point(mid1.x, mid1.y);
		point(mid2.x, mid2.y);
		point(mid3.x, mid3.y);
		
		// Optional: stop the animation loop once drawing is complete
		// noLoop(); 
	}
}

/**
 * A helper function to animate a line from a startVector to an endVector.
 * @param {p5.Vector} startVector - The starting point of the line.
 * @param {p5.Vector} endVector - The ending point of the line.
 */
function animateLine(startVector, endVector) {
	// Increment the progress of the animation
	progress += animationSpeed;

	// Use lerp() to find the point between start and end for the current progress
	let currentPos = p5.Vector.lerp(startVector, endVector, progress);

	// Draw the line from the start to the current animated point
	line(startVector.x, startVector.y, currentPos.x, currentPos.y);

	// If the line is complete...
	if (progress >= 1.0) {
		progress = 0; // Reset progress for the next line
		phase++;      // Move to the next phase
	}
}