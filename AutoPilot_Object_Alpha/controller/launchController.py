from utils.color import *
from utils.loggerFlightStatus import *
from time import sleep
import math
import time

start_time = time.time()


# ==================== LAUNCH SEQUENCE ====================

def configLaunchSequence(FV):
    """
    Configure the launch sequence before takeoff.
    
    Performs pre-flight checks and configures systems:
    - Activates brakes
    - Sets throttle to 70%
    - Prepares autopilot
    
    Args:
        FV: FlightVessel object containing vessel data
            - FV.isFlying (bool): Indicates if vessel is in flight mode
            - FV.vessel: Reference to kRPC vessel
    """
    if FV.isFlying:
        sleep(1)
        print("\n=== Automatique Launch Sequence ===")
        FV.vessel.control.brakes = True
        
        print("\n  --Pre-flight initialisation--\n")
        sleep(1)
        print(green + "     Breakes Engage")

        sleep(1)
        print("     Throttle Engage")
        FV.vessel.control.throttle = 0.7
        sleep(1)

        print("     Auto_pilot Setup" + end)
        sleep(1)
        print(green + "     Auto_pilot Engage" + end)
        sleep(2)


def congifLaunchProcess(FV):
    """
    Execute the airplane launch process.
    
    - Activates next stage (engine ignition)
    - Releases brakes
    - Configures autopilot direction upward
    
    Args:
        FV: FlightVessel object
            - FV.isFlying (bool): Flight mode active
            - FV.vessel: Reference to vessel
            - FV.ap: Vessel autopilot
    """
    if FV.isFlying:
        print('\n  --Launch Process--\n')
        sleep(1)
        print(green + "     Firing up")
        FV.vessel.control.activate_next_stage()
        sleep(1)
        print("     Breakes Disengage")
        sleep(1)
        FV.vessel.control.brakes = False
        print("     Auto_pilot Direction\n" + end)

    # Config Autopilot - Vertical direction (0, 1, 0)
    FV.ap.target_direction = (0, 1, 0)


def LaunchProcess(FV, srf_frame):
    """
    Manage ground acceleration phase until 40 m/s.
    
    Continuously monitors:
    - Surface speed
    - Angle of attack
    - Altitude
    - Roll
    
    Args:
        FV: FlightVessel object with all flight data
        srf_frame: Surface reference frame for speed measurements
    
    Note:
        Active loop until surface speed reaches 40 m/s
    """
    if FV.isFlying:
        while FV.srf_speed < 40:
            # Flight variables
            FV.srf_speed = FV.vessel.flight(srf_frame).speed
            d = FV.vessel.direction(FV.vessel.orbit.body.reference_frame)
            v = FV.vessel.velocity(FV.vessel.orbit.body.reference_frame)
            dotprod = d[0]*v[0] + d[1]*v[1] + d[2]*v[2]
            vmag = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
            
            # Angle of attack calculation
            angle = 0
            if dotprod > 0:
                angle = abs(math.acos(dotprod / vmag) * (180.0 / math.pi))
            
            FV.altitude = FV.vessel.flight().surface_altitude
            roll = FV.vessel.flight().roll
            altitude_variation = FV.altitude - FV.prev_alt
            FV.prev_alt = FV.altitude

            displayFlightStatus(FV.srf_speed, angle, FV.altitude, altitude_variation, roll, False)
            sleep(FV.delay)

