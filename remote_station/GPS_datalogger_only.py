Copyright [2024] lmboucher

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#--------------------
#SET THE PARAMETERS :
#--------------------

# Set the right serial port name for the Raspberry to look at the right place
serial_port_name_GPS = '/dev/ttyAMA0'
#file name where to save the received data from the GPS module
YOUR_PATH = "/home/blabla/blabla/..."
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
        
    data = gps_ser.readline() #reading the line sent by the GPS (can start by GGA or something else)
    start_by_GGA = False #I set this variable assuming the line we read was not starting by GGA
    
    while not start_by_GGA : #Until our line is not starting by GGA, we read another one
        
        if data.find(b'GGA') > 0 : #check for bytes-like objects starting by GGA
            msg = pynmea2.parse(data.decode()) #returns a sentence GGA(...) with the different GPS information
            start_by_GGA = True # To go out of the loop afterward
            #We get the different information, here very simply organized
            my_string = "{0}, {1} {2}, {3} {4}, {5} {6}\n".format(msg.timestamp, msg.latitude, msg.lat_dir, msg.longitude, msg.lon_dir, msg.altitude, msg.altitude_units)
            print_and_write(file, my_string) 
        
        else :
            data = gps_ser.readline()

#---------------------------
#ENTRY POINT OF THE SCRIPT :
#---------------------------

if __name__ == "__main__":
        
    gps_ser = serial.Serial(serial_port_name_GPS, baudrate, timeout=0.5)
    
    with open(log_file_name, 'a', encoding='utf-8') as my_file :
        
        while True :
            
            read_gps_info(gps_ser, my_file)
    
    gps_ser.close()
