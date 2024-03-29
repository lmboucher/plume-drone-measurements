To set up your Raspberry, you  may use a HDMI-HDMI or HDMI-VGA cable which you plug in on one side to the Raspberry and on the other side to a monitor. Then, you plug in a keyboard via the USB port to be able to write command lines and programs. The mouse is optional since you can go into Terminal mode without it. You also need an alimentation ; you can buy the one from Raspberry or use an external battery or use a computer or a phone charger or ... 

# Communication with the Neo 6m GPS module

The goal of this part is to be able to receive, print, and save the data acquired by the GPS module in the Raspberry.

## Installations

1. Install Python on your Raspberry, the version must be at least 3.5. This tutorial is nice : [Python 3.9 installation on a Raspberry Pi](https://itheo.tech/install-python-39-on-raspberry-pi).

2. Install pip with `sudo apt install python3-pip`

3. Make sure you do not have any conflicts between your librairies. Conflicts arrive notably when you install pip packages being a superuser, so pay attention to be superuser only for apt installations.

4.  Install pyserial (NOT serial otherwise you will have issues) `pip install pyserial`

5.  Install librairies to handle communication with the GPS module `sudo apt install gpsd gpsd-clients python3-gps minicom`

## Configuration files modifications

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

## Communicate !

Now everything is ready to communicate with the GPS module ! 

Set the baudrate of the serial port associated to the GPS correctly : `stty -F /dev/ttyAMA0 9600`

Connect your GPS module to your Raspberry :

SCHEMAAAAAAAAA

The first time, in order to see data incoming in the Terminal you can do those steps :

1. First kill all launched processes : `sudo killall gpsd`

2. Add the device to the gpsd tool : go to the file `sudo nano /etc/default/gpsd` and add your GPS serial port : `DEVICES = "/dev/ttyAMA0"

3. Configure the socket in which the stream goes :
```
sudo systemctl enable gpsd.socket
sudo systemctl start gpsd.socket
cgps -s
```
4. Put your Raspberry + GPS module under a clear sky (not in a yard) and wait at least 20 minutes to get a signal.

I advise you after this first try to write a little program (mine is in Python) to read incoming data easily without having to do again all the steps from that part.

## Create a program to communicate with the GPS module

PUT MY PROGRAM HERE

# Raspberry setting for the data transmission to another device

The communication module used here is a RFD 868x-EU device. Thanks to a USB-FTDI cable, it is plugged in the Raspberry via USB port.

The first and most important step is to determine in which serial port the information pass : look at your ports without plugging in the communication module by using `ls /dev/` in your Terminal. Then plug in the communication module and look at `ls /dev/` again. On Linux you can even safely add `| grep tty` at the end of the command. This time a port should have appeared. In my case it is sometimes `ttyACM0` and sometimes `ttyACM1` (but I have also the GPS module and the multisensor board connected).
