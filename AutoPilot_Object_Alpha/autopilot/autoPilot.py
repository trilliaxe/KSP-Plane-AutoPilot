
from utils.color import *
from controller.launchController import *
from controller.emergencyController import *
from controller.takeOffController import *
from controller.freeFlightController import *



def runAutoPilot(FV, link):
    """
    Execute the complete autopilot sequence for airplane flight.
    
    Flight sequence:
    1. Pre-launch configuration and system checks
    2. Launch process (engine start, brake release)
    3. Takeoff process (acceleration, gear retraction, climb to 1000m)
    4. Free flight (continuous monitoring with emergency handling)
    
    Args:
        FV: FlightVessel object containing all vessel data and state         
        link: kRPC connection object
    
    
    """
    
    # ==================== PRE-LAUNCH CONFIGURATION ====================
    
    configLaunchSequence(FV)

    # Configure the AutoPilot reference frames and initial settings
    FV.ap.target_roll = 0  # Maintain wings level
    FV.ap.target_heading = 0  # Maintain north heading
    FV.ap.reference_frame = FV.vessel.surface_velocity_reference_frame
    
    # Define reference frames for flight calculations
    obt_frame = FV.vessel.orbit.body.non_rotating_reference_frame
    srf_frame = FV.vessel.orbit.body.reference_frame
    
    # Create hybrid reference frame (body position with surface rotation)
    ref_frame = link.space_center.ReferenceFrame.create_hybrid(
        position=FV.vessel.orbit.body.reference_frame,
        rotation=FV.vessel.surface_reference_frame
    )
    
    FV.ap.engage()

    # ==================== LAUNCH PROCESS ====================

    congifLaunchProcess(FV)
    LaunchProcess(FV, srf_frame)

    # ==================== TAKEOFF PROCESS ====================
    congifTakeOffProcess()
    TakeOffProcess(FV, srf_frame)

    # ==================== FREE FLIGHT PROCESS ====================
    configFreeFlight(FV.ap)
    FreeFlight(FV, srf_frame)