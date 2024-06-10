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
#This program is only receiving data and storing them to the wanted text file.
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
#Enter here the path associated to the file where you want your received data to be written
my_result_file_path = '/home/lucie/ENS2/STAGE_NICOLOSI/tache_2/received_data.txt'

'''
Functions
'''
def open_serial_port() :
    '''
    Open the serial port of the modem attached to the ground station
    '''
    
    try :
        #It is like on the Raspberry, only need to precise the baud rate, the rest is by default
        comm_ser_gs = serial.Serial(comm_port_name, 57600)
        return comm_ser_gs
    
    except serial.SerialException :
        print("Impossible to open " + str(comm_port_name) + " abort the communication")
        return None

def acquire_sent_data(file, comm_ser_gs) :
    
    try :
        with file as my_file :
            while True : #While lines are received
                data = comm_ser_gs.readline().decode().strip()
                if data :
                    print(data)
                    my_file.write(data + '\n')
                    my_file.flush()
                        
    except KeyboardInterrupt :
        print('\nKeyboard interrupt detected. Stopping')
    
    except Exception as e :
        print(f"Error : {e}")

'''
Main entry of the program
'''
if __name__ == "__main__" :
        
    comm_ser_gs = open_serial_port()
    
    file = open(my_result_file_path, 'a+', encoding='utf-8') #Append to the file
    
    acquire_sent_data(file, comm_ser_gs)
    
    comm_ser_gs.close()
