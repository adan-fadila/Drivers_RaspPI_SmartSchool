from flask import Blueprint
from controllers.mindolife_controller import MindolifeController

iot_devices_blueprint = Blueprint('iot_devices', __name__)
iot_devices_view = MindolifeController.as_view('mindolife_controller')
iot_devices_blueprint.add_url_rule('/get_devices', view_func=iot_devices_view, methods=['GET'])
iot_devices_blueprint.add_url_rule('/change_feature_state', view_func=iot_devices_view, methods=['POST'])