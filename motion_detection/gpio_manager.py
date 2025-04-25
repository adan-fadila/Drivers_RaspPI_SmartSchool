# gpio_manager.py

import RPi.GPIO as GPIO

class GPIOManager:
    def __init__(self, led_pin, relay_pin, pir_out_pin):
        self.led_pin = led_pin
        self.relay_pin = relay_pin
        self.pir_out_pin = pir_out_pin
        self.gpio_initialized = False
        self.setup_gpio()
    
    def setup_gpio(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
            GPIO.setup(self.led_pin, GPIO.OUT)
            GPIO.setup(self.relay_pin, GPIO.OUT)
            GPIO.setup(self.pir_out_pin, GPIO.IN)
            GPIO.output(self.relay_pin, GPIO.HIGH)  # Relay off initially
            self.gpio_initialized = True
        except RuntimeError as e:
            print(f"[GPIO ERROR] RuntimeError: {e}")
        except Exception as e:
            print(f"[GPIO ERROR] General Exception: {e}")
    
    def led_relay_on(self):
        if self.gpio_initialized:
            GPIO.output(self.led_pin, GPIO.HIGH)
            GPIO.output(self.relay_pin, GPIO.LOW)  # Active low relay

    def led_relay_off(self):
        if self.gpio_initialized:
            GPIO.output(self.led_pin, GPIO.LOW)
            GPIO.output(self.relay_pin, GPIO.HIGH)

    def read_pir(self):
        if self.gpio_initialized:
            return GPIO.input(self.pir_out_pin)
        return 0  # default to no motion if GPIO isn't ready
    
    def cleanup(self):
        if self.gpio_initialized:
            GPIO.cleanup()
