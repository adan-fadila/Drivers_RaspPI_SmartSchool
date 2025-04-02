import os
import json
import logging

# Configuration file path
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'sensors_config.json')

def load_sensor_config():
    """
    Load the sensor configuration from the config file.
    
    Returns:
        dict: The sensor configuration or an empty dict if loading fails
    """
    try:
        if not os.path.exists(CONFIG_FILE_PATH):
            logging.warning(f"Sensor configuration file not found at {CONFIG_FILE_PATH}")
            return {}
            
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            return json.load(config_file)
    except Exception as e:
        logging.error(f"Error loading sensor configuration: {e}")
        return {}

def get_all_sensor_names():
    """
    Get all sensor names from the configuration file.
    
    Returns:
        list: List of sensor names
    """
    config = load_sensor_config()
    names = []
    
    if not config or 'sensors' not in config:
        return names
        
    # Extract names from all sensor types
    for sensor_type, sensors in config['sensors'].items():
        for sensor in sensors:
            if 'name' in sensor:
                names.append(sensor['name'])
                
    return names 

def get_room_for_device(device_id):
    """
    Get the room name for a given device ID.
    
    Args:
        device_id (str): The Sensibo device ID
        
    Returns:
        str: The room name or None if not found
    """
    config = load_sensor_config()
    
    if not config or 'sensors' not in config:
        return None
    
    # Look for the device ID in all sensor types
    for sensor_type, sensors in config['sensors'].items():
        for sensor in sensors:
            if sensor.get('device_id') == device_id:
                location_id = sensor.get('location')
                if location_id and 'locations' in config and location_id in config['locations']:
                    return config['locations'][location_id].get('name', location_id)
                return location_id  # Fall back to location ID if location name not found
    
    return None 

def get_sensors_by_location(location_id=None):
    """
    Get all sensors available in a specific location or all locations.
    
    Args:
        location_id (str, optional): The location ID to filter by. If None, returns all locations with their sensors.
        
    Returns:
        dict: Dictionary containing locations and their available sensors
    """
    config = load_sensor_config()
    result = {}
    
    if not config or 'locations' not in config:
        return result
    
    locations = config['locations']
    
    # Filter by location_id if provided
    if location_id:
        if location_id in locations:
            location_data = locations[location_id]
            result[location_id] = {
                'name': location_data.get('name', location_id),
                'sensors': location_data.get('sensors', [])
            }
    else:
        # Return all locations and their sensors
        for loc_id, loc_data in locations.items():
            result[loc_id] = {
                'name': loc_data.get('name', loc_id),
                'sensors': loc_data.get('sensors', [])
            }
    
    return result 