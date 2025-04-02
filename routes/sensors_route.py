from flask import Blueprint
from controllers.sensors_controller import SensorsController

# Create Blueprint and register SensorsController with routes
sensors_blueprint = Blueprint('sensors', __name__)
sensors_view = SensorsController.as_view('sensors_controller')
sensors_blueprint.add_url_rule('/get_events', view_func=sensors_view, methods=['GET'])
sensors_blueprint.add_url_rule('/get_sensors_by_location', view_func=sensors_view, methods=['GET']) 