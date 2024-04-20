# gpio_manager.py

import RPi.GPIO as GPIO

class GPIOManager:
    def __init__(self, led_pin, relay_pin, pir_pin):
        self.led_pin = led_pin
        self.relay_pin = relay_pin
        self.pir_pin = pir_pin
        self.setup_gpio()
    
    def setup_gpio(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.led_pin, GPIO.OUT)
            GPIO.setup(self.relay_pin, GPIO.OUT)
            GPIO.setup(self.pir_pin, GPIO.IN)
            GPIO.output(self.relay_pin, GPIO.HIGH)  # Ensure the relay is off initially
        except Exception as e:
            print(f"Error setting up GPIO: {e}")
    
    def led_relay_on(self):
        GPIO.output(self.led_pin, GPIO.HIGH)
        GPIO.output(self.relay_pin, GPIO.LOW)  # Active low relay
    
    def led_relay_off(self):
        GPIO.output(self.led_pin, GPIO.LOW)
        GPIO.output(self.relay_pin, GPIO.HIGH)  # Deactivate relay
    
    def read_pir(self):
        return GPIO.input(self.pir_pin)
    
    def cleanup(self):
        GPIO.cleanup()
