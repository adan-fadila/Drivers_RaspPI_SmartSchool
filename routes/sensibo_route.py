from flask import Blueprint
from controllers.sensibo_controller import SensiboController

# Create Blueprint and register SensiboController with routes
sensibo_blueprint = Blueprint('sensibo', __name__)
sensibo_view = SensiboController.as_view('sensibo_controller')
sensibo_blueprint.add_url_rule('/get_ac_state', view_func=sensibo_view, methods=['GET'])
sensibo_blueprint.add_url_rule('/get_sensor_data', view_func=sensibo_view, methods=['GET'])
sensibo_blueprint.add_url_rule('/switch_ac_state', view_func=sensibo_view, methods=['POST'])
sensibo_blueprint.add_url_rule('/update_mode', view_func=sensibo_view, methods=['POST'])