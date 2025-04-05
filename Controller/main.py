# Standard library imports
import os
import sys
from datetime import datetime
import json
import platform
import inspect
import re
import time
import socket
import threading

# Third-party imports
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, 
    QVBoxLayout, QWidget, QScrollArea, 
    QPushButton, QStyle, QCheckBox
)
from PyQt5.QtCore import (
    Qt, QObject, pyqtSignal, pyqtSlot,
    QTimer, QThread
)
from PyQt5.QtGui import (
    QFont, QFontMetrics, QCursor, 
    QTextDocument, QTextOption
)

# Local imports
from utils.utils import (
    readJSONfile, getBaseDir, 
    StoreDependencies, softHyphenateLongWords
)
from utils.utils_UI import (
    DefineUIsizes, DefineFontSizes, StaticText,
    centerWindowOnScreen, MakeTextWithMaxHeight,
    AppSize, AppBoundaries, PushButton, Toggle
)
from utils.styles import (
    buttonStyle, toggleStyle
) 
from DailyWordApp.getDailyWords import DailyWord, DailyPriorityWord
from DailyWordApp.makeAppContents import makeAppContents
from DailyWordApp.utils import SetWindowTitle
from DailyWordApp.main import runDailyWordApp
from Timer.main import runTimer

# Store a reference to each dependency above
dep = StoreDependencies(globals())

class Controller(QObject):
    
    # Define the signals in which the controller will send messages to workers (the channels)
    startTask = pyqtSignal(str)
    shutdownTask = pyqtSignal(str)

    def __init__(self, app, dep):
        super().__init__()
        self.app = app
        self.dep = dep

        # Start the listener to listen for messages from other processes
        self.startPortListener()

        # Connect the signals (channels) to the slots (methods) that will be send down the channels
        self.startTask.connect(self.route_start)
        self.shutdownTask.connect(self.route_shutdown)

        # Define the workers: the wrappers around a particular part of a program, that define specific actions
        self.workers = {
            'dailyWordApp': DailyWordAppWrapper('DailyWordApp', app, dep),
            'timer': TimerWrapper('Timer', dep)
        }

        # Connect internal signals to controller's slots
        self.workers['timer'].request_start.connect(self.route_start)
        self.workers['timer'].request_shutdown.connect(self.route_shutdown)

        # --- NEW: Create a QThread, move TimerWrapper to that thread ---
        self.timer_thread = QThread()
        self.workers['timer'].moveToThread(self.timer_thread)
        self.timer_thread.start()
        self.workers['timer'].trigger_start.connect(self.workers['timer'].start)
        # --------------------------------------------------------------

    # Listener function - to listen for messages from other processes
    def startPortListener(self):
        threading.Thread(target=portListener, daemon=True).start()    

    # Define the slots behavior that will be sent down the signals/channels
    @pyqtSlot(str)
    def route_start(self, name):
        if name in self.workers:
            self.workers[name].start()

    @pyqtSlot(str)
    def route_shutdown(self, name):
        if name in self.workers:
            self.workers[name].shutdown()

class DailyWordAppWrapper(QObject):
    def __init__(self, name, app, dep):
        super().__init__()
        self.name = name
        self.app = app
        self.dep = dep
        self.dailyWordAppRunning = False

    def start(self):
        print(f"{self.name}: running app...")
        self.window = runDailyWordApp(self.app, self.dep)
        self.dailyWordAppRunning = True
        
    def shutdown(self):
        self.window.close()
        self.dailyWordAppRunning = False

class TimerWrapper(QObject):
   
    request_start = pyqtSignal(str)
    request_shutdown = pyqtSignal(str)
    trigger_start = pyqtSignal()

    def __init__(self, name, dep):
        super().__init__()
        self.name = name
        self.dep = dep
        self.timerRunning = False

    @pyqtSlot()
    def start(self):
        runTimer(self, self.dep)
        self.timerRunning = True    

    def shutdown(self):
        self.timerRunning = False


def portListener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 12345))
    server.listen(1)
    print("Listening for pings on port 12345...")
    while True:
        conn, addr = server.accept()
        msg = conn.recv(1024).decode()
        print(f"Received message: {msg}")
        if msg == "ping":
            print("Ping received!")
            # TODO: add logic
        conn.close()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    dep.QTimer.singleShot(20000, app.quit)  # quits after 2 seconds

    # window = runDailyWordApp(app, dep)

    controller = Controller(app, dep)
    controller.workers['timer'].trigger_start.emit()
    
    # Start the event loop and get the exit code
    exit_code = app.exec_()
    sys.exit(exit_code)