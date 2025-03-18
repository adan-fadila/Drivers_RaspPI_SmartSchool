from flask import request, jsonify
import logging
from services.sensor_config_service import get_all_sensor_names
from controllers.base_controller_abstract import BaseController

class SensorsController(BaseController):
    def get(self):
        """Handles GET requests for sensor-related endpoints."""
        if request.path.endswith('/get_events'):
            # Get all sensor names from the configuration
            sensor_names = get_all_sensor_names()
            if sensor_names:
                return jsonify({'success': True, 'events': sensor_names}), 200
            else:
                return jsonify({'success': False, 'message': 'No sensor names found'}), 404
    
    def post(self):
        """Handles POST requests for sensor-related endpoints."""
        # This method is required by the abstract base class
        # We don't have any POST endpoints yet, so we'll return a method not allowed error
        return jsonify({'success': False, 'message': 'Method not allowed'}), 405 