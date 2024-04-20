import requests
import logging
import json
from urllib.parse import urlencode

def fetch_iot_devices_data():
    """Fetch IoT devices data from an external API."""
    url = 'https://api.mindolife.com/API/Gateway/getIoTDevices'
    params = {
        'developerKey': 'dec4695bf4450e3a4e0aa2b3f92929b631055ee78b77c5da59d434dee088f1cc',
        'dataType': 'json',
        'client': 'web',
        'jsonResponse': True,
        'getFullData': True,
        'daysOfHistory': 30,
        'sessionKey': '3c387806e55743f337bd915199ea7a8a426f617414ebdd8e736f2d969bb7350a3b14aafb3542940d865eaf72046ef99e78a28e7a1f4dc4eed1490380ed7d391677413bf666ba5ee7f1695dff2f5c692997d99b99765a43ed70c2125253d0aa3b5efe849bf4bafb67f45083f1a1bba0c5d8fef74415fddd9c1030a15e3e2ca689'
    }
    try:
        response = requests.get(url, params=params)
        print("Raw API Response:", response.text)  # Print raw response for debugging
        logging.debug("Raw API Response: %s", response.text)  # Log raw response

        response.raise_for_status()
        data = response.json()

        # if 'devices' not in data:
        #     logging.error("Invalid data structure or missing 'devices' key: %s", data)
        #     return {'success': False, 'message': 'Invalid data structure or missing `devices` key'}

        return data
    except requests.HTTPError as e:
        logging.error("HTTP Error: %s", e.response.text)
        return {'success': False, 'message': 'HTTP Error occurred', 'details': str(e)}
    except requests.RequestException as e:
        logging.error("Request Failed: %s", e)
        return {'success': False, 'message': 'Error fetching data', 'details': str(e)}
    except ValueError as e:
        logging.error("JSON Decode Error: %s", e)
        return {'success': False, 'message': 'Error decoding JSON data', 'details': str(e)}

def change_feature_state_service(device_id, state):
    print(device_id, state)
    base_url = 'https://api.mindolife.com/API/Gateway/changeFeatureValue'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    payload = {
        'developerKey': 'dec4695bf4450e3a4e0aa2b3f92929b631055ee78b77c5da59d434dee088f1cc',
        'dataType': 'json',
        'client': 'web',
        'jsonResponse': 'true',
        'iotDeviceID': device_id,
        'featureSetID': '1',
        'featureID': '1',
        'value': json.dumps({"value": state}),
        'sessionKey': '3c387806e55743f337bd915199ea7a8a426f617414ebdd8e736f2d969bb7350a3b14aafb3542940d865eaf72046ef99e78a28e7a1f4dc4eed1490380ed7d391677413bf666ba5ee7f1695dff2f5c692997d99b99765a43ed70c2125253d0aa3b5efe849bf4bafb67f45083f1a1bba0c5d8fef74415fddd9c1030a15e3e2ca689'
    }

    encoded_data = urlencode(payload)

    try:
        response = requests.post(base_url, headers=headers, data=encoded_data)
        response.raise_for_status()  # Check for HTTP errors

        # Assuming response should be JSON
        try:
            json_response = response.json()
            return {'success': True, 'data': json_response}
        except ValueError:
            logging.error(f"Failed to parse JSON, Status Code: {response.status_code}, Response Body: {response.text}")
            return {'success': False, 'message': "Failed to parse JSON", 'data': response.text}
    except requests.HTTPError as e:
        logging.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
        return {'success': False, 'message': 'HTTP error occurred', 'details': e.response.text}
    except requests.RequestException as e:
        logging.error(f"Error changing feature state for device ID {device_id}: {str(e)}")
        return {'success': False, 'message': 'Error changing feature state', 'details': str(e)}