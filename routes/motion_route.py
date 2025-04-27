from flask import Blueprint, jsonify
import RPi.GPIO as GPIO

# Initialize Blueprint
motion_sensor_blueprint = Blueprint('motion_sensor', __name__)

# Setup GPIO mode and pin
GPIO.setmode(GPIO.BCM)  # Using GPIO.BCM mode for simplicity
PIR_PIN = 17  # GPIO pin 17 for PIR sensor

# Set up the PIR pin
GPIO.setup(PIR_PIN, GPIO.IN)

@motion_sensor_blueprint.route('/motion_state', methods=['GET'])
def get_motion_state():
    """
    Endpoint to check if motion is detected by the PIR sensor.
    Returns a JSON response with the motion state (True/False).
    """
    # Check the PIR sensor value
    if GPIO.input(PIR_PIN):
        motion_state = True  # Motion detected
    else:
        motion_state = False  # No motion detected

    # Return the state as a JSON response
    return jsonify({"motion_detected": motion_state})
