from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory

Device.pin_factory = LGPIOFactory()

from gpiozero import MotionSensor

class MotionSensorService:
    def __init__(self, pir_pin):
        self.pir = MotionSensor(pir_pin)


    def is_motion_detected(self):
        """Return True if motion is detected, False otherwise."""
        return self.pir.motion_detected
