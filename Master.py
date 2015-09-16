import sys, os
from LeapMotion import Leap,LeapMotion_Driver
from Lights import DMX_Driver
import time

def main():
    '''
    Main Script for converting hand motions recorded by LeapMotion device to mechanical motion and colors in the light (beamZ IntiScan300).
    -Motion of the right hand moves the light connected to ttyUSB0
    -Motion of the left hand moves the light connected to ttyUSB1
    -A rapid swipe to the right or left changes the color of the corresponding light.

    @author: Thomas Haase and Jami L Johnson
    September 14, 2015
    '''
    go = True
    try:
        print "Starting Initialization"
        leapDev = LeapMotion_Driver.LeapListener()
        controller = Leap.Controller()
        controller.add_listener(leapDev)
        print "Connected to LeapMotion"
#        dmx_right = DMX_Driver.DMX_Controller("/dev/ttyUSB0",1,0,False)
#        dmx_left = DMX_Driver.DMX_Controller("/dev/ttyUSB1",1,4,True)
        dmx_guy = DMX_Driver.DMX_Controller_Chained("/dev/ttyUSB0",1,0,100,4,False,True)
        print "Connected to Lights"
            
        while go == True:
            
            all_hands, all_gestures  = leapDev.get_frame(controller)
            # initialize hand positions
            left_position = Leap.Vector(1, 0.5, 0)
            right_position = Leap.Vector(1, 0.5, 0)        
        
            # initialize grip strength
            left_grip_strength = 0        
            right_grip_strength = 0
 
            for hand in all_hands:
                if hand.is_left:
                    left_position = hand.palm_position
                    left_grip_strength = hand.grab_strength
                  
                    if hand.palm_velocity[0] < -900:
                        print 'left swipe'
#                        dmx_left.change_color()
                        dmx_guy.change_color(False)
                        time.sleep(0.1)
                else:
                    right_position = hand.palm_position
                    right_grip_strength = hand.grab_strength

                    if hand.palm_velocity[0] > 900:
                        print 'right swipe'
#                        dmx_right.change_color()
                        dmx_guy.change_color(True)
                        time.sleep(0.1)
            
#            dmx_right.update_position(right_position)
#            dmx_left.update_position(left_position)
            
#            dmx_right.light_intensity(right_grip_strength)
#            dmx_left.light_intensity(left_grip_strength)
            
            dmx_guy.update_position(right_position,left_position)
            dmx_guy.light_intensity(right_grip_strength,left_grip_strength)
    except KeyboardInterrupt:
        go = False
        print 'Exiting Script'
        controller.remove_listener(leapDev)
        sys.exit(0)
    
if __name__ == "__main__":
    main()
