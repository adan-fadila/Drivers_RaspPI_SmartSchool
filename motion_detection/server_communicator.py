# server_communicator.py

import requests
import socket

class ServerCommunicator:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def is_server_running(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.settimeout(2)
                s.connect((self.address, int(self.port)))
                s.close()
                print("Server is running.")
                return True
            except socket.error as e:
                print(f"Server check failed: {e}")
                return False

    def send_request_to_node(self, state):
        url = f"http://{self.address}:{self.port}/api-sensors/motion-detected"
        try:
            response = requests.post(url, json={"state": state}, timeout=5)
            if response.status_code == 200:
                print(f"Light {state} request successful: {response.status_code}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Request to Node.js server failed: {e}")
            return False
