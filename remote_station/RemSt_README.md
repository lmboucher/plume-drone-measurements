To set up your Raspberry, you  may use a HDMI-HDMI or HDMI-VGA cable which you plug in on one side to the Raspberry and on the other side to a monitor. Then, you plug in a keyboard via the USB port to be able to write command lines and programs. The mouse is optional since you can go into Terminal mode without it. You also need an alimentation ; you can buy the one from Raspberry or use an external battery or use a computer or a phone charger or ... 

# Raspberry setting for one module at a time

The goal of this part is to be able to receive, print, and save the data acquired by each of the modules connected to the Raspberry. Since we can not connect 2 modules by UART at the same time, in the end, two setups are configured :
1) The multisensor board (USB) + the communication module (USB) + the GPS module (UART)
2) The multisensor board (USB) + the communication module (USB) + the particulate matter module (UART) 

## Modules connected by UART

### Installations

1. Install Python on your Raspberry, the version must be at least 3.5. This tutorial is nice : [Python 3.9 installation on a Raspberry Pi](https://itheo.tech/install-python-39-on-raspberry-pi).

2. Install Crontab to be able to launch your programs when you boot the station. It is important since the station is remote. You don't want to bring the station back to shut on your programs if they failed.

3. Install pip with `sudo apt install python3-pip`

4. Make sure you do not have any conflicts between your librairies. Conflicts arrive notably when you install pip packages being a superuser, so pay attention to be superuser only for apt installations.

5.  Install pyserial (NOT serial otherwise you will have issues) `pip install pyserial`

6.  Install librairies to handle communication with the GPS module `sudo apt install gpsd gpsd-clients python3-gps minicom`

### Configuration files modifications

Now we need to modify some configuration files so files read by the Raspberry system when it boots.

1. Go to your `cmdline.txt` file : `sudo nano /boot/cmdline.txt` and replace the existing command by
```
dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles`
```

2. Go to your `config.txt` file : `sudo nano /boot/config.txt` and add to the end of it :
```
dtparam=spi=on
dtoverlay=pi3-disable-bt
core_freq=250
enable_uart=1
force_turbo=1
init_uart_baud=9600
```
3. Reboot the system to take into account the changes : `sudo reboot now`

### Communicate !

Now everything is ready to communicate with the modules ! 

Set the baudrate of the serial port associated to the GPS correctly : `stty -F /dev/ttyAMA0 9600`

Connect one of your module to your Raspberry like shown on this image :

![Image of the UART connexion to the Rasperry](https://github.com/lmboucher/plume-drone-measurements/blob/main/remote_station/Raspberry_schematics.png)

The first time, in order to see data incoming in the Terminal you can do those steps :

1. First kill all launched processes : `sudo killall gpsd`

2. Add the device to the gpsd tool : go to the file `sudo nano /etc/default/gpsd` and add your GPS serial port : `DEVICES = "/dev/ttyAMA0"`

3. Configure the socket in which the stream goes :
```
sudo systemctl enable gpsd.socket
sudo systemctl start gpsd.socket
cgps -s
```
4. For the GPS module, you need to put your Raspberry connected to it under a clear sky (not in a yard). You also need to wait at least 20 minutes to get a signal at first. For the PMS Plantower module it works in all environments.

I advise you after this first try to write a little program (mine is in Python) to read incoming data easily without having to do again all the steps from that part.

#### Specific to the Neo 6m - GPS module

The Neo 6m - global positionning system (GPS) module sends National Marine Electronics Association (NMEA) sentences. That means we don't need to read all of them, only those strating by "GGA" standing for "Global Positioning System Fix Data". Once spotted, you can decode the sentence and, here by using the `pynmea2` library, get the GPS information.

[Here](https://github.com/lmboucher/plume-drone-measurements/blob/main/remote_station/GPS_communication_only.py) is a little example of a Python script to communicate with your GPS module.

#### Specific to the PMS5303 Plantower module

The Plantower module sends information coded in bytes. So depending on the timeout you set, you will have more or less lines of `b''`. With a timeout of 0.2 seconds and staying in a not highly variable environment I typically get series like :
```
b''
b''
b''
b''
b'BM\x00\x1c\x00\x17\x00\x18\x00\x1b\x00\x14\x00\x18\x00\x1b\x11\xd0\x06o\x00/\x00\x00\x00\x00\x00\x00\x11\x00\x02\xd2'
```
Here the information is contained in the 5th line.

To decode that, the decode function of Python is not very efficient. The instrument documentation gives information about what the bytes correspond to. The two first characters : `B` and `M`, are fixed. Then, you have a succession of bytes you can interprete.

Bytes 3 and 4 : `\x00\x1c` give the frame length
Bytes 5 and 6 : `\x00\x17` give the value of the first data
...
Bytes 27 and 28 : `\x00\x00` give the value of the twelfth data
Bytes 29 and 30 : `\x11\x00` give the value of the "reserved" data
Bytes 31 and 32 : `\x02\xd2` give the check code

The documentation indicates that the number of information per second can vary depending of the measures made by the instrument. Due to that I set the timeout at the minimum to be sure to get all the sent information.

[Here](https://github.com/lmboucher/plume-drone-measurements/blob/main/remote_station/PMS_datalogger_only.py) is a little example of a Python script to communicate with your PMS5303 Plantower module.

## Modules connected by USB

### The transceiver modem

The communication module used here is a RFD 868x-EU device. Thanks to a USB-FTDI cable, it is plugged in the Raspberry via USB port.

The first and most important step is to determine in which serial port the information pass : look at your ports without plugging in the communication module by using `ls /dev/` in your Terminal. Then plug in the communication module and look at `ls /dev/` again. On Linux you can even safely add `| grep tty` at the end of the command. This time a port should have appeared. In my case it is sometimes `ttyACM0` and sometimes `ttyACM1` (but I have also the GPS module and the multisensor board connected). 

When you have the communication port name, you are ready to read and write information in the port. Use the serial library to open the port and write the information you wish in it. You would use in the beginning `my_port = serial.Serial(my_port_name_with_path, my_baudrate, my_timeout)`. The information transiting from one communication modem to another one must be encoded. So use `my_port.write(my_string.encode())`. By default `utf-8` encoding is used. When this is done it is over. The ground station has to take the flame.

### The tecnosense multisensor board

Here, the code is mostly inspired of the code given by the multisensor library.

# [Raspberry setting for three modules at a time (PMS5303, RFD 868x-EU module, and tecnosense multisensor board)](https://github.com/lmboucher/plume-drone-measurements/blob/main/remote_station/PMS_multigas_comm_datalogger.py)

In that program, as said in the title, three modules are connected to the Raspberry. The program is divided in 4 parts as usual. However, the third part, dedicated to the functions, is itself divided in 4 parts.

If you have the same installation than here, the program should work just by modifying the parameters in the beginning (first part and also the most important one). Then, again again, for the imports, check you have only the `pyserial` library installed and not the `serial` one. 

### The functions

1) In the Plantower module part, only one function is written. It permits to read the information sent by the device based on what explained before.

2) In the communication module part, the function is just to open correctly the port. As written before, the port name changes depending on the situation so it is better to dedicate a whole function to the opening. Also, I added the possibility of returning `None` in case the communication module is not plugged in.

3) In the multigas part, it is also just a function for the port opening. It is inspired by the original code given by the multisensor library.

4) The "whole" part is the biggest one. It contains four functions. The first function permits to print a given string in the terminal and to store the given string in a given document. The second function permits to create the header of your file. The third function permits to collect one data line with the data of the three modules. The fourth function permits to call the previous ones to record continuously.

# [Raspberry setting for three modules at a time (RFD 868x-EU module, Neo6mGPS, and tecnosense multisensor board)](https://github.com/lmboucher/plume-drone-measurements/blob/main/remote_station/GPS_multigas_comm_datalogger.py)

This program is similar to the previous one. Changes have been made to get in the end correctly one information per second and not one information every two seconds.

1) The first part is not dedicated to the Plantower module but to the GPS module. It contains three functions. The first one returns the latitude, longitude, and altitude sent by the GPS. The second function returns only the time given by the GPS. The third function yields in an array on one side the GPS time and on the other side the GPS latitude, longitude, and altitude. We don't decode information in the same way than with the Plantower module, we use the Pynmea2 library.

2) The second  part is still the same than previously.

3) The third part is a little bit modified ; there is still a function opening the port but also a function yielding one line of measurements taken by the sensors on the multisensor board.

4) This "whole" part is the same than before, however, now, in the function to get the modules data, print them, and log them, we just get what is yielded by the functions in parts 1) and 3). This permits to run the two acquisitions in parallel and not lose one second when running a process.
