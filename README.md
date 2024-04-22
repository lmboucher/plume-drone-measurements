# Remote-Ground-station-setting-live-drone-measurements
This repository contains information for :

1. The setting of a Raspberry Pi3b which is attached to a drone and to different modules. The whole forms what I call the remote station. The modules are : a Neo6m GPS module, a tecnosense multisensor board, a RFD868X-EU communication module, and a PMS5303 Plantower module. The PMS and the GPS can not be connected at the same time, they occupy the same position. The remote station sends the data got with the different modules to the ground station. The remote station is also capable of receiving information from the ground station and of interpreting it.
2. The setting of a computer ground station receiving, storing, and plotting live the received data when connected to the second RFD868X-EU communication module. The computer ground station also permits to send information to the remote station.
3. The setting of an Android ground station (Android application) receiving, storing, and plotting live the received data when installed on a device connected to the RFD868X-EU communication module. The application also permits to send information to the remote station.

## Raspberry settings

You will find in this [directory](https://github.com/lmboucher/plume-drone-measurements/tree/main/remote_station) all the necessary Python scripts, schemes, and .

For more details go to this [README file](https://github.com/lmboucher/plume-drone-measurements/blob/main/remote_station/RemSt_README.md)

## Computer ground station settings

I used Python 3.11.2 with Spyder (5th version). You will find in this [directory](https://github.com/lmboucher/plume-drone-measurements/tree/main/computer_ground_station) three scripts :
1. One is to receive and store the data sent by the remote station to the ground station ;
2. One is to send information to the remote station. The remote station interprets this information as a Terminal command line. In case our remote station has a problem while it is several kilometers away, we need to be able to relaunch it without getting it back to us (drone batteries are heavy, expensive, and does not last that long) ; 
3. One is still to receive and store the data sent by the remote station, but is moreover doing a live plot of some of the received data. Variations of some parameters are much easier to see with a plot.

For more details go to this [README file](https://github.com/lmboucher/plume-drone-measurements/blob/main/computer_ground_station/Computer_GrSt_README.md)

## Android ground station

I used Android Studio 2023.2.1.24 with Linux Debian 64 bits. My app is coded in Kotlin. 

This app is designed to print and plot the information sent by the remote station to the ground station. It permits also to send information to the remote station.

You will have more information in this [README file](https://github.com/lmboucher/plume-drone-measurements/blob/main/android_ground_station/Android_GrSt_README.md)
