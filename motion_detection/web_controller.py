from flask import Flask, render_template
from motion_detection.motion_sensor_monitor import MotionSensorMonitor

app = Flask(__name__)

class WebController:
    def __init__(self, app, sensor_monitor):
        self.app = app
        self.sensor_monitor = sensor_monitor

        # Setting up routes
        @app.route("/")
        def index():
            # Renders the index.html with the current manual control status
            return render_template('index.html', manual_control=self.sensor_monitor.manual_control)

        @app.route("/<action>", methods=['GET', 'POST'])
        def action(action):
            # Route to handle actions like turning on, off, or setting to automatic
            if action == "on":
                self.sensor_monitor.trigger_led_relay("on")
                self.sensor_monitor.set_manual_control(True)
            elif action == "off":
                self.sensor_monitor.trigger_led_relay("off")
                self.sensor_monitor.set_manual_control(False)
            elif action == "auto":
                self.sensor_monitor.set_manual_control(False)
            return render_template('index.html', manual_control=self.sensor_monitor.manual_control)

# The instance of WebController should be created in the main app module where you set up the Flask application
# Example of instantiation in app.py:
# sensor_monitor = MotionSensorMonitor(gpio_manager, server_communicator)
# web_controller = WebController(app, sensor_monitor)
