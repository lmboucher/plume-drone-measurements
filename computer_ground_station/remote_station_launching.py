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

##
#This program is made to send a wanted command line to the remote station which
#will execute it. It can be made at whatever moment at an infinite number of times.
##

'''
Some imports
'''
import serial

'''
Some definitions
'''
#Enter here the port name of the modem on your computer
comm_port_name = '/dev/ttyUSB0'

'''
Main entry of the script
'''

if __name__ == "__main__" :
    
    #opening the communication port
    comm_ser = serial.Serial(comm_port_name, 57600)
    
    #asks the user which command to send
    command = input("Enter command : ")
    
    #send the command to the modem with a delimiter 
    comm_ser.write(command.encode())
    comm_ser.write(b'\n')
    
    comm_ser.close()
