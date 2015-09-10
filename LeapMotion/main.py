"""
Main script for reading leap motion control devices and interfacing the information to a DMX controler.

"""

import Leap, sys, thread, time
from Leap import SwipeGesture
import dmx_control


class LeapListener(Leap.Listener):
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    dmx_right = dmx_control.dmx_controller("/dev/ttyUSB0",1,0)
#    dmx_left = dmx_control.dmx_controller("Hi I am random port also",9)
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
    
    def on_disconnect(self, controller):
        print "Disconnected"
        
    def on_exit(self, controller):
        print "Exited"
        
    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

#        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        left_position = Leap.Vector(1, 1, 0)
        right_position = Leap.Vector(1, 1, 0)
        
        left_grip_strength = 0        
        right_grip_strength = 0
        
        for hand in frame.hands:
#            handType = "Left hand" if hand.is_left else "Right hand"
#            print "  %s, id %d, position: %s" % (handType, hand.id, hand.palm_position)
            # Get the hand's normal vector and direction
#            normal = hand.palm_normal
            if hand.is_left:
               left_position = hand.palm_position
               left_grip_strength = hand.grab_strength
                
            else:
                right_position = hand.palm_position
                right_grip_strength = hand.grab_strength
       
        
        self.dmx_right.update_position(right_position)
        self.dmx_right.light_intensity(right_grip_strength)
        
#        self.dmx_left.update_position(left_position)
#        self.dmx_left.light_intensity(left_grip_strength)        
        
        #Get gestures
        for gesture in frame.gestures():

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
#                print   "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (gesture.id, self.state_names[gesture.state], swipe.position, swipe.direction, swipe.speed)
                if (swipe.direction[0]>0.8):
                    print "swipe right detected"
                    self.dmx_right.change_color()
#                    self.dmx_left.change_color()
                   
                elif(swipe.direction[0]<(-0.8)):
                    print "swipe left detected"
#                    self.dmx_right.change_color()

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""
            
    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a Leap Motion listener and controller
    leapDev = LeapListener()
    controller = Leap.Controller()

    # Have the Leap Motion listener receive events from the controller
    controller.add_listener(leapDev)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the listener when done
        controller.remove_listener(leapDev)

if __name__ == "__main__":
    main()