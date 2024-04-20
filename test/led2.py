import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

Relay_PIN = 13
PIR_PIN = 11

GPIO.setup(Relay_PIN, GPIO.OUT)
GPIO.setup(PIR_PIN, GPIO.IN)

# Initialize Relay to OFF
GPIO.output(Relay_PIN, GPIO.HIGH)

# Optional: Add a delay for PIR sensor stabilization (e.g., 30 seconds)
print("Waiting for PIR sensor to stabilize")
time.sleep(30)
print("PIR sensor is ready")

try:
    while True:
        if GPIO.input(PIR_PIN) == GPIO.HIGH:
            print("Bulb ON, Relay LOW")
            GPIO.output(Relay_PIN, GPIO.LOW)
        else:
            print("Bulb OFF, Relay HIGH")
            GPIO.output(Relay_PIN, GPIO.HIGH)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Program stopped")
finally:
    GPIO.cleanup()
