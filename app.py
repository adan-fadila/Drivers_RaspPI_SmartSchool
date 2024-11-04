# app.py

from flask import Flask
from motion_detection.web_controller import WebController
from motion_detection.motion_sensor_monitor import MotionSensorMonitor
from motion_detection.gpio_manager import GPIOManager
from motion_detection.server_communicator import ServerCommunicator
from routes.mindolife_route import iot_devices_blueprint
from routes.sensibo_route import sensibo_blueprint
from routes.mock_route import devices_blueprint


from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()  # This loads the variables from .env

# Route Gateway
# Register the blueprint
app.register_blueprint(iot_devices_blueprint, url_prefix='/api-mindolife')
app.register_blueprint(sensibo_blueprint, url_prefix='/api-sensibo')
app.register_blueprint(devices_blueprint, url_prefix='/api-mock')


@app.route('/test')
def test_message():
    return 'This is a test message'
def create_app():

    # NODE_SERVER_ADDRESS = os.getenv('NODE_SERVER_ADDRESS', '10.100.102.8')
    # NODE_SERVER_PORT = os.getenv('NODE_SERVER_PORT', '8001')
    # Load environment variables
    LED_PIN = int(os.getenv('LED_PIN', '3'))
    RELAY_PIN = int(os.getenv('RELAY_PIN', '13'))
    PIR_PIN = int(os.getenv('PIR_PIN', '11'))
    # NODE_SERVER_ADDRESS = os.getenv('NODE_SERVER_ADDRESS', '10.100.102.8')
    NODE_SERVER_ADDRESS = os.getenv('NODE_SERVER_ADDRESS', '10.100.102.12')
    NODE_SERVER_PORT = os.getenv('NODE_SERVER_PORT', '8001')
    SPACE_ID = os.getenv('SPACE_ID', '61097711')  # Default or fetched from .env
    ROOM_ID = os.getenv('ROOM_ID', '38197016')
    ROOM_NAME = os.getenv('ROOM_NAME', 'Living Room')  
    DEVICE_ID = os.getenv('DEVICE_ID', '65109692') 
    ClientIP = os.getenv('ClientIP', '192.168.1.107')
    user_oid = "65b76f020db757311fe54f38"    
    # Create instances of the GPIO manager and server communicator
    gpio_manager = GPIOManager(LED_PIN, RELAY_PIN, PIR_PIN)
    server_communicator = ServerCommunicator(NODE_SERVER_ADDRESS, NODE_SERVER_PORT)
    motion_sensor_monitor = MotionSensorMonitor(gpio_manager, server_communicator, SPACE_ID, ROOM_ID, ROOM_NAME, DEVICE_ID, ClientIP, user_oid)
    
    # Create the web controller, which sets up routes
    web_controller = WebController(app, motion_sensor_monitor)
    print(f"room id is : {ROOM_ID}")
    # Start monitoring motion in a separate thread
    motion_sensor_monitor.start_monitoring()
    
    return app ,gpio_manager

if __name__ == '__main__':
    # Create the Flask app
    app ,gpio_manager= create_app()

    app.run(debug=True, host='0.0.0.0', port=5009)
    # Run the Flask application
    # try:
    #     app.run(debug=True, host='0.0.0.0', port=5009)
    # except KeyboardInterrupt:
    #     print("Program stopped")
    # finally:
    #     gpio_manager.cleanup()  # This needs to be inside create_app or handled differently
