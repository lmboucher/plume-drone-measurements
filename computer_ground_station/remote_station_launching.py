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