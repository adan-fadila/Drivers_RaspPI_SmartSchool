import logging
from flask import jsonify, request

# Import the IoT devices services module
from services.mindolife_services import fetch_iot_devices_data, change_feature_state_service
from controllers.base_controller_abstract import BaseController
# Configure detailed logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MindolifeController(BaseController):
    def get(self):
        """Handle GET requests for fetching IoT devices data."""
        try:
            result = fetch_iot_devices_data()
            if isinstance(result, dict) and not result.get('success', True):
                # If result is a dictionary and has a 'success' key that indicates failure
                return jsonify(result), 500

            # If result is a list or a successful dict without 'success' key, transform and return
            return jsonify(success=True, devices=result)  # Make sure to return 'devices' after transformation
        except Exception as e:
            logging.error("Exception during fetching or transforming IoT devices data: %s", str(e))
            return jsonify(success=False, message='Failed to fetch or transform IoT device data', error=str(e)), 500

    def post(self):
        """Handle POST requests to change feature state of an IoT device."""
        try:
            data = request.get_json()
            if not data or 'deviceId' not in data or 'state' not in data:
                return jsonify({'success': False, 'message': 'Request must include deviceId and state'}), 400

            device_id = data['deviceId']
            state = data['state']
            response_data = change_feature_state_service(device_id, state)
            return jsonify(response_data), 200 if response_data['success'] else 500
        except Exception as e:
            logging.error(f"Failed to process request: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to change feature state', 'error': str(e)}), 500


