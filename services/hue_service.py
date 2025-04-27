import requests

class HueService:
    def __init__(self):
        self.hue_base_url = "http://<HUE_BRIDGE_IP>/api/<HUE_USERNAME>/lights"  # Replace with your Hue Bridge IP and username

    def switch_light_state(self, data):
        """Switch the state of a light via the Hue API"""
        light_id = data.get("light_id")
        state = data.get("state")
        brightness = data.get("brightness", None)
        color = data.get("color", None)

        if not light_id:
            return {"success": False, "message": "Light ID is required"}, 400

        # Build the URL to the Hue API endpoint for the specific light
        url = f"{self.hue_base_url}/{light_id}/state"
        
        # Construct the payload
        payload = {"on": state}
        if brightness is not None:
            payload["bri"] = brightness
        if color is not None:
            payload["hue"] = color.get("hue", 0)  # Assume color is a dict like {"hue": 10000, "sat": 254}
            payload["sat"] = color.get("sat", 254)

        # Make a PUT request to the Hue API
        try:
            response = requests.put(url, json=payload)
            response_data = response.json()

            if response.status_code == 200 and response_data.get("success"):
                return {"success": True, "statusCode": 200, "data": response_data}
            else:
                error_msg = response_data.get("error", {}).get("description", "Unknown error")
                return {"success": False, "message": error_msg}, response.status_code
        except requests.RequestException as e:
            return {"success": False, "message": str(e)}, 500

    def get_light_state(self, light_id):
        """Get the current state of a light via the Hue API"""
        if not light_id:
            return {"success": False, "message": "Light ID is required"}, 400

        # Build the URL to the Hue API endpoint for the specific light
        url = f"{self.hue_base_url}/{light_id}"

        # Make a GET request to the Hue API
        try:
            response = requests.get(url)
            response_data = response.json()

            if response.status_code == 200:
                # Return the light state (simplified)
                light_state = {
                    "state": response_data.get("state", {}),
                    "name": response_data.get("name", "Unknown")
                }
                return {"success": True, "lightState": light_state}, 200
            else:
                error_msg = response_data.get("error", {}).get("description", "Unknown error")
                return {"success": False, "message": error_msg}, response.status_code
        except requests.RequestException as e:
            return {"success": False, "message": str(e)}, 500
