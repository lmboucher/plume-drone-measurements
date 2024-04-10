'''
This file is the same as sensor_datalogger.py, but with more comments, with more organization, 
and a nicer text file in the end.
'''

#---------------------
#SET THE SYSTEM TYPE :
#---------------------

#This variable is set because the UART is handled in a little different way. The code can adapt itslef reading this variable
#1= PC
#2= raspberry
system=1
#the variable is used only for PC system. For raspberry this variable will be ignroed
serial_port_names_sensor = ['/dev/ttyACM0', '/dev/ttyACM1']
serial_port_name_GPS = '/dev/ttyAMA0'
serial_port_name_comm = '/dev/ttyUSB0'
#set the MODBUS address of the board, it is configured using the dip switch on the board
multisensor_address = 0x2
#force a new scan. You can set this variable to 1 if a new AFE scan is required after the sturtup (discouraged)
force_new_scan=0
#loop time in seconds
loop_time=1
#number of interactions. Set -1 to infinite loop. Use the STOP to abort
number_of_points=-1
#file name where to save the data log
log_file_name="/home/tecnosense/lucie_board_test/data_risultati.txt"
#The user may decided to user the custom configuration sets. This set of parameters allow to redefine some of the
#factory data. Set 1 to use this feature and fill the list below putting 1 on the AFE position you would like to
#use the custom calibration data.

# se change_calibration e' impostato a 1, la calibrazione di ogni AFE verra' reimpostata o a 0 (FABRICA) o a 1 (UTENTE)
change_calibration = 0
#if enable =1 insert here the AFE you need to use the custom configuration. AFE from 1 to 6. value1==ON, value0==OFF
# 4,5,6 lato GPIO 1,2,3 lato connettore nero
afe_custom_calibration = [0, 0, 0, 0, 0, 0]
only_log = 0


#---------
#IMPORTS :
#---------

import serial #be careful, pyserial library from pip to install, and not serial
import struct
import time
import datetime
import string
import multisensor
import os
import pynmea2 #for the GPS module NMEA message parsing


#-----------
#FUNCTIONS :
#-----------

'''
GPS
'''

def read_gps_info(gps_ser) :
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
                msg = pynmea2.parse(data.decode()) #returns a sentence GGA(...) with different information that we take and structure on next line
                start_by_GGA = True #won't go in the loop again
                return " ,{0} {1} ,{2} {3} ,{4} {5}\n".format(msg.latitude, msg.lat_dir, msg.longitude, msg.lon_dir, msg.altitude, msg.altitude_units)
            
            else :
                data = serialPort.readline()

def read_gps_timestamp(gps_ser) :
    '''
    read the current timestamp from the GPS
    '''
    with gps_ser as ser :

        #reads the line sent by the GPS
        data = ser.readline()
        #We assume that the read line does not start by GGA (otherwise we are really lucky, it is required to be able to parse)
        start_by_GGA = False
        #This loop will continue indefinitely as the read line can not be parsed
        
        while not start_by_GGA :
            
            if data.find(b'GGA') > 0 : #We check if the line starts by GGA to parse it
                msg = pynmea2.parse(data.decode())
                start_by_GGA = True
                
                if msg.timestamp == None :
                    return None
                
                else :
                    return msg.timestamp.replace(microsecond=0, tzinfo=None)
            
            else : #If we can't parse it we read another line and test it
                data = ser.readline()
    
    
'''
Transmission
'''

def open_communication_port() :
    '''
        Open the serial port associated to the communication modem if this one is plugged in 
    '''
    
    #try to open, will work if the modem is plugged in
    try :
        #By default no parity, 8 data bits, 1 stop bit, so no need to set them
        comm_ser = serial.Serial(serial_port_name_comm, 57600)
        #I add the boolean plugged_in to set a condition "I send" / "I do not send" after in my functions
        plugged_in = True
        return plugged_in, comm_ser
    
    except serial.SerialException : #The modem is not plugged in
        plugged_in = False
        return plugged_in, None
        
'''
Multigas
'''

def open_sensor_port():
    '''
        Open the right serial port and return it.
    '''

    if system==1:
        
        for port_name in serial_port_names_sensor : #Iterate over the possible port names
            
            try : #attempt to open the serial port
                ser = serial.Serial(baudrate=115200,timeout=0.1)
                ser.port = port_name
                ser.open()
                print("Successfully connected to " + str(port_name))
                return ser
                
            except serial.SerialException : #We try to connect to the next port
                print("Failed to connect to " + str(port_name))
                
        return None #If no valid port has been found
        
    else:
        
        ser = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=0.1)
        print("Successfully connected to /dev/ttyS0")
        return ser

