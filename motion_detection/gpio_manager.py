# gpio_manager.py

# import RPi.GPIO as GPIO

# class GPIOManager:
#     def __init__(self, led_pin, relay_pin, pir_pin):
#         self.led_pin = led_pin
#         self.relay_pin = relay_pin
#         self.pir_pin = pir_pin
#         self.setup_gpio()
    
#     def setup_gpio(self):
#         try:
#             GPIO.setwarnings(False)
#             GPIO.setmode(GPIO.BOARD)
#             GPIO.setup(self.led_pin, GPIO.OUT)
#             GPIO.setup(self.relay_pin, GPIO.OUT)
#             GPIO.setup(self.pir_pin, GPIO.IN)
#             GPIO.output(self.relay_pin, GPIO.HIGH)  # Ensure the relay is off initially
#         except Exception as e:
#             print(f"Error setting up GPIO: {e}")
    
#     def led_relay_on(self):
#         GPIO.output(self.led_pin, GPIO.HIGH)
#         GPIO.output(self.relay_pin, GPIO.LOW)  # Active low relay
    
#     def led_relay_off(self):
#         GPIO.output(self.led_pin, GPIO.LOW)
#         GPIO.output(self.relay_pin, GPIO.HIGH)  # Deactivate relay
    
#     def read_pir(self):
#         return GPIO.input(self.pir_pin)
    
#     def cleanup(self):
#         GPIO.cleanup()



# motion_detection/gpio_manager.py


class MockGPIO:
    @staticmethod
    def setmode(mode):
        pass

    @staticmethod
    def setup(channel, state):
        pass

    @staticmethod
    def output(channel, state):
        print(f"Mock output on channel {channel} to state {state}")


try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO = MockGPIO()
    GPIO_AVAILABLE = False
class GPIOManager:
    def __init__(self, led_pin, relay_pin, pir_pin):
        self.led_pin = led_pin
        self.relay_pin = relay_pin
        self.pir_pin = pir_pin
        self.setup_gpio()

    def setup_gpio(self):
        if GPIO_AVAILABLE:
            try:
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(self.led_pin, GPIO.OUT)
                GPIO.setup(self.relay_pin, GPIO.OUT)
                GPIO.setup(self.pir_pin, GPIO.IN)
                GPIO.output(self.relay_pin, GPIO.HIGH)  # Ensure the relay is off initially
            except Exception as e:
                print(f"Error setting up GPIO: {e}")
        else:
            print("Mock mode: GPIO setup skipped")

    def led_relay_on(self):
        if GPIO_AVAILABLE:
            GPIO.output(self.led_pin, GPIO.HIGH)
            GPIO.output(self.relay_pin, GPIO.LOW)  # Active low relay
        else:
            print("Mock mode: LED and relay turned on")

    def led_relay_off(self):
        if GPIO_AVAILABLE:
            GPIO.output(self.led_pin, GPIO.LOW)
            GPIO.output(self.relay_pin, GPIO.HIGH)  # Deactivate relay
        else:
            print("Mock mode: LED and relay turned off")

    def read_pir(self):
        if GPIO_AVAILABLE:
            return GPIO.input(self.pir_pin)
        else:
            print("Mock mode: PIR sensor reading")
            return False  # Simulate no motion detected

    def cleanup(self):
        if GPIO_AVAILABLE:
            GPIO.cleanup()
        else:
            print("Mock mode: Cleanup called (no action taken)")

