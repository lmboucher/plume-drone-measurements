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
#This program is designed to be launched on the ground station. It acquires and stores the 
#data sent by the remote station. Moreover, it plots live the gaz concentrations
#of your choice (given what is possible)

#Make sure to leave 1 minute after launching the remote station before launching this program
#since it will not plot the text file header.
#During this minute, you can use the program with only the transmission to check if it works.

#Make sure to change the parameters in the beginning to make them suitting you.
##

'''
Some imports
'''
import serial
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
import matplotlib.colors as mcolors

'''
Parameters you need to check
'''
#Enter here the port name of the modem on your computer
comm_port_name = '/dev/ttyUSB0'
#Port opening, make sure the baudrate is correct
comm_ser_gs = serial.Serial(comm_port_name, 57600)
#Enter here the path associated to the file where you want your received data to be written
my_result_file_path = '/home/lucie/ENS2/stage_nicolosi/tache_2/received_data.txt'
#Indicate here names for your AFE measurements, in the increasing AFE number
#WARNING : put all of them even if you don't want to plot all of them.
my_AFE = ['SO2 (ppm)', 'H2S (ppm)', 'CO2 (ppm)']
is_there_CO2_temps = True
#Number of sensors measuring concentrations and which you want to plot, here your number can
#be < len(my_AFE) if you don't want to plot everything you measure.
n_sensors = 3
#Indicate here on how much lines you want to to your plots (for 6 sensors, maybe better two or three lines)
#WARNING : n_sensors must be divisible by n_line_fig. It is a bit annoying
#if you want an impair number of plots but the advantage is that it takes your whole screen
n_line_fig = 3
n_col_fig = n_sensors // n_line_fig
#Indicate which colors you want for each graphic (basic ones or CSS4_COLORS ones)
yellowgreen = mcolors.CSS4_COLORS['yellowgreen']
lightseagreen = mcolors.CSS4_COLORS['lightseagreen']
darkred = mcolors.CSS4_COLORS['darkred']
palevioletred = mcolors.CSS4_COLORS['palevioletred']
violet = mcolors.CSS4_COLORS['plum']
salmon = mcolors.CSS4_COLORS['salmon']
my_colors = [yellowgreen, lightseagreen, violet]
#Indicate here the column numbers corresponding to the concentration measurements of the 
#AFE you want to see (make it correponds with the order above)
#Index 0 is your first column which corresponds to the GPS time
corresponding_AFE_columns = [5, 6, 7]
#Total number of columns in the data
if is_there_CO2_temps :
    n_col = len(my_AFE)+9
else :
    n_col = len(my_AFE)+9

#Enter here the number of points you want to plot at the same time
n_points_plotted = 20
#Enter here in milliseconds the refresh time of your plot (best is to make it coincide with the frequency at which data are sent by the Raspberry)
my_refresh_time = 2000
#To have a nice x-axis on the plot, set here the date of your measurements
my_year = 2024
my_month = 4
my_day = 8

'''
Functions
'''

def acquire_sent_data_plots():
    '''
        This function permits to read the data sent by the Raspberry.
        It also permits to store and yield the 50 last measurements made by 
    '''
    
    #Opening the file where to store the data on the ground station. With permits to close the file after use.
    with open(my_result_file_path, 'a+', encoding='utf-8') as file:
        
        count = 0 #Will be incremented, permits us to have the plotted number of data yielded at the same time
        data_to_send = [] #Stores the data to yield
        
        while True:  # While lines are received
        
            while count < n_points_plotted : #We add n_points_plotted lines to data_to_send
                
                line = comm_ser_gs.readline().decode().strip() #Reading and decoding the line received
                line = line.replace('\x00', '')
                
                if line:
                    
                    print(line)
                    file.write(line + '\n') #Storing all the lines in the results file of the ground station
                    file.flush()
                    split_line = line.split(" ,")
                    #To start the plotting we need to have a GPS time signal, so until we have this signal we just store the data
                    if split_line[0] != "None" :
                        data_to_send.append(split_line) #Adding the line to the data to yield
                        count += 1
            
            #Now the number of measures wanted has been received, data_to_send is converted to an array and yielded (returned but with continuing the script)
            data_to_send = np.array(data_to_send)
            yield data_to_send

            # Continue yielding data while receiving new lines and updating the data
            while True:
                
                line = comm_ser_gs.readline().decode().strip()
                line = line.replace('\x00', '')
                
                if line:
                    print(line)
                    file.write(line + '\n')
                    file.flush()
                    split_line = line.split(" ,")
                    #It is the same here, we don't send the data to the plotting function if there is no time signal
                    if split_line[0] != "None" :
                        new_data_point = np.array([split_line])
    
                        if len(new_data_point[0]) == n_col :
                            data_to_send = np.concatenate((data_to_send[1:], new_data_point), axis=0) #In the yielded data we add the last line received and remove the first one
                        
                        yield data_to_send

