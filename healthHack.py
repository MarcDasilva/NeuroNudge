import serial
import time
import re
from pynput.keyboard import Controller

# Initialize keyboard controller
keyboard = Controller()

# Open serial connection (update COM port as needed)
ser = serial.Serial('COM5', 115200, timeout=1)  # Change 'COM3' to match your Arduino port (Linux/Mac: '/dev/ttyUSB0')

time.sleep(2)  # Wait for the connection to establish

print("Listening for movement...")

lowest_heart_rate = None  # Variable to track the lowest heart rate


def check_heart_rate(heart_rate):
    """Checks the heart rate and compares it to the lowest recorded value."""
    global lowest_heart_rate

    if heart_rate > 50 and (lowest_heart_rate is None or heart_rate < lowest_heart_rate):
        lowest_heart_rate = heart_rate  # Update lowest recorded heart rate
        print (lowest_heart_rate)

    if lowest_heart_rate is not None:
        difference = heart_rate - lowest_heart_rate

        if difference > 50:
            print("Keep it up!")  # Encouragement message
            keyboard.press("k")
            keyboard.release("k")

while True:
    if ser.in_waiting > 0:  # Check if data is available
        line = ser.readline().decode('utf-8').strip()  # Read and decode the line
        print(f"Arduino: {line}")  # Print received data

        if "Significant movement!" in line:  # Check if movement is detected
            print("Spacebar Pressed!")
            keyboard.press(" ")
            keyboard.release(" ")

        # Detect heart rate message
        if "heartRate=" in line:
            match = re.search(r'heartRate=(-?\d+)', line)  # Extract the number
            if match:
                heart_rate = int(match.group(1))  # Convert to integer
                print(f"Detected heart rate: {heart_rate}")

                if 150 < heart_rate < 250:
                    print("WARNING: High Heart Rate Detected!")
                    keyboard.press("h")
                    keyboard.release("h")

                check_heart_rate(heart_rate)  # Call function to check heart rate increase

    time.sleep(0.1)  # Small delay to avoid CPU overuse