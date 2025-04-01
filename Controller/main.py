# Standard library imports
import os
import sys
from datetime import datetime
import json
import platform
import inspect
import re

# Third-party imports
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, 
    QVBoxLayout, QWidget, QScrollArea, 
    QPushButton, QStyle, QCheckBox
)
from PyQt5.QtCore import (
    Qt, QObject, pyqtSignal, pyqtSlot,
    QTimer
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

# Store a reference to each dependency above
dep = StoreDependencies(globals())

class Controller(QObject):
    
    # Define signals
    startTask = pyqtSignal(str) # signal to start worker (str)
    shutdownTask = pyqtSignal(str) # signal to shut down worker (str)
    sendMessage = pyqtSignal(str, str) # signal to receive a message from a worker (str)

    def __init__(self, app, dep):
        super().__init__()

        # Initializeworkers
        self.workers = {
            'dailyWordApp': DailyWordAppWrapper('DailyWordApp', app, dep)
        }

        # Connect general signals to routing methods
        self.startTask.connect(self.route_start)
        self.shutdownTask.connect(self.route_shutdown)
        self.sendMessage.connect(self.route_send_message)

    @pyqtSlot(str)
    def route_start(self, name):
        if name in self.workers:
            print(f"Starting {name}")
            self.workers[name].start()

    @pyqtSlot(str)
    def route_shutdown(self, name):
        if name in self.workers:
            print(f"Shutting down {name}")
            self.workers[name].shutdown()

    @pyqtSlot(str, str)
    def route_send_message(self, name, message):
        if name in self.workers:
            print(f"Sending to {name}: {message}")
            self.workers[name].receive_message(message)

class DailyWordAppWrapper(QObject):
    def __init__(self, name, app, dep):
        super().__init__()
        self.name = name
        self.app = app
        self.dep = dep

    def start(self):
        print(f"{self.name}: running app...")
        self.window = runDailyWordApp(self.app, self.dep)
        
    def shutdown(self):
        print(f"{self.name}: shutdown called (no-op or implement if needed)")

    def receive_message(self, msg):
        print(f"{self.name} received message: {msg} (no-op or handle if needed)")

if __name__ == "__main__":

    

    app = QApplication(sys.argv)
    
    dep.QTimer.singleShot(10000, app.quit)  # quits after 2 seconds

    # window = runDailyWordApp(app, dep)

    controller = Controller(app, dep)
    controller.startTask.emit('dailyWordApp') 

    # Start the event loop and get the exit code
    exit_code = app.exec_()
    sys.exit(exit_code)