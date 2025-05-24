import FreeCAD as App
import Part
import Sketcher


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
		self.stator = FramelessMotor()	#init all classes from actuator yaml
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
	parr = []
	
	p1 = App.Vector(mp.bottomBearing.OD - mp.bottomBearing.OuterRaceClearance,0)
	p2 = App.Vector(p1.x,mp.BottomBearingSupportThickness)
	innerWallRadius = mp.stator.StatorOD	#line to line
	p3 = App.Vector(innerWallRadius-mp.stator.StatorODMountClearance, p2.y)
	p4 = App.Vector(p3.x, p3.y + mp.stator.WireClearance) #vertical
	p5 = App.Vector(innerWallRadius, p4.y) #horizontal
	heightFromStatorBase  = mp.stator.StatorHeight + mp.topBearing.Height + mp.GearboxHeightClearance
	p6 = App.Vector(p5.x, p5.y + heightFromStatorBase) #vertical	#increase y to add clearance for the top bearing
	outerWallRadius = innerWallRadius + mp.OuterWallThickness
	p7 = App.Vector(outerWallRadius, p6.y)	#horizontal
	p8 = App.Vector(p7.x, -mp.bottomBearing.Height)
	p9 = App.Vector(mp.bottomBearing.OD, p8.y)
	p10 = App.Vector(p9.x, 0)
	p11 = App.Vector(p1.x, p10.y)

	#TODO: load points into an array and play back 
	sketch.addGeometry(Part.LineSegment(p1,p2))
	sketch.addGeometry(Part.LineSegment(p2,p3))
	sketch.addGeometry(Part.LineSegment(p3,p4))
	sketch.addGeometry(Part.LineSegment(p4,p5))
	sketch.addGeometry(Part.LineSegment(p5,p6))
	sketch.addGeometry(Part.LineSegment(p6,p7))
	sketch.addGeometry(Part.LineSegment(p7,p8))
	sketch.addGeometry(Part.LineSegment(p8,p9))
	sketch.addGeometry(Part.LineSegment(p9,p10))
	sketch.addGeometry(Part.LineSegment(p10,p11))
	

doc.recompute()

