# motion_sensor_monitor.py

import threading
import time
from motion_detection.gpio_manager import GPIOManager
from motion_detection.server_communicator import ServerCommunicator

class MotionSensorMonitor:
    def __init__(self, gpio_manager, server_communicator):
        self.gpio_manager = gpio_manager
        self.server_communicator = server_communicator
        self.manual_control = False
        self.led_status = False
        self.thread = threading.Thread(target=self.monitor_pir, daemon=True)
    
    def monitor_pir(self):
        last_motion_time = None
        motion_detected = False
        while True:
            pir_value = self.gpio_manager.read_pir()
            if pir_value:
                last_motion_time = time.time()
                motion_detected = True
                if not self.led_status and not self.manual_control:
                    self.trigger_led_relay("on")
            elif motion_detected and (time.time() - last_motion_time > 10):
                motion_detected = False
                if not self.manual_control:
                    self.trigger_led_relay("off")
            time.sleep(0.1)
    
    def trigger_led_relay(self, state):
        if state == "on" and self.server_communicator.is_server_running() and self.server_communicator.send_request_to_node(state):
            self.gpio_manager.led_relay_on()
            self.led_status = True
            print("Bulb ON, Relay LOW")
        elif state == "off":
            self.gpio_manager.led_relay_off()
            self.led_status = False
            print("Bulb OFF, Relay HIGH")
            self.server_communicator.send_request_to_node(state)
    
    def start_monitoring(self):
        self.thread.start()
    
    def set_manual_control(self, state):
        self.manual_control = state
