
from utils.color import *
from utils.loggerFlightStatus import *
from controller.emergencyController import *
from time import sleep
import math
import time

start_time = time.time()

# ==================== FREE FLIGHT ====================

def configFreeFlight(ap):
    """
    Configure vessel for free flight after takeoff.
    
    - Disengages autopilot
    - Activates SAS (Stability Augmentation System)
    - Resets target direction to (0, 1, 0)
    
    Args:
        ap: Vessel autopilot
    """
    print("\n  --After TakeOff--\n")
    sleep(1)
    ap.target_direction = (0, 1, 0)
    ap.disengage()
    print(green + "     Auto_pilot Disengage")
    sleep(1)
    ap.sas = True
    print("     SAS Engage")
    sleep(1)
    print("     Free Flight" + end)


def FreeFlight(FV, srf_frame):
    """
    Manage free flight with automatic emergency situation monitoring.
    
    Automatically detects and corrects:
    - Dangerous dive (altitude_variation < -150 and altitude < 2500)
    - Overspeed (> 1361 m/s, approximately Mach 4)
    - Spin (angle > 40° and roll > 60° and altitude > 10m)
    
    Args:
        FV: FlightVessel object
        srf_frame: Surface reference frame
    
    Note:
        Infinite loop with continuous monitoring of flight parameters
    """
    run = True
    while run:
        # Flight variables
        FV.srf_speed = FV.vessel.flight(srf_frame).speed
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

        # Display flight data
        displayFlightStatus(FV.srf_speed, angle, FV.altitude, altitude_variation, roll, False)

        # Automatic emergency situation management
        if (altitude_variation < -150 and FV.altitude < 2500) or \
           (altitude_variation < -110 and FV.altitude < 1500):
            pullUp(FV, srf_frame, angle, roll)
        elif FV.srf_speed > 1361:
            OverSpeed(FV, srf_frame, angle, roll)
        elif (angle > 40 or angle < -40) and (roll > 60 or roll < -60) and FV.altitude > 10:
            vrille(FV, srf_frame, angle, roll)
            pullUp(FV, srf_frame, angle, roll)
        
        sleep(FV.delay)


