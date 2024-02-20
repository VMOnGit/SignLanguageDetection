import serial
import time

# Define the Arduino's serial port (update this to your specific port)
  # On Windows, it's typically 'COMX'. On macOS or Linux, it's something like '/dev/ttyUSB0'.
def show_text(text):
    # Initialize the serial connection
    arduino_port = 'COM4'
    ser = serial.Serial(arduino_port, 9600)
    time.sleep(2)  # Allow time for the Arduino to reset

    try:
        while True:
            if text.lower() == 'exit':
                break
            ser.write(text.encode())  # Send the text to the Arduino
    except KeyboardInterrupt:
        pass

    ser.close()  # Close the serial connection