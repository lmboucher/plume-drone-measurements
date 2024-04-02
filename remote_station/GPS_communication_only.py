#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:59:56 2024

@author: lucie
"""

#--------------------
#SET THE PARAMETERS :
#--------------------

# Set the right serial port name for the Raspberry to look at the right place
serial_port_name_GPS = '/dev/ttyAMA0'
#file name where to save the received data from the GPS module
YOUR_PATH = "home/blabla/blabla/..."
log_file_name = YOUR_PATH + "GPS_res.txt"
# Set the correct baudrate
baudrate = 9600

#---------
#IMPORTS :
#---------

import serial #make sure you installed only pyserial and not serial...
import pynmea2

#-----------
#FUNCTIONS :
#-----------

def print_and_write(file, string):
    '''
        Print string on screen and write it to file.
    '''

    print(string)
    string = string.replace('\x00', '')
    file.write(string)

def read_gps_info(gps_ser, file) :
    '''
    When this function is called, it returns the GPS position and time. One information is sent per second.
    We are interested in the NMEA messages starting by GGA.
    However, between one line starting with GGA and another one, other lines are sent by the GPS (we do not want them).
    Therefore, when we call this function, it returns the next line starting by GGA. There is a variable offset of some milliseconds 
    between the result and the moment the function is called.
    '''
    
    #necessary condition not to have issues, "with" ensures the serial port is closed after use
    with gps_ser as serialPort :
        
        data = serialPort.readline() #reading the line sent by the GPS (can start by GGA or something else)
        start_by_GGA = False #I set this variable assuming the line we read was not starting by GGA
        
        while not start_by_GGA : #Until our line is not starting by GGA, we read another one
            
            if data.find(b'GGA') > 0 : #check for bytes-like objects starting by GGA
                msg = pynmea2.parse(data.decode()) #returns a sentence GGA(...) with the different GPS information
                start_by_GGA = True # To go out of the loop afterward
                #We get the different information, here very simply organized
                my_string = "{0} {1}, {2} {3}, {4} {5}\n".format(msg.latitude, msg.lat_dir, msg.longitude, msg.lon_dir, msg.altitude, msg.altitude_units)
                print_and_write(file, my_string) 
            
            else :
                data = serialPort.readline()

#---------------------------
#ENTRY POINT OF THE SCRIPT :
#---------------------------

if __name__ == "__main__":
        
    gps_ser = serial.Serial(serial_port_name_GPS, baudrate, timeout=0.5)
    
    with open(log_file_name, 'a', encoding='utf-8') as my_file :
        
        while True :
            
            read_gps_info(gps_ser, my_file)