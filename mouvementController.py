from color import *
from time import sleep
import math
import time
start_time = time.time()
#The Sequence

#The Launch
def configLaunchSequence(FV):
    if(FV.isFlying):
        ########################################################
        sleep(1)
        print("\n=== Automatique Launch Sequence ===")
        FV.vessel.control.brakes = True;
        

        ########################################################

        print("\n  --Pre-flight initialisation--\n")
        sleep(1)
        print(green+"     Breakes Engage")

        sleep(1)
        print("     Throttle Engage")
        FV.vessel.control.throttle = 0.7
        sleep(1)

        print("     Auto_pilot Setup"+end)
        sleep(1)
        print(green+"     Auto_pilot Engage"+end)
        sleep(2)
def congifLaunchProcess(FV):
    if(FV.isFlying):
        print('\n  --Launch Process--\n')
        sleep(1)
        print(green+"     Firing up")
        FV.vessel.control.activate_next_stage()
        sleep(1)
        print("     Breakes Disengage")
        sleep(1)
        FV.vessel.control.brakes = False;
        print("     Auto_pilot Direction\n"+end)

    #Config Autopilot
    FV.ap.target_direction = (0, 1, 0)
def LaunchProcess(FV,srf_frame):
    if(FV.isFlying):
        while FV.srf_speed < 40:

            #Variable Flight
            FV.srf_speed = FV.vessel.flight(srf_frame).speed
            d = FV.vessel.direction(FV.vessel.orbit.body.reference_frame)
            v = FV.vessel.velocity(FV.vessel.orbit.body.reference_frame)
            dotprod = d[0]*v[0] + d[1]*v[1] + d[2]*v[2]
            vmag = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
            angle = 0
            if dotprod > 0:
                angle = abs(math.acos(dotprod / vmag) * (180.0 / math.pi))
            FV.altitude = FV.vessel.flight().surface_altitude
            roll = FV.vessel.flight().roll
            altitude_variation = FV.altitude-FV.prev_alt
            FV.prev_alt = FV.altitude

            flightStatus(FV.srf_speed,angle,FV.altitude,altitude_variation,roll,False)
            
            sleep(FV.delay)

#The TakeOff
def congifTakeOffProcess():
    print("\n  --TakeOff Process--\n")
def TakeOffProcess(FV,srf_frame):
    
    while not FV.takeoff:

        #Variable Flight
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
        altitude_variation = FV.altitude-FV.prev_alt
        FV.prev_alt = FV.altitude
        roll = FV.vessel.flight().roll
    
        
        takeOffGear(FV.srf_speed, FV.vessel)
        movement(pitch,FV.ap)
        FV.takeoff = statusTakeOff(FV.altitude)
        flightStatus(FV.srf_speed,angle,FV.altitude,altitude_variation,roll,False)


        sleep(FV.delay)

#After TakeOff
def configFreeFlight(ap):
    print("\n  --After TakeOff--\n")
    sleep(1)
    ap.target_direction = (0, 1, 0)
    ap.disengage()
    print(green+"     Auto_pilot Disengage")
    sleep(1)
    ap.sas = True
    print("     SAS Engage")
    sleep(1)

    print("     Free Flight"+end)
def FreeFlight(FV,srf_frame):
    run =True
    while(run):

        #Variable Flight
        FV.srf_speed = FV.vessel.flight(srf_frame).speed
        d = FV.vessel.direction(FV.vessel.orbit.body.reference_frame)
        v = FV.vessel.velocity(FV.vessel.orbit.body.reference_frame)
        dotprod = d[0]*v[0] + d[1]*v[1] + d[2]*v[2]
        vmag = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        angle = 0
        if dotprod > 0:
            angle = abs(math.acos(dotprod / vmag) * (180.0 / math.pi))
        FV.altitude = FV.vessel.flight().surface_altitude
        altitude_variation = FV.altitude-FV.prev_alt
        FV.prev_alt = FV.altitude
        roll = FV.vessel.flight().roll


        #Display
        flightStatus(FV.srf_speed,angle,FV.altitude,altitude_variation,roll,False)

        #Option
        if((altitude_variation < -150 and FV.altitude < 2500) or (altitude_variation < -110 and FV.altitude < 1500) ):
            pullUp(FV,srf_frame,angle,roll)
        elif(FV.srf_speed > 1361):
            OverSpeed(FV,srf_frame,angle,roll)
        elif((angle > 40 or angle <-40)and(roll>60 or roll < -60)and FV.altitude > 10):
            vrille(FV,srf_frame,angle,roll)
            pullUp(FV,srf_frame,angle,roll)
        sleep(FV.delay)

