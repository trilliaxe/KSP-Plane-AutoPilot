
from utils.color import *
from utils.loggerFlightStatus import *
from time import sleep
import time

start_time = time.time()
# ==================== EMERGENCY MODES ====================

def OverSpeed(FV, srf_frame, angle, roll):
    """
    Emergency mode: Overspeed.
    
    Triggered when speed exceeds 1361 m/s (~Mach 4).
    
    Corrective actions:
    - Engages autopilot
    - Points nose upward (1, 0, 0)
    - Reduces throttle to 10%
    - Waits 2 seconds
    - Disengages autopilot and re-activates SAS
    
    Args:
        FV: FlightVessel object
        srf_frame: Surface reference frame
        angle (float): Current angle of attack
        roll (float): Current roll
    """
    print("     " + redB + "Help Mode (Over Speed)" + endB + red)
    FV.ap.engage()
    FV.ap.target_direction = (1, 0, 0)
    FV.vessel.control.throttle = 0.1
    
    FV.srf_speed = FV.vessel.flight(srf_frame).speed
    FV.altitude = FV.vessel.flight().surface_altitude
    altitude_variation = FV.altitude - FV.prev_alt
    FV.prev_alt = FV.altitude

    displayFlightStatus(FV.srf_speed, angle, FV.altitude, altitude_variation, roll, True)
    sleep(2)

    FV.srf_speed = FV.vessel.flight(srf_frame).speed
    FV.altitude = FV.vessel.flight().surface_altitude
    altitude_variation = FV.altitude - FV.prev_alt
    FV.prev_alt = FV.altitude
    FV.ap.disengage()
    FV.ap.sas = True
    
    displayFlightStatus(FV.srf_speed, angle, FV.altitude, altitude_variation, roll, True)
    print(end, end="")


def pullUp(FV, srf_frame, angle, roll):
    """
    Emergency mode: Pull up recovery.
    
    Triggered during dangerous dive:
    - Altitude variation < -150 m/s and altitude < 2500m
    - Altitude variation < -110 m/s and altitude < 1500m
    
    Corrective actions:
    - Engages autopilot
    - Points upward (1, 1, 0)
    - Reduces throttle to 10% then 60%
    - Maintains for 3 seconds
    - Disengages autopilot and restores full throttle
    
    Args:
        FV: FlightVessel object
        srf_frame: Surface reference frame
        angle (float): Current angle of attack
        roll (float): Current roll
    """
    print("     " + redB + "Help Mode (Pull Up)" + endB + red)
    FV.ap.engage()
    FV.ap.target_direction = (1, 1, 0)
    FV.vessel.control.throttle = 0.1

    FV.srf_speed = FV.vessel.flight(srf_frame).speed
    FV.altitude = FV.vessel.flight().surface_altitude
    altitude_variation = FV.altitude - FV.prev_alt
    FV.prev_alt = FV.altitude
    FV.vessel.control.throttle = 0.6

    displayFlightStatus(FV.srf_speed, angle, FV.altitude, altitude_variation, roll, True)
    sleep(3)

    FV.srf_speed = FV.vessel.flight(srf_frame).speed
    FV.altitude = FV.vessel.flight().surface_altitude
    altitude_variation = FV.altitude - FV.prev_alt
    FV.prev_alt = FV.altitude
    FV.ap.disengage()
    FV.ap.sas = True
    FV.vessel.control.throttle = 1

    displayFlightStatus(FV.srf_speed, angle, FV.altitude, altitude_variation, roll, True)
    print(end, end="")


def vrille(FV, srf_frame, angle, roll):
    """
    Emergency mode: Spin recovery.
    
    Triggered when airplane is in a spin:
    - Angle of attack > 40° or < -40°
    - Roll > 60° or < -60°
    - Altitude > 10m
    
    Corrective actions:
    - Engages autopilot
    - Applies directional correction based on spin direction
    - Reduces throttle to 20% then 50%
    - Progressively centers to (0, 1, 0)
    - Waits 3.5 seconds total
    - Disengages autopilot and restores full throttle
    
    Args:
        FV: FlightVessel object
        srf_frame: Surface reference frame
        angle (float): Current angle of attack
        roll (float): Current roll
    """
    print("     " + redB + "Help Mode (Vrille)" + endB + red)
    FV.ap.engage()
    FV.vessel.control.throttle = 0.2
    
    # Correction direction based on spin direction
    if angle < 0:
        FV.ap.target_direction = (1, 1, 1)
    else:
        FV.ap.target_direction = (-1, 1, -1)
    
    sleep(2)

    FV.srf_speed = FV.vessel.flight(srf_frame).speed
    FV.altitude = FV.vessel.flight().surface_altitude
    altitude_variation = FV.altitude - FV.prev_alt
    FV.prev_alt = FV.altitude
    FV.vessel.control.throttle = 0.5
    FV.ap.target_direction = (0, 1, 0)

    displayFlightStatus(FV.srf_speed, angle, FV.altitude, altitude_variation, roll, True)
    sleep(1.5)
    
    FV.srf_speed = FV.vessel.flight(srf_frame).speed
    FV.altitude = FV.vessel.flight().surface_altitude
    altitude_variation = FV.altitude - FV.prev_alt
    FV.prev_alt = FV.altitude
    FV.ap.disengage()
    FV.ap.sas = True
    FV.vessel.control.throttle = 1
    
    displayFlightStatus(FV.srf_speed, angle, FV.altitude, altitude_variation, roll, True)
    print(end, end="")