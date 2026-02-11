import krpc
from autopilot.autoPilot import *
from playsound import *


#Setup KRPC connection

link = krpc.connect(name="AutoPilot Object Alpha")

class FlightValues:
  def __init__(self,vessel,srf_speed,altitude,prev_alt):
    self.vessel = vessel
    self.ap = vessel.auto_pilot
    self.takeoff = False
    self.delay = 0.8
    self.isFlying = vessel.flight().surface_altitude <20
    self.srf_speed = srf_speed
    self.altitude = altitude
    self.prev_alt = prev_alt

FV = FlightValues(link.space_center.active_vessel, 0,0,0) 

#Run the AutoPilot

runAutoPilot(FV,link)