import Leap, sys,os
from new_driver import LeapListener
#import dmx_control

def main():
    try:
        while True:
            leapDev = LeapListener()
            controller = Leap.Controller()
            
            # initialize hand positions
            left_position = Leap.Vector(1, 1, 0)
            right_position = Leap.Vector(1, 1, 0)

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

            self.dmx_right.update_position(right_position)
            self.dmx_left.update_position(left_position)
            
            self.dmx_right.light_intensity(right_grip_strength)
            self.dmx_left.light_intensity(left_grip_strength)  

            for gesture in all_gestures:
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    if swipe.direction[0] > 0.8:
                        print 'swipe right'
                    elif swipe.direction[0] < -0.8:
                        print 'swipe left detected'
    except KeyboardInterrupt:
        pass
    finally:
        'Exiting Script'
        controller.remove_listener(leapDev)
        sys.exit(0)
    
if __name__ == "__main__":
    main()