'''
Whole
'''

def print_and_write(file, string):
    '''
        Print string on screen and write it to file.
    '''

    print(string)
    string = string.replace('\x00', '')
    if plugged_in :
        comm_ser.write(string.encode())
    file.write(string)


def get_board_info(ser, file):
    '''
        Get board info (serial number, connected AFE...) and write it to a file.
        Information on the top of the file risultati.txt
    '''

    # stop previous measurements loop 
    multisensor.write_MEASURE_CYCLE(system, ser, multisensor_address,0)
    time.sleep(0.1)    

    if force_new_scan==1:
        multisensor.write_SCAN_AFE(system, ser, multisensor_address) #force the initialization routine
        #add a sleep time to let the multisensor to scan the AFE
        time.sleep(0.5)

    print_and_write(file, "######################## BOARD INFO ########################\n")

    #for printing line 2
    board_version = multisensor.read_COMPILER_DATE_TIME(system, ser, multisensor_address).decode("utf-8") #get what should be printed
    print_and_write(file, "Multisensor version: {0}\n".format(board_version)) #print it

    #for printing line 3
    board_SN=multisensor.read_SERIAL_NUMBER(system, ser, multisensor_address) #get what should be printed
    print_and_write(file, "Multisensor SN (HEX): {0}\n".format(board_SN.hex())) #print it

    # if the result (the initialization routine) is not ready, try again 10 times
    for i in range(10):
        multisensor_ready = multisensor.read_READY(system, ser, multisensor_address)

        # if the sensor is ready, exit this loop
        if multisensor_ready[0] == 1:
            break

        # if the sensor is not ready, retry
        print("Sensor not ready, retrying...\nReturned read_READY value:", multisensor_ready)
        time.sleep(0.5)

    # number_of_measurements is the number of different measurements that the board can provide, line 4
    number_of_measurements = multisensor.read_NUMBER_OF_MEASUREMENTS(system, ser, multisensor_address)
    number_of_measurements = int.from_bytes(number_of_measurements, byteorder='big', signed=False)
    print_and_write(file, "Total number of available measures: {0}\n".format(number_of_measurements))

    #measurement_table_header = "System Time\t"
    measurement_table_header = "GPS Time "
    afe_details_string = ""

    prev_afen = 0
    for i in range (1, number_of_measurements+1):
        measurements_name = multisensor.read_MEASUREMENTS_NAME(system, ser, multisensor_address,i)
        afe_n = measurements_name[0]
        # print(f'reading afen {afe_n}')
        afe_name = ""
        afe_descr = measurements_name[1:15].decode("utf-8")

        # if onboard sensor
        if afe_n == 0x0B:
            afe_name = "OnBoard"

        # if AFE
        else:
            afe_name = "AFE {}".format(afe_n)

            if prev_afen != afe_n:
                #update the prev_afen value
                prev_afen = afe_n
                afe_details = multisensor.read_AFE_CONF_SN_VERSION_MODEL (system, ser, multisensor_address, afe_n)
                afe_sn = afe_details[0:20].decode("utf-8")
                afe_version = afe_details[20:35].decode("utf-8")
                afe_model = afe_details[35:45].decode("utf-8")

                afe_details_string += "{0}: SN={1}, version={2}, model={3}\n".format(afe_name, afe_sn, afe_version, afe_model)

                #check if user requested to enable the custom configuration for this AFE
                afe_has_custom_calibration = afe_custom_calibration[afe_n - 1]
                if change_calibration:
                    print_and_write(file, f'custom calibration for afen {afe_n} flag is {afe_has_custom_calibration}')
                    multisensor.write_AFE_EN_CUSTOM (system, ser, multisensor_address, afe_n, afe_has_custom_calibration)
                    multisensor.write_SCAN_AFE(system, ser, multisensor_address)
                    #add a sleep time to let the multisensor to scan the AFE
                    time.sleep(0.5)
                    tmp=multisensor.read_MEASUREMENTS_NAME(system, ser, multisensor_address,i)

        afe_string = "{0}.\t{1}\t{2}\n".format(i, afe_name, afe_descr)
        column_name = "{0} {1}".format(afe_name, afe_descr)
        measurement_table_header += "," + column_name
        print_and_write(file, afe_string)

    print_and_write(file, "AFE details:\n")
    print_and_write(file, afe_details_string)

    # stop measuring loop
    multisensor.write_MEASURE_CYCLE(system, ser, multisensor_address,0)
    time.sleep(0.1)

    print_and_write(file, "######################## END BOARD INFO ########################\n")
    file.flush()

    #Adding to the measurememt table header the GPS information
    GPS_columns = ["GPS latitude", "GPS longitude", "GPS altitude"]
    
    for i in range(len(GPS_columns)) :
        #little conditions to ensure having the same delimiter everywhere
        if i == 0 :
            measurement_table_header += "," + GPS_columns[i]
        else :
            measurement_table_header += " ," + GPS_columns[i]

    return number_of_measurements, measurement_table_header


