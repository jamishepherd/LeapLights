# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 16:49:27 2015

@author: Thomas Haase
"""
import pysimpledmx

class DMX_Controller():
    def __init__(self, usb_port,start_port,start_color,inverted):
        self.dmx_com = pysimpledmx.DMXConnection(usb_port)
        self.x_channel = start_port
        self.y_channel = start_port+1
        self.color_channel = start_port+2
        self.dimmer_channel = start_port+5        
        self.color_table = [10,20,35,50,65,80,95,110,125] 
        self.color_index = start_color        
        self.invert = inverted        
        
        self.dmx_com.setChannel(self.x_channel,128)
        self.dmx_com.setChannel(self.y_channel,128)
        self.dmx_com.setChannel(self.color_channel,self.color_table[self.color_index])
        self.dmx_com.setChannel(start_port+3,5) #Open gobo
        self.dmx_com.setChannel(start_port+4,10) #Open Shutter
        self.dmx_com.setChannel(self.dimmer_channel,255)        
        
        self.dmx_com.render()
    def update_position(self,position_data):
        hand_position = [position_data[0],position_data[1]]

        if (abs(hand_position[0])>255):
            if (hand_position[0]<-255):
                hand_position[0] = -255
            else:
                hand_position[0] = 255
       
        if (hand_position[1]<70):
            hand_position[1] = 70
        elif (hand_position[1]>402):
            hand_position[1] = 402
        
        hand_position[0] = hand_position[0] + 255
        hand_position[0] = int(hand_position[0]/2.0)
        
        hand_position[1] = hand_position[1] - 70 
        hand_position[1] = hand_position[1]*0.766
        hand_position[1] = int((1 - hand_position[1]/255)*255)
        
        if self.invert:
            hand_position[0] = 255 - hand_position[0]
            hand_position[1] = 255- hand_position[1]
        self.dmx_com.setChannel(self.x_channel,hand_position[0])
        self.dmx_com.render()
        self.dmx_com.setChannel(self.y_channel,hand_position[1])
        self.dmx_com.render()
       
    def change_color(self):
        self.color_index = self.color_index+1
        if (self.color_index > 8):
            self.color_index = 0
        self.dmx_com.setChannel(self.color_channel,self.color_table[self.color_index])
        self.dmx_com.render()
        print "color changed"   
        
    def light_intensity(self,grip_strength):
        dimmer_value = int((1-grip_strength)*255)
        self.dmx_com.setChannel(self.dimmer_channel,dimmer_value)
        self.dmx_com.render()
#        print dimmer_value
        
def get_coords(lpos,rpos):
    print lpos, rpos   

     
