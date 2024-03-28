"""
The goal of this programme is to listen to commands coming from the ground station continuously, in case there is any problem while
the remote is far away
"""
import serial
import os

serial_port_name_comm = '/dev/ttyUSB0'

def open_communication_port() :
    '''
        Open the serial port associated to the communication modem if this one is plugged in 
    '''
    
    #try to open, will work if the modem is plugged in
    try :
        #By default no parity, 8 data bits, 1 stop bit, so no need to set them
        comm_ser = serial.Serial(serial_port_name_comm, 57600)
        #I add the boolean plugged_in to set a condition "I send" / "I do not send" after in my functions
        return comm_ser
    
    except serial.SerialException : #The modem is not plugged in or the port is already being used
        print("can't open the communication port, please check the plug or the port name")

if __name__ == "__main__" :	

	comm_ser = open_communication_port()
	
	try :
		
		while True :
			
			line = comm_ser.readline().decode().strip()

			if line :
				
				print("received command", line)
				os.system(line)
				
	except KeyboardInterrupt :
		
		print("Keyboard was interrupted, exiting")
	
	finally :
		
		comm_ser.close()