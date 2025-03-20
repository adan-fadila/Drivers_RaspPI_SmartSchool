from flask import Blueprint, jsonify
from flask.views import MethodView
from services import actuator_config_service
import logging

class ActuatorsController(MethodView):
    def get(self):
        """
        Get information about all available actuators
        """
        try:
            actuator_names = actuator_config_service.get_all_actuator_names()
            locations = actuator_config_service.get_all_locations()
            
            actuators_by_location = {}
            for location in locations:
                actuators_by_location[location] = actuator_config_service.get_actuators_by_location(location)
            
            response = {
                "status": "success",
                "data": {
                    "actuator_count": len(actuator_names),
                    "locations": actuators_by_location
                }
            }
            return jsonify(response), 200
        except Exception as e:
            logging.error(f"Error retrieving actuator data: {e}")
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

class ActuatorActionsController(MethodView):
    def get(self):
        """
        Get names of all actuators from config along with their types
        """
        try:
            actuators_with_types = actuator_config_service.get_actuators_with_types()
            if actuators_with_types:
                return jsonify({'success': True, 'actions': actuators_with_types}), 200
            else:
                return jsonify({'success': False, 'message': 'No actuator names found'}), 404
        except Exception as e:
            logging.error(f"Error retrieving actuator names: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500

# Blueprint for actuators routes
actuators_blueprint = Blueprint('actuators', __name__, url_prefix='/api-actuators')

# Register the controller with the blueprint
actuators_blueprint.add_url_rule('/list', view_func=ActuatorsController.as_view('list_actuators'), methods=['GET'])
actuators_blueprint.add_url_rule('/get_actions', view_func=ActuatorActionsController.as_view('get_actions'), methods=['GET']) 