def plot_data(data):
    '''
        Function to plot the data live
    '''
    
    #Figure setting
    fig, axs = plt.subplots(n_line_fig, n_col_fig)
    
    #to be sure axs is indeed an array
    if n_line_fig == 1 :
        axs = np.array([axs])
    elif n_col_fig == 1 :
        axs = axs.reshape(-1, 1)
    
    #Initializing lines for the animation. 
    #As much lines as plots.
    lines = [[axs[i, j].plot([], [], color=my_colors[i * n_col_fig + j], label=my_AFE[i * n_col_fig + j])[0] for j in range(n_col_fig)] for i in range(n_line_fig)]
    
    #axs is a 2D array
    for ax_row in axs:
        for ax in ax_row:
            #Setting the legends (which gaz)
            ax.legend(loc='upper right')


    def animate(frame):
        '''
            Function eaten by FuncAnimation to have the refreshing with what interest us
        '''
        
        #We receive the next yielded data, so an array with n_points_plotted lists one after each other.
        #Each of these lists contain all the data sent by the Raspberry.
        try:
            data_point = next(data)   
        except StopIteration:
            return
        
        #We reshape the initial array to have n_points_plotted lines and as much columns as sent variables by the Raspberry
        data_point = np.reshape(data_point, (n_points_plotted, n_col))
        
        #Extracting the times as a datetime object with the wanted date.
        timestamps = []
        for ts in data_point[:, 0] :
            ts_int = datetime.datetime.strptime(ts, '%H:%M:%S')
            timestamps += [ts_int.replace(year=my_year, month=my_month, day=my_day, tzinfo=None)]
        
        #Extracting the concentrations of interest
        sensor_values = data_point[:, corresponding_AFE_columns].astype(float)
        
        #Updating lines and axs
        for i in range(n_line_fig):
            for j in range(n_col_fig):
                index = i * n_col_fig + j
                if index < n_sensors:
                    line = lines[i][j]
                    ax = axs[i, j]
                    #Make sure each figure has its own axis
                    ax.clear()
                    ax.plot(timestamps, sensor_values[:, index], color=my_colors[index], ls='--', marker='o')
                    ax.set_title("Live concentration of " + my_AFE[index] + " in the box-near atmosphere (50 last measurements)", fontsize=10)
                    ax.legend([line], [my_AFE[index]], loc='upper right')
                    ax.grid(color=my_colors[index], linestyle='-.', linewidth=0.3)
                    # ax.fill_between(timestamps, sensor_values[:, index], 0, facecolor=my_colors[index], alpha=0.2)
                    # Rotate and align the tick labels so they look better.
                    fig.autofmt_xdate()
                    # Design the x axis to show the times and not the date.
                    ax.fmt_xdata = mdates.DateFormatter('%H:%M:%S')
    
    #Animate
    ani = animation.FuncAnimation(fig, animate, interval=my_refresh_time)  # Refresh every 2000 milliseconds (2 seconds)
    
    #Show
    plt.show()

'''
Main entry of the script
'''
if __name__ == "__main__":
        
    # Start acquiring data
    data = acquire_sent_data_plots() #Acquiring data indefinitely

    while True : #make an infinite loop
            
        try :
            plot_data(data)
            
        except Exception :
            print("An error occured")
            plt.close()
            continue
        
        except KeyboardInterrupt :
            print("Keyboard has been interrupted, closing the program")
            break

    comm_ser_gs.close()
