from flask import Blueprint
from controllers.Mock_controller import Mock_controller

devices_blueprint = Blueprint('devices', __name__)
devices_view = Mock_controller.as_view('Mock_controller')
devices_blueprint.add_url_rule('/get_devices', view_func=devices_view, methods=['GET'])
devices_blueprint.add_url_rule('/change_state', view_func=devices_view, methods=['POST'])
