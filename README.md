# Arduino Live Data Feed 

## Overview

This project consists of two main components: a Python script (`DAS.py`) and an Arduino script (`UltrasonicSensor.ino`). The project aims to monitor and display live altitude data from an Arduino board using a web-based dashboard.

## Components

1. **Python Script (`DAS.py`)**
   - Sets up a Dash web application to display real-time altitude data.
   - Reads data from an Arduino device via a serial connection.
   - Includes functionality to handle disconnections and user interruptions gracefully.
   - Displays data on a web dashboard and saves the data to a CSV file.

2. **Arduino Script (`UltrasonicSensor.ino`)**
   - Measures distance using an ultrasonic sensor connected to the Arduino.
   - Sends the distance data over the serial port to the connected computer.

## Requirements

### Hardware

- Arduino board (e.g., Arduino Uno)
- Ultrasonic sensor (e.g., HC-SR04)
- Jumper wires
- Breadboard

### Software

- Python 3.x
- Dash
- Dash DAQ
- Dash Bootstrap Components
- Plotly
- PySerial
- Arduino IDE

## Setup and Installation

### Arduino

1. Connect the ultrasonic sensor to the Arduino as follows:
   - VCC to 5V
   - GND to GND
   - Trig to digital pin 9
   - Echo to digital pin 8

2. Open the `UltrasonicSensor.ino` script in the Arduino IDE.
3. Upload the script to the Arduino board.

### Python

1. Install the required Python packages:
   ```
   pip install dash dash-daq dash-bootstrap-components plotly pyserial serial
   ```

2. Ensure the Arduino is connected to the computer and note the COM port (e.g., `COM9`).

3. Update the COM port in the `DAS.py` script if necessary.

4. Run the Python script:
   ```
   python DAS.py
   ```

## Usage

1. After running the Python script, open a web browser and navigate to `http://127.0.0.1:8050`.
2. The web dashboard will display real-time altitude data from the Arduino.
3. Press the stop button on the web page to terminate the data collection and close the application.

## Script Details

### Python Script (`DAS.py`)

- **Functions:**
  - `serial_monitor(port, baudrate)`: Continuously reads altitude data from the specified serial port.
  - `update_altitude_value(n_intervals, n_clicks, int_open, ard_open)`: Updates the graph and text on the web page.
  - `end_execution_1(n_clicks)`: Terminates the execution upon button press.
  - `end_execution_2(n)`: Handles errors and terminates the execution if necessary.

- **Callbacks:**
  - Updates the graph and text on the web page.
  - Displays modals in case of errors or user interruption.

### Arduino Script (`UltrasonicSensor.ino`)

- **Setup:**
  - Initializes serial communication.
  - Sets the ultrasonic sensor pins.

- **Loop:**
  - Sends a trigger pulse to the ultrasonic sensor.
  - Reads the echo pulse duration.
  - Calculates the distance based on the duration.
  - Sends the distance data over the serial port.

## Notes

- Ensure the Arduino is properly connected to the specified COM port before running the Python script.
- The Python script will create an `Altitude.csv` file to log the altitude data.

## Troubleshooting

- **SerialException**: Check the Arduino connection and the specified COM port.
- **ValueError**: Ensure the data being sent by the Arduino is in the correct format.
- **KeyboardInterrupt**: The script can be terminated using keyboard interrupts (Ctrl+C) or the stop button on the web page.

## References

- [Plotly Dash](https://dash.plotly.com/)
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
- [Arduino](https://www.arduino.cc/)
