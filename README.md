# Remote-Ground-station-setting-live-drone-measurements
This repository is aimed to contain information for :

- The setting of a Raspberry Pi3b
- The setting of a Neo6m GPS module on the Raspberry
- The setting of a tecnosense Multisensor board on the Raspberry
- The setting of a RFD 868x communication module on the Raspberry to send and receive information to a ground station
- The setting of a computer for receiving, sending, and plotting live the information sent by the Raspberry via a RFD 868x module
- The creation of an Android application for receiving, sending, and plotting live information sent by the Raspberry via a RFD 868x module

## Raspberry settings

To set up your Raspberry, you  may use a HDMI-HDMI or HDMI-VGA cable which you plug in on one side to the Raspberry and on the other side to a monitor. Then, you plug in a keyboard via the USB port to be able to write command lines and programs. The mouse is optional since you can go into Terminal mode without it.

### Communication with the Neo 6m GPS module

The goal of this part is to be able to receive, print, and save the data acquired by the GPS module in the Raspberry.

#### Installations

1. Install Python on your Raspberry, the version must be at least 3.5. This tutorial is nice : [Python 3.9 installation on a Raspberry Pi](https://itheo.tech/install-python-39-on-raspberry-pi).

2. Install pip with `sudo apt install python3-pip`

3. Make sure you do not have any conflicts between your librairies. Conflicts arrive notably when you install pip packages being a superuser, so pay attention to be superuser only for apt installations.

4.  Install pyserial (NOT serial otherwise you will have issues) `pip install pyserial`

5.  Install librairies to handle communication with the GPS module `sudo apt install gpsd gpsd-clients python3-gps minicom`

#### Configuration files modifications

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

#### Communicate !

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

I advise you after this first try to write a little program (mine is in Python) to read incoming data easily without having to do again all those last steps.

#### Create a program to communicate with the GPS module

PUT MY PROGRAM HERE

### Raspberry setting for the data transmission to another device

The communication module used here is a RFD 868x-EU device. Thanks to a USB-FTDI cable, it is plugged in the Raspberry via USB port.

The first and most important step is to determine in which serial port the information pass : look at your ports without plug in the communication module `ls /dev/`, now plug in the communication module and look at `ls /dev/` again. On Linux you can even safely add `| grep tty` at the end of those two commands. This time a port should have appeared. In my case it is sometimes `ttyACM0` and sometimes `ttyACM1` (I have also the GPS module connected).

## Ground station settings

I use two options for my ground station receiving data from the remote station : the Raspberry and its modules. The first is using my computer and the second is to use an Android tablet (much more practical for field work).

### Computer ground station

I used Python 3.11.2 with Spyder (5th version). I wrote three programs :
- One is designed to send Terminal command lines to the Rasperry
- One is designed to receive data from the remote station
- One is designed to receive data from the remote station and to plot the different concentrations measured by the multisensor board with the time as the x-axis.

#### Installations

For the communication with the remote station (the receiving and sending of data) you will need to install the `pyserial` library. So first you need to install pip.
```
sudo apt install python3-pip
```
When you have pip, pay attention not to install `serial` too or not to already have it. In your Terminal you can check for the pip librairies you have, then maybe uninstall `serial` and eventually maybe install `pyserial` if you don't already have it. Make sure you are not doing those commands as a superuser. 
```
pip list
pip uninstall serial
pip install pyserial
```
Some more librairies are needed if you want to do the plotting of the received data, especially if you want to do the live plot with datetime objects on the x-axis.

#### Programming

The first step is to find which port is used by your computer, like the Raspberry before. Connect your communication device to your computer and see `ls /dev/` in your Terminal. Then do it again without plugging in your communication module. There should be a port appearing on the first try and not on the second, that's this one you will need to use.

### Android ground station

SCHÉMAAAAAAAAA

I use Android Studio on my computer (Linux Debian amd64) PRECISE THE VERSIONNNN OF ANDROID STUDIO

The first step is to install Android Studio. At first launch, I chose "do not import settings" and "standard setup", I was new to this app. Try to follow the "Hello World" course from the [Essentials](https://developer.android.com/codelabs/basic-android-kotlin-compose-first-app?hl=fr) . If when you launch a build you have `Error running "GreetingPreview" : /dev/kvm is not found` go to your BIOS (restart your computer and press without stopping the F2 key) and enable `Intel Virtualization Technology` (found in the `Configuration` menu on my computer).

Then, Android Studio is ready to create the ground station app. I use the [usb-serial-for-android library](https://github.com/mik3y/usb-serial-for-android). Steps 2. to ... are taken from Kai Morich's README.md file.

1. Create a new project on Android Studio, choose the option "Empty Views Activity"
2. Go to your `settings.gradle.kts` file and add the line `maven(url = "https://jitpack.io")` like :
```
dependencyResolutionManagement {
    ...
    repositories {
        ...
        maven(url = "https://jitpack.io")
    }
}
```
3. Go to your `build.gradle.kts (Module:app)` file and add in the dependencies the usb-serial-for-android library :
```
dependencies {
    ...
    implementation("com.github.mik3y:usb-serial-for-android:3.7.0")
    ...
}
```
4. To notify the app when a device is attached, add LINK TO THE FILE in your `app/kotlin+java/res/xml/' directory.
5. Configure the presence of that file in your `AndroidManifest.xml` found in your `app/mannifests/` directory :
```
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <application
        ...        
        <activity
            ...
            <intent-filter>
                ...
                <action android:name="android.hardware.usb.action.USB_DEVICE_ATTACHED" />
            </intent-filter>
            <meta-data
                android:name="android.hardware.usb.action.USB_DEVICE_ATTACHED"
                android:resource="@xml/device_filter" />
        </activity>
    </application>
</manifest>
```
6. Now implement the code in `app/kotlin+java/com.example.YOUR_APP_NAME/MainActivity`
