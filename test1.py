import RPi.GPIO as GPIO
import time

# Setup GPIO mode and pin
GPIO.setmode(GPIO.BCM)  # Using GPIO.BCM mode for simplicity
PIR_PIN = 17  # GPIO pin 17 for PIR sensor

# Set up the PIR pin
GPIO.setup(PIR_PIN, GPIO.IN)

print("PIR Sensor Test Script")
print("Press Ctrl+C to exit")

try:
    while True:
        # Read PIR sensor value
        if GPIO.input(PIR_PIN):
            print("Motion Detected!")
        else:
            print("No Motion")
        
        # Sleep to prevent overwhelming the terminal
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting PIR sensor test...")

finally:
    # Clean up GPIO settings to reset the pin state
    GPIO.cleanup()
