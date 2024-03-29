The developped application is doing the equivalent of my second and third programs on the computer ground station.

SCHÉMAAAAAAAAA

I use Android Studio on my computer (Linux Debian amd64). I dowloaded the version 2O23.2.1.24 for Linux 64 bits.

The first step is to install Android Studio. At first launch, I chose "do not import settings" and "standard setup", I was new to this app. Try to follow the "Hello World" course from the [Essentials](https://developer.android.com/codelabs/basic-android-kotlin-compose-first-app?hl=fr) . If when you launch a build you have `Error running "GreetingPreview" : /dev/kvm is not found` go to your BIOS (restart your computer and press without stopping the F2 key) and enable `Intel Virtualization Technology` (found in the `Configuration` menu on my computer).

Then, Android Studio is ready to create the ground station app. I use the [usb-serial-for-android library](https://github.com/mik3y/usb-serial-for-android).

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
3. Go to your `build.gradle.kts (Module:app)` file and add in the dependencies the usb-serial-for-android and graphView libraries :
```
dependencies {
    ...
    implementation("com.github.mik3y:usb-serial-for-android:3.7.0")
    implementation("com.jjoe64:graphview:4.2.2")
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
6. Add in your `gradle.properties` file
```
android.useAndroidX=true #May already be here
android.enableJetifier=true
``` 
7. Now implement the code in `app/kotlin+java/com.example.YOUR_APP_NAME/MainActivity` and set you res xml files as you wish.
