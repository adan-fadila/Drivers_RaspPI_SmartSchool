# routes/motion_route.py

from flask import Blueprint
from services.motion_service import MotionSensorService
from controllers.motion_controller import MotionSensorController

motion_blueprint = Blueprint('motion', __name__)

# Initialize service and controller
sensor_service = MotionSensorService(pir_pin=17)  # Use your PIR pin
sensor_controller = MotionSensorController(sensor_service)

# Define the route
@motion_blueprint.route('/status', methods=['GET'])
def motion_status():
    return sensor_controller.get_motion_status()
