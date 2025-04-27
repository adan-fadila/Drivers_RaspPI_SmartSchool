from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

hue_api_blueprint = Blueprint('hue_api', __name__)

# Read them safely from environment
HUE_API_URL = os.getenv("HUE_API_URL")
HUE_APP_KEY = os.getenv("HUE_APP_KEY")

@hue_api_blueprint.route('/get_light_state', methods=['GET'])
def get_light_state():
    try:
        # Get the light ID from query parameters, default to '1'
        light_id = request.args.get('light_id', '1')

        # URL to fetch light state from Hue API
        url = f"{HUE_API_URL}/{light_id}"
        headers = {
            "hue-application-key": HUE_APP_KEY,
            "Content-Type": "application/json"
        }

        # Make the GET request to Hue API
        response = requests.get(url, headers=headers, verify=False)

        # Check if the API call was successful
        if response.status_code == 200:
            return jsonify({
                "message": "Light state retrieved successfully",
                "success": True,
                "data": response.json()
            }), 200
        else:
            return jsonify({
                "message": "Failed to retrieve light state",
                "success": False,
                "errors": response.json()
            }), 500

    except Exception as e:
        return jsonify({
            "message": f"Error: {str(e)}",
            "success": False
        }), 500


@hue_api_blueprint.route('/switch_light_state', methods=['PUT'])
def switch_light_state():
    try:
        # Parse incoming JSON data
        data = request.get_json()

        # Extract required fields from the request body
        light_id = data.get('light_id')
        state = data.get('state')
        brightness = data.get('brightness', None)
        color = data.get('color', None)

        # Validate inputs
        if not light_id or state is None:
            return jsonify({
                "message": "Missing required fields (light_id, state).",
                "success": False
            }), 400

        # Prepare the payload for the PUT request to Hue API
        payload = {
            "on": {"on": state}
        }

        # Add optional brightness and color if provided
        if brightness is not None:
            payload["bri"] = brightness
        if color is not None:
            payload["hue"] = color.get("hue")
            payload["sat"] = color.get("sat")

        # Make the PUT request to the Hue API
        url = f"{HUE_API_URL}/{light_id}"
        headers = {
            "hue-application-key": HUE_APP_KEY,
            "Content-Type": "application/json"
        }

        response = requests.put(url, json=payload, headers=headers, verify=False)

        # Check the response from Hue API
        if response.status_code == 200:
            return jsonify({
                "message": "Light state updated successfully",
                "success": True,
                "data": response.json()
            }), 200
        else:
            return jsonify({
                "message": "Failed to update light state",
                "success": False,
                "errors": response.json()
            }), 500

    except Exception as e:
        return jsonify({
            "message": f"Error: {str(e)}",
            "success": False
        }), 500
