import FreeCAD as App
import Part
import Sketcher

class MotorControlPCB:
	def __init__(self):
		self.BoardThickness = 1.0	
		self.BottomLayerClearance = 1.0	#clearance from the bottom of board to highest component. 
		self.EncoderHeight = 0.5
		self.EncoderAirgap = 1.0
		self.BoardRadius = 16
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
		self.StatorOD = 60
		self.StatorHeight = 26
		self.StatorID = 30
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
			self.topBearing = Bearing(16, 8, 4)
			self.bottomBearing = Bearing(16, 8, 4)
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
sketch.Placement = App.Placement(App.Vector(0,0,0), App.Rotation(0,0,0,1))	#position, orientation. TODO pull in the rotation matrix translation helper function from the parametric gear design work you did earlier

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
	for i in range(0,len(p)-1):
		sketch.addGeometry(Part.LineSegment(p[i],p[i+1]))
	

doc.recompute()

