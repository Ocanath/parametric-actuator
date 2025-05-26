import FreeCAD as App
import Part
import Sketcher

class MotorControlPCB:
	def __init__(self):
		self.BoardThickness = 1.0	
		self.BottomLayerClearance = 1.0	#clearance from the bottom of board to highest component. 
		self.EncoderHeight = 0.5
		self.EncoderAirgap = 1.0
		self.BoardRadius = 20
		self.BoardSeatClearance = 0.3	#mm


class Bearing:
	def __init__(self, ID, OD, Height):
		self.ID = ID
		self.OD = OD
		self.Height = Height
		self.InnerRaceDiameter = self.ID + 1	#check
		self.OuterRaceClearance = 1

#TODO: initialize from a .yaml
#TODO: move to separate file
class FramelessMotor:
	def __init__(self):
		self.StatorOD = 38
		self.StatorHeight = 16
		self.StatorID = 22
		self.IsInrunner = True
		if(self.IsInrunner):
			self.StatorODMountClearance = 3	#radial dimension
		self.WireClearance = 2	#mm, applied to top and bottom
		
		self.RotorOD = 28
		self.RotorID = self.RotorOD/2
		self.RotorHeight = self.StatorHeight
		
#TODO: move this to separate file
class MotorParams:
	def __init__(self):
		self.stator = FramelessMotor()	#TODO: init all classes from actuator yaml
		self.mctl_pcb = MotorControlPCB()
		if(self.stator.IsInrunner):
			self.topBearing = Bearing(30, 17, 4)
			self.bottomBearing = Bearing(30, 17, 4)
		else:
			self.rotorBearing = Bearing(10,5,5)	#bleh
		self.BottomBearingSupportThickness = 2	#thickness of the base
		self.OuterWallThickness = 2
		self.GearboxHeightClearance = 2
#some motor parameter class, pulled all design defining dims from the yaml
mp = MotorParams()

doc = App.newDocument("StatorHousing")	#TODO: figure out how to open existing document, or close all before creating new; regenerating is annoying
App.setActiveDocument("StatorHousing")

App.ActiveDocument.recompute()

sketch = doc.addObject("Sketcher::SketchObject", "StatorHousingCrossSection")
sketch.Placement = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(1,0,0), 90))	# Rotate 90 degrees around X axis to get XZ plane

if(mp.stator.IsInrunner == True):
	p = []
	
	p.append(App.Vector(mp.bottomBearing.OD - mp.bottomBearing.OuterRaceClearance,0))
	p.append(App.Vector(p[0].x,mp.BottomBearingSupportThickness))
	innerWallRadius = mp.stator.StatorOD	#line to line
	p.append(App.Vector(innerWallRadius-mp.stator.StatorODMountClearance, p[len(p)-1].y))
	p.append(App.Vector(p[len(p)-1].x, p[len(p)-1].y + mp.stator.WireClearance)) #vertical
	p.append(App.Vector(innerWallRadius, p[len(p)-1].y)) #horizontal
	heightFromStatorBase  = mp.stator.StatorHeight + mp.topBearing.Height + mp.GearboxHeightClearance
	p.append(App.Vector(p[len(p)-1].x, p[len(p)-1].y + heightFromStatorBase)) #vertical	#increase y to add clearance for the top bearing
	outerWallRadius = innerWallRadius + mp.OuterWallThickness
	p.append(App.Vector(outerWallRadius, p[len(p)-1].y))	#horizontal

	"""
	Create a seat for the pcb. Note: for an inrunner with top and bottom bearing, the rotor will rest on the bearing races and will be retained that way, 
	so retaining rings should not be necessary
	"""
	distFromOriginToBase = mp.bottomBearing.Height + mp.mctl_pcb.BoardThickness + mp.mctl_pcb.EncoderAirgap + mp.mctl_pcb.EncoderHeight 
	p.append(App.Vector(p[len(p)-1].x, p[0].y - distFromOriginToBase))
	p.append(App.Vector(mp.mctl_pcb.BoardRadius, p[len(p)-1].y))
	p.append(App.Vector(p[len(p)-1].x, p[len(p)-1].y + mp.mctl_pcb.BoardThickness))
	p.append(App.Vector(p[len(p)-1].x-mp.mctl_pcb.BoardSeatClearance, p[len(p)-1].y))
	p.append(App.Vector(p[len(p)-1].x, p[0].y - mp.bottomBearing.Height))
	p.append(App.Vector(mp.bottomBearing.OD, p[len(p)-1].y))
	p.append(App.Vector(p[len(p)-1].x, 0))
	p.append(App.Vector(p[0].x, p[len(p)-1].y))



	#TODO: load points into an array and play back 
	lines = []
	for i in range(len(p)-1):
		line = sketch.addGeometry(Part.LineSegment(p[i],p[i+1]))
		lines.append(line)
		if i > 0:  # For all lines after the first one
			# Make end point of previous line coincident with start point of current line
			sketch.addConstraint(Sketcher.Constraint('Coincident', lines[i-1], 2, lines[i], 1))
		elif i == 0:  # For the first line
			# Fix the start point at the origin using distance constraints
			sketch.addConstraint(Sketcher.Constraint('DistanceX', lines[i], 1, p[0].x))  # Fix x at 0
			sketch.addConstraint(Sketcher.Constraint('DistanceY', lines[i], 1, p[0].y))  # Fix y at 0
		
		# Check if line is horizontal (same y coordinates)
		if abs(p[i].y - p[i+1].y) < 1e-6:
			sketch.addConstraint(Sketcher.Constraint('Horizontal', i))
			# Add distance constraint for horizontal lines
			sketch.addConstraint(Sketcher.Constraint('Distance', i, abs(p[i+1].x - p[i].x)))
		# Check if line is vertical (same x coordinates)
		elif abs(p[i].x - p[i+1].x) < 1e-6:
			sketch.addConstraint(Sketcher.Constraint('Vertical', i))
			# Add distance constraint for vertical lines
			sketch.addConstraint(Sketcher.Constraint('Distance', i, abs(p[i+1].y - p[i].y)))
	

doc.recompute()

# Create the revolution
revolve = doc.addObject("Part::Revolution", "StatorHousing")
revolve.Source = sketch
revolve.Axis = (0, 0, 1)  # Z axis
revolve.Base = (0, 0, 0)  # Origin point
revolve.Angle = 360  # Full revolution

doc.recompute()


