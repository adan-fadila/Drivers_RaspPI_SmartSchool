# motion_sensor_monitor.py

import threading
import time
from motion_detection.gpio_manager import GPIOManager
from motion_detection.server_communicator import ServerCommunicator

class MotionSensorMonitor:
    def __init__(self, gpio_manager: GPIOManager, server_communicator: ServerCommunicator,
                 space_id, room_id, room_name, device_id, raspberryPiIP, user_oid):
        self.gpio_manager = gpio_manager
        self.server_communicator = server_communicator
        self.space_id = space_id
        self.room_id = room_id
        self.room_name = room_name
        self.device_id = device_id
        self.raspberryPiIP = raspberryPiIP
        self.user_oid = user_oid

        self.manual_control = False
        self.led_status = False
        self._retry_timer = None
        self.thread = threading.Thread(target=self._monitor_pir_loop, daemon=True)

    def _monitor_pir_loop(self):
        last_motion_time = None
        motion_detected = False

        while True:
            pir_value = self.gpio_manager.read_pir()

            if pir_value:
                last_motion_time = time.time()
                if not motion_detected:
                    print("Motion detected.")
                motion_detected = True

                if not self.led_status and not self.manual_control:
                    self.trigger_led_relay("on")
            elif motion_detected and last_motion_time and (time.time() - last_motion_time > 120):
                print("No motion for 2 minutes.")
                motion_detected = False

                if not self.manual_control:
                    self.trigger_led_relay("off")

            time.sleep(0.1)

    def trigger_led_relay(self, state: str):
        if not self.server_communicator.is_server_running():
            print("⚠️ Server not running — skipping relay control.")
            return

        approved, message = self.server_communicator.send_request_to_node(
            state, self.space_id, self.room_id, self.room_name,
            self.device_id, self.raspberryPiIP, self.user_oid
        )

        if approved:
            if state == "on":
                self.gpio_manager.led_relay_on()
                self.led_status = True
                print("✅ Light turned ON (Relay LOW).")
            elif state == "off":
                self.gpio_manager.led_relay_off()
                self.led_status = False
                print("✅ Light turned OFF (Relay HIGH).")
        else:
            print(f"❌ Server rejected '{state}' request: {message}")
            if "No new rules found" in message:
                print("⏳ Retrying in 30 seconds...")
                if not self._retry_timer or not self._retry_timer.is_alive():
                    self._retry_timer = threading.Timer(30, self.trigger_led_relay, args=[state])
                    self._retry_timer.start()

    def start_monitoring(self):
        print("📡 Starting PIR motion monitoring...")
        self.thread.start()

    def set_manual_control(self, state: bool):
        self.manual_control = state
        print(f"🔧 Manual control set to {state}")
