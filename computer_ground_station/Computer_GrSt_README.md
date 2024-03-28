**This directory contains the information specific to the setting of the computer ground station.**

# Common prerequisits to all the programs

First you need Python.
Then you need to install the `pyserial` library. Install `pip` and then `pyserial`.
```
sudo apt install python3-pip
pip install pyserial
```
If you already have pip, pay attention not to install `serial` too or not to already have it. In your Terminal you can check for the pip librairies you have, then maybe uninstall `serial` and eventually maybe install `pyserial` if you don't already have it. Make sure you are not doing those commands as a superuser. 
```
pip list
pip uninstall serial
pip install pyserial
```
Also, you need to know which port is used by your computer : in your Terminal look at `ls /dev/`. Then plug in your communication module and do again `ls /dev/`. An additional port should be there on the second time use this one. On Linux you can safely do `ls /dev/ | grep tty` rather than just `ls /dev/`, it will be faster to see the new port.

# [First program](https://github.com/lmboucher/Remote-Ground-station-setting-live-drone-measurements/blob/main/computer_ground_station/ground_station_data_transmission.py)

This program aims to handle simply the communication with the Raspberry. As said in the MainREADME, the Raspberry (remote station ReSt) and the computer (ground station GrSt) are both connected to a RFD 868x - EU communication module via USB since the module is sold with a FTDI-USB cable. Data are sent by the remote station every two seconds. So every two seconds the information is received and stored by the ground station. This is what permits this first program. It contains four parts :

1. The import of the pip pyserial library
2. The parameters' setting
- The port name for the computer to know where to listen to the information
- The text file where to store the arriving data with its path
3. The functions
- The first function permits to open the port
- The second one permits to acquire and store the data sent by the remote station
4. The main entry
- You need to make sure that you open the port before starting playing with the data.
- You need in the end to close the port otherwise it can be problematic if you relaunch the program.

# [Second program](https://github.com/lmboucher/Remote-Ground-station-setting-live-drone-measurements/blob/main/computer_ground_station/remote_station_launching.py)

In this project, the remote station is remote since it is on a drone. So if there is any problem while the station is far away we need to be able to reboot the station without bringing it back (batteries are expensive and not lasting indefinitely). So this program permits to send Terminal command lines to the remote station which executes them. It contains three parts :

1. The import of the pip pyserial library
2. The port name setting to know where to go to listen to the data
3. The main entry of the script where a command line is asked to the user and then sent to the remote station. As before, make sure you open the port with the correct baudrate and make sure you close it in the end.

# [Third program](https://github.com/lmboucher/Remote-Ground-station-setting-live-drone-measurements/blob/main/computer_ground_station/ground_station_data_transmission_plots.py)

This program has the same aim than the first one : it receives and stores data. However, it has one more feature : it plots live some data... It is easier to visualize different variations with a plot than with written numbers. In my case, since the Raspberry is connected to both the multisensor board and the GPS module, the data incoming are Strings like 
```
"GPS_time ,SensorInfo1 ,SensorInfo2 ,... , SensorInfoN ,GPS_lon ,GPS_lat, GPS_alt \n"
```
The sensor information are diverse, we have in the beginning temperature, humidity, pressure, and in the end gas concentrations. The live plot is the one of some sensor information depending on GPS time. GPS time is like `"HH:MM:SS"`.

This program is divided in four parts as the first one.

1. The imports' part

As usual you need the pip pyserial library. In my case, since I want times on the x-axis, I need the datetime module (no installation needed it comes with your Python installation) and the matplotlib.dates module (installation with matplotlib `sudo apt install python3-matplotlib`). Numpy is used since I work with arrays for the plotting (install it with `sudo apt install python3-numpy`). Then other librairies from matplotlib are needed to do nice plots, but no more installations to do.

2. The parameters' setting

I would say that this is the most important part. Pay attention to it especially if you do not want to make the same plots as me. The comments should indicate what to fill and why.
