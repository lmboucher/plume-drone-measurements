# Remote-Ground-station-setting-live-drone-measurements
This repository is aimed to contain information for :

- The setting of a Raspberry Pi3b
- The setting of a Neo6m GPS module on the Raspberry
- The setting of a tecnosense Multisensor board on the Raspberry
- The setting of a RFD 868x communication module on the Raspberry to send and receive information to a ground station
- The setting of a computer for receiving, sending, and plotting live the information sent by the Raspberry via a RFD 868x module
- The creation of an Android application for receiving, sending, and plotting live information sent by the Raspberry via a RFD 868x module

# Android application for communication with the Raspberry

SCHÉMAAAAAAAAA

I use Android Studio on my computer (Linux Debian amd64).

The first step is to install Android Studio. At first launch, I chose "do not import settings" and "standard setup", I was new to this app. Try to follow the "Hello World" course from the (https://developer.android.com/codelabs/basic-android-kotlin-compose-first-app?hl=fr "Essentials") . If when you launch a build you have "Error running "GreetingPreview" : /dev/kvm is not found" go to your bios (restart your computer and press without stopping the F2 key) and enable "Intel Virtualization Technology" (found in the "Configuration" menu on my computer).

Then, I created my app for my ground station. I use the (https://github.com/mik3y/usb-serial-for-android "usb-serial-for-android library").

1. Create a new project on Android Studio :
