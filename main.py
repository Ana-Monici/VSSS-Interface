import os
from api.new_api import Api
from api.api_recv import Api_recv
import argparse
import json
from game import Match

# import sys
# from PyQt5 import QtCore, QtGui, QtWidgets, uic
# from field_graphics import MainWindow
from field_graphics import Window

parser = argparse.ArgumentParser(description='NeonInterface')
parser.add_argument('--config_file', default='config.json')

args = parser.parse_args()

def get_config(config_file=None):
    if config_file:
        config = json.loads(open(config_file, 'r').read())
    else:
        config = json.loads(open('config.json', 'r').read())

    return config

class Interface():
    def __init__(self, config_file=None):
        self.config = get_config(config_file)
        self.match = Match(self)

        self.api_address = self.config.get("network").get("api_address")
        self.api_port = self.config.get("network").get("api_port")
        self.api_recv_port = self.config.get("network").get("api_recv_port")

        self.api = Api(self.api_address, self.api_port)

        self.api_recv = Api_recv(self, self.match, self.api_address, self.api_recv_port)

        self.start()

    def start(self):
        self.api.start()
        self.api_recv.start()
        # self.match.game_status = "GAME_ON"
        # self.match.start()
        # self.update()
    
    def update(self):
        self.api.send_data(self.match)
        # self.match.update()

interface = Interface(config_file=args.config_file)

window = Window(interface)

# while True:
#     interface.update()

# app = QtWidgets.QApplication(sys.argv)
# window = MainWindow(interface)
# window.show()
# app.exec_()
