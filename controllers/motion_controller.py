# motion_detection/motion_sensor_controller.py

from flask import jsonify

class MotionSensorController:
    def __init__(self, sensor_service):
        self.sensor_service = sensor_service

    def get_motion_status(self):
        """Return the current motion sensor status."""
        motion = self.sensor_service.is_motion_detected()
        return jsonify({
            "motion_detected": motion
        })
