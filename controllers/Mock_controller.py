import logging
from flask import jsonify, request
from controllers.base_controller_abstract import BaseController

class Mock_controller(BaseController):
    def get(self):
        pass

    def post(self):
        print("tap status switched")
        return jsonify(message="Operation successful"), 200 
