import Leap, sys, thread, time
from Leap import SwipeGesture

class LeapListener(Leap.Listener):
    def on_init(self,controller):
        print 'LeapMotion initialized'

    def on_connect(self,controller):
        print 'Connected'
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self,controller):
        print 'LeapMotion disconnected'

    def on_exit(self,controller):
        print 'Exited LeapMotion acquisition loop.'

    def get_frame(self,controller):
        frame = controller.frame()
        return frame.hands, frame.gestures()


    
