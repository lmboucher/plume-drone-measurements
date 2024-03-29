package com.example.ground_station_final_application

import android.content.Context
import android.hardware.usb.UsbManager
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.ScrollView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.hoho.android.usbserial.driver.UsbSerialDriver
import com.hoho.android.usbserial.driver.UsbSerialPort
import com.hoho.android.usbserial.driver.UsbSerialProber
import com.hoho.android.usbserial.util.SerialInputOutputManager
import com.jjoe64.graphview.GraphView
import com.jjoe64.graphview.series.DataPoint
import com.jjoe64.graphview.series.LineGraphSeries
import java.io.BufferedWriter
import java.io.File
import java.io.FileWriter
import java.io.IOException
import java.math.BigDecimal
import java.nio.charset.Charset
import java.text.DecimalFormat


// private const val READ_TIMEOUT = 35 // 35 milliseconds timeout (we have every two seconds a new line arriving with at maximum 64 bytes to read)
private const val FILENAME = "received_data.txt"

// SerialInputOutputManager is a public class from the Usb Serial for Android library
// We start the interface Listener as we start our activity, takes care to open a Byte buffer with a size adapted to our data (64 bytes)
class MainActivity : AppCompatActivity(), SerialInputOutputManager.Listener {

    private lateinit var textView: TextView
    private lateinit var port: UsbSerialPort
    private lateinit var ioManager: SerialInputOutputManager
    private lateinit var scrollView: ScrollView
    private lateinit var editText: EditText
    private lateinit var graph: GraphView
    private var myIncr: Double = 0.0
    private var series = LineGraphSeries<DataPoint>(arrayOf<DataPoint>(DataPoint(0.0, 0.0)))

    // Declare a buffer to accumulate incoming data
    private var dataBuffer = StringBuilder()
    private var isAcquisitionRunning = false

    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // Initialization of the text of the upper layout
        textView = findViewById(R.id.textView)
        scrollView = findViewById(R.id.scrollView)
        editText = findViewById(R.id.sendCommand)
        graph = findViewById(R.id.graphView)

        val launch: Button = findViewById(R.id.read)
        val stop: Button = findViewById(R.id.write)
        val send: Button = findViewById(R.id.send)

        // If when we click on the "launch" button the acquisition has not started, it starts
        launch.setOnClickListener {
            if (!isAcquisitionRunning) {
                startDataAcquisition()
            }
        }

        // In case the acquisition is running and we want to stop it
        stop.setOnClickListener {
            if (isAcquisitionRunning) {
                stopDataAcquisition()
                isAcquisitionRunning = false
            }
        }