#Generic Display
def flightStatus(srf_speed,angle,altitude,altitude_variation,roll,error):
    

    speed = str(round(srf_speed)).ljust(4)
    mach = str(round(srf_speed/343,1)).ljust(3)
    altitudetxt = str(round(altitude)).ljust(5)
    vAltitude = str(round(altitude_variation)).ljust(5)
    angletxt = str(round(angle,1)).ljust(4)
    rolltxt = str(round(roll)).ljust(4)
    if(not error):
        if(srf_speed >= 1029):
            
            speed = orange+speed+end
            mach = orange+mach+end

        if(altitude_variation<=-100):
            if(altitude<1000):
                altitudetxt = orange + altitudetxt + end
            vAltitude = orange + vAltitude + end
        elif(altitude < 50 and altitude_variation <= 0):
            altitudetxt = orange + altitudetxt + end

        if(angle >15 or angle < -15):
            angletxt = orange + angletxt + end
            if(roll >30 or roll < -30):
                 rolltxt = orange + rolltxt + end
        elif(roll >100 or roll < -100):
            rolltxt = orange + rolltxt + end

    speed_padded  = '     |  Surface Speed = '+ speed +' m/s  |'
    mach_padded = '  '+ mach +' mach  |'
    AOA_padded = "  AOA = " + angletxt +" °  |"
    altitude_padded = "  Altitude = "+ altitudetxt +" m  |"
    vAltitude_padded = "  Altitude Variation = "+ vAltitude +" m  |"
    roll_padded = "  Roll = "+ rolltxt +" °  |"
    print(speed_padded + mach_padded + AOA_padded + roll_padded + altitude_padded + vAltitude_padded)

#Mouvement Controller 
def movement (pitch,ap):
    if(pitch < 5):
        ap.target_direction = (1, 1, 0)
    elif(pitch > 0 and pitch< 30 ):
        ap.target_direction = (0, 1, 0)
    else:
        ap.target_direction = (-1, 1, 0)

def statusTakeOff(altitude):
    if altitude > 1000:
        return True
    return False

def takeOffGear(srf_speed, vessel):
    if(vessel.control.gear and srf_speed > 60 ):
        print(green+"     Gear UP"+end)
        vessel.control.gear = False
        vessel.control.throttle = 1

def OverSpeed(FV,srf_frame,angle,roll):
    # Help Mode (Over Speed)
    print("     "+redB+"Help Mode (Over Speed)"+endB+red)
    FV.ap.engage()
    FV.ap.target_direction = (1, 0, 0)
    FV.vessel.control.throttle = 0.1
    FV.srf_speed = FV.vessel.flight(srf_frame).speed
    FV.altitude = FV.vessel.flight().surface_altitude
    altitude_variation = FV.altitude-FV.prev_alt
    FV.prev_alt = FV.altitude

    flightStatus(FV.srf_speed,angle,FV.altitude,altitude_variation,roll,True)
    sleep(2)

    FV.srf_speed = FV.vessel.flight(srf_frame).speed
    FV.altitude = FV.vessel.flight().surface_altitude
    altitude_variation = FV.altitude-FV.prev_alt
    FV.prev_alt = FV.altitude
    FV.ap.disengage()
    FV.ap.sas = True
    flightStatus(FV.srf_speed,angle,FV.altitude,altitude_variation,roll,True)
    print(end, end ="")

def pullUp(FV,srf_frame,angle,roll):

        # Help Mode (Pull Up)
        print("     "+redB+"Help Mode (Pull Up)"+endB+red)
        FV.ap.engage()
        FV.ap.target_direction = (1, 1, 0)
        FV.vessel.control.throttle = 0.1
        

        FV.srf_speed = FV.vessel.flight(srf_frame).speed
        FV.altitude = FV.vessel.flight().surface_altitude
        altitude_variation = FV.altitude-FV.prev_alt
        FV.prev_alt = FV.altitude
        FV.vessel.control.throttle = 0.6

        flightStatus(FV.srf_speed,angle,FV.altitude,altitude_variation,roll,True)

        sleep(3)

        FV.srf_speed = FV.vessel.flight(srf_frame).speed
        FV.altitude = FV.vessel.flight().surface_altitude
        altitude_variation = FV.altitude-FV.prev_alt
        FV.prev_alt =FV.altitude
        FV.ap.disengage()
        FV.ap.sas = True
        FV.vessel.control.throttle = 1

        flightStatus(FV.srf_speed,angle,FV.altitude,altitude_variation,roll,True)
        print(end, end ="")

def vrille(FV,srf_frame,angle,roll):
    # Help Mode (Vrille)
        print("     "+redB+"Help Mode (Vrille)"+endB+red)
        FV.ap.engage()
        FV.vessel.control.throttle = 0.2
        if(angle <0):
            FV.ap.target_direction = (1, 1, 1)
        else:
            FV.ap.target_direction = (-1, 1, -1)
        sleep(2)

        FV.srf_speed = FV.vessel.flight(srf_frame).speed
        FV.altitude = FV.vessel.flight().surface_altitude
        altitude_variation = FV.altitude-FV.prev_alt
        FV.prev_alt = FV.altitude
        FV.vessel.control.throttle = 0.5
        FV.ap.target_direction = (0, 1, 0)

        flightStatus(FV.srf_speed,angle,FV.altitude,altitude_variation,roll,True)
        sleep(1.5)
        FV.srf_speed = FV.vessel.flight(srf_frame).speed
        FV.altitude = FV.vessel.flight().surface_altitude
        altitude_variation = FV.altitude-FV.prev_alt
        FV.prev_alt = FV.altitude
        FV.ap.disengage()
        FV.ap.sas = True
        FV.vessel.control.throttle = 1
        flightStatus(FV.srf_speed,angle,FV.altitude,altitude_variation,roll,True)
        print(end, end ="")
