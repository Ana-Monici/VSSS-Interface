import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from field_graphics import MainWindow

import threading

class Window(threading.Thread):
    def __init__(self, interface):
        self.interface = interface
        self.interface.set_window(self)
        self.call_window()
    
    def call_window(self):
        app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow(self.interface)
        self.window.show()
        app.exec_()
