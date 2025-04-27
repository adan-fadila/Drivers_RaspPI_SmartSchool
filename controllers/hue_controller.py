from services.hue_service import HueService
from flask import jsonify

class HueController:
    def __init__(self):
        self.hue_service = HueService()

    def switch_light_state(self, light_id, state, brightness=None, color=None):
        try:
            # Ensure that the light_id and state are received
            if not light_id or state is None:
                raise ValueError("light_id and state are required.")

            # Logic for interacting with the Hue API to switch the light state
            if state:
                # Logic for turning the light ON
                print(f"Turning light {light_id} ON")
            else:
                # Logic for turning the light OFF
                print(f"Turning light {light_id} OFF")

            # If brightness is provided, handle brightness logic
            if brightness is not None:
                print(f"Setting brightness for light {light_id} to {brightness}")
                # Add code to adjust brightness using the Hue API

            # If color is provided, handle color logic
            if color is not None:
                print(f"Setting color for light {light_id} to hue={color['hue']}, sat={color['sat']}")
                # Add code to change the color using the Hue API

            # After successfully switching the light state, return success
            return {"message": "Light state updated successfully", "success": True}

        except Exception as e:
            # Handle exceptions and return a failure message
            return {"message": f"Error switching light state: {str(e)}", "success": False}
    def get_light_state(self, light_id):
        try:
            # Call the service layer to retrieve the light state
            result = self.hue_service.get_light_state(light_id)
            return jsonify(result), result['statusCode']
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
