import FreeCAD as App
import Part
import Sketcher
from enum import Enum, auto

class LineOrientation(Enum):
	HORIZONTAL = 'h'
	VERTICAL = 'v'

def create_constrained_line(sketch, start_point, length, orientation=LineOrientation.HORIZONTAL):
	"""
	Creates a horizontal or vertical line with appropriate constraints.
	
	Args:
		sketch: The sketch object to add the line to
		start_point: App.Vector representing the start point
		length: Length of the line (positive for right/up, negative for left/down)
		orientation: LineOrientation enum ('h' for horizontal, 'v' for vertical)
	
	Returns:
		The created line object
	"""
	# Calculate end point based on orientation
	if orientation == LineOrientation.HORIZONTAL:
		end_point = App.Vector(start_point.x + length, start_point.y, 0)
	else:  # VERTICAL
		end_point = App.Vector(start_point.x, start_point.y + length, 0)
	
	# Create the line
	line = sketch.addGeometry(Part.LineSegment(start_point, end_point))
	
	# Add appropriate constraint
	if orientation == LineOrientation.HORIZONTAL:
		sketch.addConstraint(Sketcher.Constraint('Horizontal', line))
	else:  # VERTICAL
		sketch.addConstraint(Sketcher.Constraint('Vertical', line))
	
	# Add distance constraint
	sketch.addConstraint(Sketcher.Constraint('Distance', line, abs(length)))
	
	return line

def join_lines(sketch, line1, line2):
    """
    Joins two lines by making the end point of line1 coincident with the start point of line2.
    
    Args:
        sketch: The sketch object containing the lines
        line1: First line object
        line2: Second line object
    
    Returns:
        None
    """
    # Add coincident constraint between end of line1 and start of line2
    sketch.addConstraint(Sketcher.Constraint('Coincident', line1, 2, line2, 1))


