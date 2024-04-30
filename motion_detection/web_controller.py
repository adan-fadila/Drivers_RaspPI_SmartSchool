from flask import Flask, render_template
from motion_detection.motion_sensor_monitor import MotionSensorMonitor

app = Flask(__name__)

class WebController:
    def __init__(self, app, sensor_monitor):
        self.app = app
        self.sensor_monitor = sensor_monitor

        # Setting up routes within the Flask app
        app.add_url_rule("/", "index", self.index)
        app.add_url_rule("/<action>", "action", self.action, methods=['GET', 'POST'])

    def index(self):
        """Renders the index.html with the current manual control status."""
        return render_template('index.html', manual_control=self.sensor_monitor.manual_control)

    def action(self, action):
        """Route to handle actions like turning on, off, or setting to automatic."""
        if action == "on":
            self.sensor_monitor.trigger_led_relay("on")
            self.sensor_monitor.set_manual_control(True)
        elif action == "off":
            self.sensor_monitor.trigger_led_relay("off")
            self.sensor_monitor.set_manual_control(False)
        elif action == "auto":
            self.sensor_monitor.set_manual_control(False)
        return render_template('index.html', manual_control=self.sensor_monitor.manual_control)

# Example usage, assuming the sensor monitor is properly instantiated elsewhere
# sensor_monitor = MotionSensorMonitor(gpio_manager, server_communicator)
# web_controller = WebController(app, sensor_monitor)
