

from utils.color import *
# ==================== DISPLAY ====================

def displayFlightStatus(srf_speed, angle, altitude, altitude_variation, roll, error):
    """
    Display real-time flight status with color-coded alerts.
    
    Displays:
    - Surface speed (m/s) and Mach number
    - Angle of attack (AOA)
    - Roll
    - Altitude
    - Altitude variation
    
    Color system:
    - Orange: Alert situation (overspeed, dive, excessive angles)
    - Green/Normal: Normal flight conditions
    """
    speed = str(round(srf_speed)).ljust(4)
    mach = str(round(srf_speed/343, 1)).ljust(3)
    altitudetxt = str(round(altitude)).ljust(5)
    vAltitude = str(round(altitude_variation)).ljust(5)
    angletxt = str(round(angle, 1)).ljust(4)
    rolltxt = str(round(roll)).ljust(4)
    
    if not error:
        # Overspeed alert (> Mach 3)
        if srf_speed >= 1029:
            speed = orange + speed + end
            mach = orange + mach + end

        # Dangerous dive alert
        if altitude_variation <= -100:
            if altitude < 1000:
                altitudetxt = orange + altitudetxt + end
            vAltitude = orange + vAltitude + end
        elif altitude < 50 and altitude_variation <= 0:
            altitudetxt = orange + altitudetxt + end

        # Excessive angle of attack and roll alert
        if angle > 15 or angle < -15:
            angletxt = orange + angletxt + end
            if roll > 30 or roll < -30:
                rolltxt = orange + rolltxt + end
        elif roll > 100 or roll < -100:
            rolltxt = orange + rolltxt + end

    speed_padded = '     |  Surface Speed = ' + speed + ' m/s  |'
    mach_padded = '  ' + mach + ' mach  |'
    AOA_padded = "  AOA = " + angletxt + " °  |"
    altitude_padded = "  Altitude = " + altitudetxt + " m  |"
    vAltitude_padded = "  Altitude Variation = " + vAltitude + " m  |"
    roll_padded = "  Roll = " + rolltxt + " °  |"
    
    print(speed_padded + mach_padded + AOA_padded + roll_padded + 
          altitude_padded + vAltitude_padded)