
from utils.color import *
from utils.loggerFlightStatus import *
from time import sleep
import time

start_time = time.time()

def movement(pitch, ap):
    """
    Adjust autopilot direction based on pitch angle.
    
    Strategy:
    - pitch < 5°: Point upward (1, 1, 0)
    - 5° < pitch < 30°: Maintain horizontal (0, 1, 0)
    - pitch > 30°: Point downward (-1, 1, 0)
    
    Args:
        pitch (float): Current pitch angle in degrees
        ap: Vessel autopilot
    """
    if pitch < 5:
        ap.target_direction = (1, 1, 0)
    elif 0 < pitch < 30:
        ap.target_direction = (0, 1, 0)
    else:
        ap.target_direction = (-1, 1, 0)


def statusTakeOff(altitude):
    """
    Check if takeoff is successful.
    
    Args:
        altitude (float): Current altitude in meters
    
    Returns:
        bool: True if altitude > 1000m, False otherwise
    """
    if altitude > 1000:
        return True
    return False


def takeOffGear(srf_speed, vessel):
    """
    Automatically retract landing gear during takeoff.
    
    Retraction conditions:
    - Gear currently deployed
    - Speed > 60 m/s
    
    Also increases throttle to 100% during retraction.
    
    Args:
        srf_speed (float): Surface speed in m/s
        vessel: Reference to kRPC vessel
    """
    if vessel.control.gear and srf_speed > 60:
        print(green + "     Gear UP" + end)
        vessel.control.gear = False
        vessel.control.throttle = 1

