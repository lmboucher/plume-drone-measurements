# Remote-Ground-station-setting-live-drone-measurements
This repository is aimed to contain information for :

1. The setting of a Raspberry Pi3b which is attached to a drone and forms what I call the remote station. Is is connected to three modules : a Neo6m GPS module, a tecnosense multisensor board, and a RFD868X-EU communication module. The remote station sends the data got with the different modules to a ground station every 2 seconds.
2. The setting of a computer to receive, store, and plot live the received data. The computer is also able to send information to the remote station. This forms the computer ground station.
3. The creation of an Android application to receive, store, and plot live the received data. The application is also able to send information to the remote station. This forms the Android ground station.

## Raspberry settings

You will find in this [directory](https://github.com/lmboucher/Remote-Ground-station-setting-live-drone-measurements/edit/main/remote_station/) two Python scripts.

1. One is to communicate with the different modules connected to the Raspberry and send the obtained data to the ground station ;
2. One is to receive Terminal command lines from the ground station and to executes them. It is mainly reboot and shutdown commands which are useful in this project.

For more details go to this [README file](https://github.com/lmboucher/Remote-Ground-station-setting-live-drone-measurements/edit/main/remote_station/RemSt_README.md)

## Computer ground station settings

I used Python 3.11.2 with Spyder (5th version). You will find in this [directory](https://github.com/lmboucher/Remote-Ground-station-setting-live-drone-measurements/blob/main/computer_ground_station/) three scripts :
1. One is to receive and store the data sent by the Raspberry ;
2. One is to send Terminal command lines to the Rasperry. In case our remote station has a problem while it is several kilometers away, we need to be able to relaunch it without getting it back to us. Drone batteries are heavy, expensive, and does not last that long ; 
3. One is still to receive and store the data sent by the Raspberry, but is moreover doing a live plot of some of the received data. Variations of some parameters are much easier to see with a plot.

For more details go to this [README file](https://github.com/lmboucher/Remote-Ground-station-setting-live-drone-measurements/blob/main/computer_ground_station/Computer_GrSt_README.md)

## Android ground station

I used Android Studio 2023.2.1.24 with Linux Debian 64 bits. My app is coded in Kotlin.

You will have more information in this [README file](https://github.com/lmboucher/Remote-Ground-station-setting-live-drone-measurements/blob/main/android_ground_station/Android_GrSt_README.md)
