// Define three variables to hold the vector positions of the triangle's corners.
let vertex1, vertex2, vertex3;

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
 * Here, we just draw a static triangle.
 */
function draw() {
	// Set the background color.
	background(40, 44, 52);

	// Set the drawing style for the triangle.
	noFill();                       // No fill color
	stroke(97, 218, 251);           // A light blue outline color
	strokeWeight(3);                // A thicker line for the outline

	// Draw the triangle by connecting the three vertices.
	beginShape();
	vertex(vertex1.x, vertex1.y);
	vertex(vertex2.x, vertex2.y);
	vertex(vertex3.x, vertex3.y);
	endShape(CLOSE); // CLOSE connects the last vertex back to the first.
}