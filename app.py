# app.py

import os
from flask import Flask
from dotenv import load_dotenv

from motion_detection.web_controller import WebController
from motion_detection.motion_sensor_monitor import MotionSensorMonitor
from motion_detection.gpio_manager import GPIOManager
from motion_detection.server_communicator import ServerCommunicator

from routes.mindolife_route import iot_devices_blueprint
from routes.sensibo_route import sensibo_blueprint
from routes.sensors_route import sensors_blueprint
from controllers.actuators_controller import actuators_blueprint

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Register API blueprints
    app.register_blueprint(iot_devices_blueprint, url_prefix='/api-mindolife')
    app.register_blueprint(sensibo_blueprint, url_prefix='/api-sensibo')
    app.register_blueprint(sensors_blueprint, url_prefix='/api-sensors')
    app.register_blueprint(actuators_blueprint)

    # Environment configs with fallbacks
    led_pin = int(os.getenv('LED_PIN', 3))
    relay_pin = int(os.getenv('RELAY_PIN', 13))
    pir_pin = int(os.getenv('PIR_PIN', 11))

    node_address = os.getenv('NODE_SERVER_ADDRESS', '10.100.102.12')
    node_port = os.getenv('NODE_SERVER_PORT', '8001')

    space_id = os.getenv('SPACE_ID', '61097711')
    room_id = os.getenv('ROOM_ID', '38197016')
    room_name = os.getenv('ROOM_NAME', 'Living Room')
    device_id = os.getenv('DEVICE_ID', '65109692')
    client_ip = os.getenv('ClientIP', '192.168.1.107')
    user_oid = os.getenv('USER_OID', '65b76f020db757311fe54f38')

    # Initialize GPIO manager and communication classes
    gpio_manager = GPIOManager(led_pin, relay_pin, pir_pin)
    server_comm = ServerCommunicator(node_address, node_port)
    motion_monitor = MotionSensorMonitor(
        gpio_manager, server_comm,
        space_id, room_id, room_name,
        device_id, client_ip, user_oid
    )

    # Start background motion monitoring
    motion_monitor.start_monitoring()

    # Set up web interface with control hooks
    WebController(app, motion_monitor)

    return app, gpio_manager

# Simple test route
app = Flask(__name__)
@app.route('/test')
def test_message():
    return 'This is a test message'

# Run server
if __name__ == '__main__':
    app, gpio_manager = create_app()
    try:
        app.run(debug=False, host='0.0.0.0', port=5009)
    except KeyboardInterrupt:
        print("🛑 Server interrupted by user.")
    finally:
        print("🧹 Cleaning up GPIO...")
        gpio_manager.cleanup()
