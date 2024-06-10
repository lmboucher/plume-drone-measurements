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

# The goal of this file is to write the gps data in the file risultati.txt
# along the multisensor results. This code would be launched automatically

#File in which gps results will be written
file_name = "/home/tecnosense/sergio_board_test/first_try.txt"
#Variable for the PC system, ignored by the Raspberry (can be obtained with something like cat /dev/serial0 I believe)
serial_port_name = '/dev/ttyAMA0'

##
#IMPORTS
##

import serial #Pyserial, check you have only this one in your pip list
import pynmea2
from datetime import datetime as dt
import os #to do some shell in the Python code

##
#FUNCTIONS
##

def print_and_write(string, my_file) :
	print(string)
	my_file.write(string + '\n')
	
def read_PM_data(pm_port) :
	
	with open(file_name, 'a', encoding="utf-8") as my_file :	
		
		current_data = pm_port.readline()
		#print(current_data)
		if current_data.startswith(b'BM') :
			"""
			print(current_data)
			charac1 = current_data[0]
			print(charac1)
			charac2 = current_data[1]
			print(charac2)
			frame_length = int.from_bytes(current_data[2:4], byteorder='big')
			print(frame_length)
			"""
			print_and_write('\n', my_file)
			time_now = dt.now()
			my_time = time_now.strftime("%H:%M:%S")
			print_and_write(my_time, my_file)
			data1 = int.from_bytes(current_data[4:6], byteorder='big')
			print_and_write("pm1= " + str(data1) + " microg/m3", my_file)
			data2 = int.from_bytes(current_data[6:8], byteorder='big')
			print_and_write("pm2.5= " + str(data2) + " microg/m3", my_file)
			data3 = int.from_bytes(current_data[8:10], byteorder='big')
			print_and_write("pm10= " + str(data3) + " microg/m3", my_file)
			data4 = int.from_bytes(current_data[10:12], byteorder='big')
			print_and_write("apm1= " + str(data4) + " microg/m3", my_file)
			data5 = int.from_bytes(current_data[12:14], byteorder='big')
			print_and_write("apm2.5= " + str(data5) + " microg/m3", my_file)
			data6 = int.from_bytes(current_data[14:16], byteorder='big')
			print_and_write("conc_unit= " + str(data6) + " microg/m3", my_file)
			data7 = int.from_bytes(current_data[16:18], byteorder='big')
			print_and_write("d>0.3microm= " + str(data7) + " in 0.1L of air", my_file)
			data8 = int.from_bytes(current_data[18:20], byteorder='big')
			print_and_write("d>0.5microm= " + str(data8) + " in 0.1L of air", my_file)
			data9 = int.from_bytes(current_data[20:22], byteorder='big')
			print_and_write("d>1microm= " + str(data9) + " in 0.1L of air", my_file)
			data10 = int.from_bytes(current_data[22:24], byteorder='big')
			print_and_write("d>2.5microm= " + str(data10) + " in 0.1L of air", my_file)
			data11 = int.from_bytes(current_data[24:26], byteorder='big')
			print_and_write("d>5.0microm= " + str(data11) + " in 0.1L of air", my_file)
			data12 = int.from_bytes(current_data[26:28], byteorder='big')
			print_and_write("d>10microm= " + str(data12) + " in 0.1L of air", my_file)
			"""
			data13 = int.from_bytes(current_data[28:30], byteorder='big')
			print(data13)
			data_check = int.from_bytes(current_data[30:32], byteorder='big')
			print(data_check)
			"""

##
#ENTRY POINT OF THE SCRIPT
##

if __name__ == "__main__" :
	
	pm_port = serial.Serial(serial_port_name, 9600, timeout=0.2) #Pyserial library, opens the port serial_port_name

	
	while True :
		
		try :

			read_PM_data(pm_port)
		
		except KeyboardInterrupt :
			
			print("Keyboard was interrupted, closing the port")
			
			pm_port.close()
