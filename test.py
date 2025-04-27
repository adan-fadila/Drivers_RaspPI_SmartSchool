from flask import Flask, jsonify
import RPi.GPIO as GPIO
import time

# Initialize Flask app
app = Flask(__name__)

# Setup GPIO mode and pin
GPIO.setmode(GPIO.BCM)  # Using GPIO.BCM mode for simplicity
PIR_PIN = 17  # GPIO pin 17 for PIR sensor

# Set up the PIR pin
GPIO.setup(PIR_PIN, GPIO.IN)

@app.route('/motion_state', methods=['GET'])
def get_motion_state():
    """
    Endpoint to check if motion is detected by the PIR sensor.
    Returns a JSON response with the motion state (True/False).
    """
    # Check the PIR sensor value
    if GPIO.input(PIR_PIN):
        # Motion detected
        motion_state = True
    else:
        # No motion detected
        motion_state = False

    # Return the state as a JSON response
    return jsonify({"motion_detected": motion_state})

if __name__ == '__main__':
    try:
        # Start the Flask app
        app.run(host='0.0.0.0', port=5000, debug=True)

    except KeyboardInterrupt:
        print("Exiting PIR sensor test...")

    finally:
        # Clean up GPIO settings to reset the pin state when the app exits
        GPIO.cleanup()
