from utils.color import *
from utils.loggerFlightStatus import *
from controller.movementController import *
from time import sleep
import math



# ==================== TAKEOFF ====================

def congifTakeOffProcess():
    """
    Display takeoff process start message.
    """
    print("\n  --TakeOff Process--\n")


def TakeOffProcess(FV, srf_frame):
    """
    Manage takeoff phase until 1000m altitude.
    
    Performs:
    - Continuous monitoring of flight parameters
    - Landing gear retraction if speed > 60 m/s
    - Pitch adjustments via movement()
    - Altitude verification to confirm takeoff
    
    Args:
        FV: FlightVessel object
        srf_frame: Surface reference frame
    
    Note:
        Active loop until FV.takeoff is True (altitude > 1000m)
    """
    while not FV.takeoff:
        # Flight variables
        FV.srf_speed = FV.vessel.flight(srf_frame).speed
        pitch = FV.vessel.flight().pitch
        d = FV.vessel.direction(FV.vessel.orbit.body.reference_frame)
        v = FV.vessel.velocity(FV.vessel.orbit.body.reference_frame)
        dotprod = d[0]*v[0] + d[1]*v[1] + d[2]*v[2]
        vmag = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        
        angle = 0
        if dotprod > 0:
            angle = abs(math.acos(dotprod / vmag) * (180.0 / math.pi))
        
        FV.altitude = FV.vessel.flight().surface_altitude
        altitude_variation = FV.altitude - FV.prev_alt
        FV.prev_alt = FV.altitude
        roll = FV.vessel.flight().roll
        
        takeOffGear(FV.srf_speed, FV.vessel)
        movement(pitch, FV.ap)
        FV.takeoff = statusTakeOff(FV.altitude)
        displayFlightStatus(FV.srf_speed, angle, FV.altitude, altitude_variation, roll, False)

        sleep(FV.delay)

