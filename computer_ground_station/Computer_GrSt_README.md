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

# [First program]()

This program contains four parts

1. The import of the pip pyserial library
2. The parameters' setting
- The port name
- The document where to store the data with its path
3. The functions
- The first function is to open the port
- The second one is to acquire the data sent by the remote station
4. The main entry
- You need to make sure that you open the port before starting playing with the data.
- You need in the end to close the port otherwise it can be problematic if you relaunch the program.

# Second program

This program contains three parts

1. The import of the pip pyserial library
2. The port name setting
3. The main entry of the script where a command line is asked to the user and then sent to the remote station. As before, make sure you open the port with the correct baudrate and make sure you close it in the end.

# Third program

This one is the biggest. In my case, since the Raspberry is connected to both the multisensor board and the GPS module, the data incoming are lines like 
```
"GPS_time ,SensorInfo1 ,SensorInfo2 ,... , SensorInfoN ,GPS_lon ,GPS_lat, GPS_alt"
```
The sensor information are diverse, we have in the beginning temperature, humidity, pressure, and in the end gas concentrations. What this program does is to receive and store the data as before. However, it also permits to do a live plot of the different gas concentrations with the GPS time on the x-axis.

This program is divided in four parts as the first one.

1. The imports' part

As usual you need the pip pyserial library. In my case, since I want times on the x-axis, I need the datetime module (no installation needed it comes with you Python installation) and the matplotlib.dates module (installation with matplotlib `sudo apt install python3-matplotlib`). Numpy is used since I work with arrays for the plotting (install it with `sudo apt install python3-numpy`). Then other librairies from matplotlib are needed to do nice plots, but no more installations to do.

The other parts are very similar to the first program, more complex but with more comments