        send.setOnClickListener {
            val inputText = editText.text.toString()
            sendStringToPort(inputText)
        }
    }

    /**
     * Start the data receiving, printing, and storing.
     */
    private fun startDataAcquisition() {

        // Setting the USB manager
        val manager = getSystemService(Context.USB_SERVICE) as UsbManager

        // Open the port
        port = openPort(manager) ?: run {
            textView.append("Failed to open the USB serial port\n")
            // Scroll the ScrollView to the bottom
            scrollView.post {
                scrollView.fullScroll(ScrollView.FOCUS_DOWN)
            }
            return
        }

        // Now the acquisition starts
        isAcquisitionRunning = true
        textView.append("The acquisition is running\n")

        // Create SerialInputOutputManager and start it
        ioManager = SerialInputOutputManager(port, this)
        ioManager.start()
        textView.append("The input output manager has started\n")
    }

    /**
     * Private function only accessible via the MainActivity class.
     * It is opening the port. If no port is available it returns null.
     * Based on the README code in the GitHub from the library.
     *
     * @param manager of type UsbManager representing the USB manager needed to open the port
     * @return the port or null, depends if a device is available or not.
     */
    private fun openPort(manager: UsbManager): UsbSerialPort? {

        // Listing the available drivers
        val availableDrivers: List<UsbSerialDriver> =
            UsbSerialProber.getDefaultProber().findAllDrivers(manager)

        // checking it is not empty
        if (availableDrivers.isEmpty()) {
            textView.append("Empty\n")
            // Scroll the ScrollView to the bottom
            scrollView.post {
                scrollView.fullScroll(ScrollView.FOCUS_DOWN)
            }
            return null
        } else {
            textView.append("number of devices available : ${availableDrivers.size}\n")
            // Scroll the ScrollView to the bottom
            scrollView.post {
                scrollView.fullScroll(ScrollView.FOCUS_DOWN)
            }
            // Open a connection to the first available driver.
            val driver = availableDrivers[0]
            // Opening the connection
            val connection = manager.openDevice(driver.device)
            if (connection == null) {
                // Handle the case where the connection is null (permission not granted)
                return null
            } else {

                val port = driver.ports[0] // Most devices have just one port (port 0)

                // Set port parameters
                try {
                    port.open(connection)
                    port.setParameters(
                        57600,
                        UsbSerialPort.DATABITS_8,
                        UsbSerialPort.STOPBITS_1,
                        UsbSerialPort.PARITY_NONE
                    )
                } catch (e: IOException) {
                    // Handle IOException
                    return null
                }

                return port
            }
        }
    }

    /**
     * Stop the data receiving, printing, and storing
     */
    private fun stopDataAcquisition() {
        // We verify that the data are arriving and that the port exists
        if (::ioManager.isInitialized && ::port.isInitialized) {
            ioManager.stop()
        } else {
            textView.append("Data acquisition is not running\n")
            // Scroll the ScrollView to the bottom
            scrollView.post {
                scrollView.fullScroll(ScrollView.FOCUS_DOWN)
            }
        }
    }

    /**

     * We take and modify the function onDestroy from the SerialInputOutputManager interface.
     * This function is called when there is an IOException throwed (throwed by the functions of the library in case of error)
     *
     * Stops the process, close the port.
     */
    override fun onDestroy() {
        super.onDestroy()
        // Stop SerialInputOutputManager when activity is destroyed
        ioManager.stop()
    }

    /**
     * We take and modify the function onNewData from the SerialInputOutputManager interface.
     * This function is called when there is new data incoming or outgoing.
     *
     * @param data of type ByteArray is the data incoming
     * @return nothing but calls the writeDataToFile function which writes the decoded data to file
     */
    override fun onNewData(data: ByteArray) {

        // Convert the byte array to a string
        val receivedString = data.toString(Charset.defaultCharset())

        runOnUiThread {
            // Append the new data to the StringBuilder
            dataBuffer.append(receivedString)

            // Process complete lines in the buffer
            processBuffer()
        }
    }

    private fun processBuffer() {

        // Search for newline characters in the StringBuilder
        var newlineIndex = dataBuffer.indexOf("\n")

        // If a newline character is found, extract and process the line
        while (newlineIndex >= 0) {
            // Extract the line from the buffer
            val line = dataBuffer.substring(0, newlineIndex)

            // Process the line as needed
            processLine(line)

            // Remove the processed line (including the newline character) from the buffer
            dataBuffer.delete(0, newlineIndex + 1)

            // Search for the next newline character in the buffer
            newlineIndex = dataBuffer.indexOf("\n")
        }
    }

    private fun processLine(line: String) {

        textView.append(line + "\n")
        // Scroll the ScrollView to the bottom
        scrollView.post {
            scrollView.fullScroll(ScrollView.FOCUS_DOWN)
        }
        writeDataToFile(line)

        val columns = line.split(",").map { it.trim() }

        if (columns.size == 12) {

            val timeGPS = columns[0]
            textView.append("Time : " + timeGPS + "\n")
            // Scroll the ScrollView to the bottom
            scrollView.post {
                scrollView.fullScroll(ScrollView.FOCUS_DOWN)
            }
            val so2conc = columns[5]
            textView.append("SO2 concentration : " + so2conc + "\n")
            // Scroll the ScrollView to the bottom
            scrollView.post {
                scrollView.fullScroll(ScrollView.FOCUS_DOWN)
            }
            val co2conc = columns[7]
            textView.append("CO2 concentration : " + co2conc + "\n")
            // Scroll the ScrollView to the bottom
            scrollView.post {
                scrollView.fullScroll(ScrollView.FOCUS_DOWN)
            }
            try {

                myIncr = myIncr.inc().inc()
                val xvalue: Double = myIncr
                val yvalue: Double = convertToDouble(co2conc)

                series.appendData(DataPoint(xvalue, yvalue), false, 10)
                graph.addSeries(series)
                graph.viewport.isXAxisBoundsManual
                graph.viewport.setMaxX(xvalue)
                graph.viewport.setMinX(series.lowestValueX)

            } catch (e: Exception) {
                // Handle parsing errors
                textView.append("Unable to add the new points to the plot, abort plotting time " + timeGPS + "\n")
                // Scroll the ScrollView to the bottom
                scrollView.post {
                    scrollView.fullScroll(ScrollView.FOCUS_DOWN)
                }
                return
            }
        }
    }

    private fun convertToDouble(value: Any): Double {
        return when (value) {
            is BigDecimal -> {
                val formattedValue = DecimalFormat("#.######").format(value)
                formattedValue.toDouble()
            }
            is Float -> value.toDouble()
            is Double -> value
            is Int -> value.toDouble()
            is Long -> value.toDouble()
            is String -> value.toDouble()
            else -> 0.0
        }
    }

    /**
     * Function created privately in our class to write to a given file a given string.
     *
     * @param data of type String : what we want to store inside the file.
     * @return nothing but writes the String to the file
     */
    private fun writeDataToFile(data: String) {
        try {
            // Open the file in append mode
            val file = File("/storage/emulated/0/Documents/data/" + FILENAME)

            // FileWriter object writes characters to the specified file. true stands for appending at the end
            val fileWriter = FileWriter(file, true)
            // BufferedWriter wrapped around the fileWriter object, buffers the output to optimize the data writing to the file
            val bufferedWriter = BufferedWriter(fileWriter)

            // Append the received data followed by a newline character to the file
            bufferedWriter.write(data)
            bufferedWriter.newLine()

            // Close the BufferedWriter to flush the data and release resources
            bufferedWriter.close()
        } catch (e: IOException) {
            // Handle IO exception
            textView.append("Error occurred while appending data to file: ${e.message}\n")
            // Scroll the ScrollView to the bottom
            scrollView.post {
                scrollView.fullScroll(ScrollView.FOCUS_DOWN)
            }
        }
    }

    /**
     * We take and adapt the function onRunError from the SerialInputOutputManager interface.
     * This function is called when {@link SerialInputOutputManager#run()} aborts due to an error.
     * It takes care of closing the port.
     */
    override fun onRunError(e: Exception) {
        // Handle any errors that occur during data reading
        runOnUiThread {
            textView.append("Error occurred: ${e.message}\n")
            // Scroll the ScrollView to the bottom
            scrollView.post {
                scrollView.fullScroll(ScrollView.FOCUS_DOWN)
            }
        }
    }

    private fun sendStringToPort(inputText: String) {

        if (::port.isInitialized) {

            try {
                val data: ByteArray = (inputText + '\n').toByteArray()
                textView.append("send : " + inputText + "\n")
                // Scroll the ScrollView to the bottom
                scrollView.post {
                    scrollView.fullScroll(ScrollView.FOCUS_DOWN)
                }
                // Convert the string to bytes and send it through the port
                port.write(data, 2000)
            } catch (e: IOException) {
                // Handle the IOException
                textView.append("Error occurred while sending data: ${e.message}\n")
                // Scroll the ScrollView to the bottom
                scrollView.post {
                    scrollView.fullScroll(ScrollView.FOCUS_DOWN)
                }
            }

        } else {

            // Set the USB manager
            val manager = getSystemService(Context.USB_SERVICE) as UsbManager

            // Try to open the port
            port = openPort(manager) ?: run {
                textView.append("Failed to open the USB serial port\n")
                // Scroll the ScrollView to the bottom
                scrollView.post {
                    scrollView.fullScroll(ScrollView.FOCUS_DOWN)
                }
                return
            }
            // Port is opened now
            val data: ByteArray = (inputText + '\n').toByteArray()
            textView.append("send : " + inputText + "\n")
            // Scroll the ScrollView to the bottom
            scrollView.post {
                scrollView.fullScroll(ScrollView.FOCUS_DOWN)
            }
            // Convert the string to bytes and send it through the port
            port.write(data, 2000)

        }

        // Clear the line where the text is written
        editText.text.clear()

    }
}