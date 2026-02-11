import krpc
from color import *
from  mouvementController import *
from playsound import *
########################################################

link = krpc.connect(name="bot")

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

########################################################

configLaunchSequence(FV)

#Config Autopilot
FV.ap.target_roll = 0;
FV.ap.target_heading = 0;
FV.ap.reference_frame = FV.vessel.surface_velocity_reference_frame
obt_frame = FV.vessel.orbit.body.non_rotating_reference_frame
srf_frame = FV.vessel.orbit.body.reference_frame
ref_frame = link.space_center.ReferenceFrame.create_hybrid(
    position=FV.vessel.orbit.body.reference_frame,
    rotation=FV.vessel.surface_reference_frame)
FV.ap.engage()

########################################################

congifLaunchProcess(FV)
LaunchProcess(FV,srf_frame)

########################################################

congifTakeOffProcess()
TakeOffProcess(FV,srf_frame)

########################################################

configFreeFlight(FV.ap)
FreeFlight(FV,srf_frame)

