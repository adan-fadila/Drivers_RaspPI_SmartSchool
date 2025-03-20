import os
import json
import logging

# Configuration file path
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'actuators_config.json')

def load_actuator_config():
    """
    Load the actuator configuration from the config file.
    
    Returns:
        dict: The actuator configuration or an empty dict if loading fails
    """
    try:
        if not os.path.exists(CONFIG_FILE_PATH):
            logging.warning(f"Actuator configuration file not found at {CONFIG_FILE_PATH}")
            return {}
            
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            return json.load(config_file)
    except Exception as e:
        logging.error(f"Error loading actuator configuration: {e}")
        return {}

def get_all_actuator_names():
    """
    Get all actuator names from the configuration file.
    
    Returns:
        list: List of actuator names
    """
    config = load_actuator_config()
    names = []
    
    if not config or 'actuators' not in config:
        return names
        
    # Extract names from all actuator types
    for actuator_type, actuators in config['actuators'].items():
        for actuator in actuators:
            if 'name' in actuator:
                names.append(actuator['name'])
                
    return names

def get_actuators_with_types():
    """
    Get all actuators with their types from the configuration file.
    
    Returns:
        list: List of dictionaries with actuator name and type
    """
    config = load_actuator_config()
    actuators_with_types = []
    
    if not config or 'actuators' not in config:
        return actuators_with_types
        
    # Extract names and types from all actuator types
    for actuator_type, actuators in config['actuators'].items():
        for actuator in actuators:
            if 'name' in actuator:
                actuators_with_types.append({
                    'name': actuator['name'],
                    'type': actuator_type
                })
                
    return actuators_with_types

def get_all_locations():
    """
    Get all configured locations.
    
    Returns:
        list: List of location identifiers
    """
    config = load_actuator_config()
    
    if not config or 'locations' not in config:
        return []
        
    return list(config['locations'].keys())

def get_actuators_by_location(location):
    """
    Get all actuators for a specific location.
    
    Args:
        location (str): Location identifier (e.g., 'livingroom')
        
    Returns:
        dict: Dictionary with location information and actuators
    """
    config = load_actuator_config()
    
    if not config or 'actuators' not in config or 'locations' not in config:
        return {}
        
    location_config = config['locations'].get(location)
    if not location_config:
        return {}
        
    result = {
        'location_name': location_config.get('name', location),
        'actuators': {}
    }
    
    # Get all actuator types for this location
    actuator_types = location_config.get('actuators', [])
    
    # Find each actuator for this location
    for actuator_type in actuator_types:
        for actuator in config['actuators'].get(actuator_type, []):
            if actuator.get('location') == location:
                if actuator_type not in result['actuators']:
                    result['actuators'][actuator_type] = []
                result['actuators'][actuator_type].append(actuator)
    
    return result 