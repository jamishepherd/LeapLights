import sys, os
from LeapMotion import Leap,LeapMotion_Driver
from Lights import DMX_Driver

def main():
    try:
        print "Starting Initialization"
        leapDev = LeapMotion_Driver.LeapListener()
        controller = Leap.Controller()
        controller.add_listener(leapDev)
        print "Connected to LeapMotion"
        dmx_right = DMX_Driver.DMX_Controller("/dev/ttyUSB0",1,0,False)
        dmx_left = DMX_Driver.DMX_Controller("/dev/ttyUSB1",1,4,True)
        print "Connected to Lights"
        
        while True:
            
            # initialize hand positions
            left_position = Leap.Vector(1, 0.5, 0)
            right_position = Leap.Vector(1, 0.5, 0)        
        
            # initialize grip strength
            left_grip_strength = 0        
            right_grip_strength = 0
            
            all_hands, all_gestures  = leapDev.get_frame(controller)
 
            for hand in all_hands:
                if hand.is_left:
                    left_position = hand.palm_position
                    left_grip_strength = hand.grab_strength
                else:
                    right_position = hand.palm_position
                    right_grip_strength = hand.grab_strength

            dmx_right.update_position(right_position)
            dmx_left.update_position(left_position)
            
            dmx_right.light_intensity(right_grip_strength)
            dmx_left.light_intensity(left_grip_strength)

            for gesture in all_gestures:
                print "Gesture happened."
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = Leap.SwipeGesture(gesture)
                    print "Swipe event happened."
                    if (swipe.direction[0] > 0.8):
                        dmx_right.change_color()                        
                        print 'swipe right detected.'
                    elif (swipe.direction[0] < (-0.8)):
                        dmx_left.change_color()
                        print 'swipe left detected.'
                        
    except KeyboardInterrupt:
        pass
    finally:
        'Exiting Script'
        controller.remove_listener(leapDev)
        sys.exit(0)
    
if __name__ == "__main__":
    main()
