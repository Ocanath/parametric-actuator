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
		self.WireClearance = 1	#mm, applied to top and bottom
		
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
		self.BaseThickness = 2	#thickness of the base


#some motor parameter class, pulled all design defining dims from the yaml
mp = MotorParams()


doc = App.newDocument("stator-housing")
App.setActiveDocument("stator-housing")
App.ActiveDocument.recompute()

sketch = doc.addObject("Sketcher::SketchObject", "StatorHousingCrossSection")
sketch.Placement = App.Placement(App.Vector(0,0,0), App.Rotation(0,0,0,1))	#position, orientation. TODO pull in the rotation matrix translation helper function from the parametric gear design work you did earlier

p1 = App.Vector(mp.bottomBearing.OD - mp.bottomBearing.OuterRaceClearance,0)
p2 = App.Vector(p1.x,mp.BaseThickness)

doc.recompute()