def write_single_measurement(gps_ser, sensor_ser, first_iteration, measure_number) :
    '''
    Write to file a single measurement from the sensors on the board
    '''
    
    #pool the update register. The result is 1 if a new data is available on the board
    data = multisensor.read_UPDATE(system, sensor_ser, multisensor_address)
    
    #no new data, continue with the next iteration
    if (data[0] != 1) :
        return
    
    #read the byte array that contains a 32bits integer timestamp and a sequence of
    #32 bits floating point numbers with the measures, following the order given in
    #the header
    data = multisensor.read_MEASUREMENTS(system, sensor_ser, multisensor_address)
    
    #Adding GPS time column
    current_time = read_gps_timestamp(gps_ser)
    table_line = str(current_time)
    
    #scan the string to read the block of 4 bytes and format them in a floating point number
    for i in range (1, measure_number+1):
        offset = 4*(i-1)+4
        measured_value = bytes(data[offset : (offset+4)])
        # unpack the 4 bytes as float number and force big-endian
        [measured_value] = struct.unpack('>f', measured_value)
        #Adding sensor columns
        table_line += " ,{:.4E}".format(measured_value) #To separe columns with a " ,"
    
    #Adding GPS latitude, longitude, and altitude columns
    table_line += read_gps_info(gps_ser)
    
    print_and_write(file, table_line + "\n")
    
    #flush file to make sure the line with the gas sensors measurement is saved
    file.flush()    

def write_board_measurements(sensor_ser, gps_ser, number_of_measurements, measurements_table_header, file) :
    '''
    Continuously write to file measurements from sensors on the board
    '''
    
    #-------------------------------------------MODBUS_STATE_REGISTER_MEASURE_CYCLE
    multisensor.write_MEASURE_CYCLE(system, sensor_ser, multisensor_address, loop_time)
    current_time = read_gps_timestamp(gps_ser)
    current_time = "Start time stamp: {}\n".format(current_time)
    print_and_write(file, current_time) #line 18
    print_and_write(file, measurements_table_header + "\n") #line 19
    
    #flush file to make sure the header is saved
    file.flush()
    first_iteration = True
    
    try :
        if number_of_points == -1 :
            while (True) :
                write_single_measurement(gps_ser=gps_ser, sensor_ser=sensor_ser, first_iteration=first_iteration, measure_number=number_of_measurements)
                first_iteration = False
        else :
            for j in range(number_of_points) :
                write_single_measurement(gps_ser=gps_ser, sensor_ser=sensor_ser, first_iteration=first_iteration, measure_number=number_of_measurements)
                first_iteration = False
    except Exception as err :
        print(f'Error during measurement loop: {err}')
        
        #Try to stop the measurement cycle
        multisensor.write_MEASURE_CYCLE(system, sensor_ser, multisensor_address, 0)
    
    finally :
        sensor_ser.close()
        gps_ser.close()
        if plugged_in :
            comm_ser.close()
            plugged_in = False
            
        if sensor_ser.open() or gps_ser.open() or plugged_in :
            print("One serial port is still open")
        else :
            print("Serial ports closed")
        
        file.close()
    

#---------------------------
#ENTRY POINT OF THE SCRIPT :
#---------------------------

if __name__ == "__main__":
    
    sensor_ser = open_sensor_port()
    
    gps_ser = serial.Serial(serial_port_name_GPS, 9600, timeout=0.5)
    
    plugged_in = open_communication_port()[0]
       
    comm_ser = open_communication_port()[1]

    file = open(log_file_name, 'a', encoding='utf-8')

    number_of_measurements, measurements_table_header = get_board_info(sensor_ser, file)

    write_board_measurements(sensor_ser, gps_ser, number_of_measurements, measurements_table_header, file)
