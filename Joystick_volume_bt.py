from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import serial
import time

# Define the serial port and baud rate
serial_port = 'COM3'  # Change this to match your Arduino's serial port
baud_rate = 9600

# Initialize serial communication
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def set_volume(volume_level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(volume_level, None)

def main():
    current_volume = 0.5  # Initial volume level
    switch_state = 0  # Initial switch state
    while True:
        # Read data from the Arduino Nano
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                # Split the received line into X and Y values
                x_value, switch_value = map(int, line.split(','))
                # Normalize X-axis value to the range 0.0 to 1.0
                new_volume = x_value / 100.0  # Assuming 100 is the maximum X-axis value
                if switch_value == 1:  # Check if the switch is turned on
                    if new_volume < 0.3:  # Gradually reduce volume
                        current_volume -= 0.01
                    elif new_volume > 0.6:  # Gradually increase volume
                        current_volume += 0.01
                    # Limit volume range between 0 and 1
                    current_volume = max(0, min(1, current_volume))
                    set_volume(current_volume)
                    print("Volume set to", current_volume)
                else:
                    print("Switch is off, volume adjustment disabled")
        except ValueError:
            print("Invalid data received from Arduino")

        time.sleep(0.01)  # Add a short delay

if __name__ == "__main__":
    main()
