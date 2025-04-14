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
    AppSize, AppBoundaries, PushButton, Toggle,
    makeScrollAreaForCentralWidget, resizeWindow
)
from utils.styles import (
    buttonStyle, toggleStyle
) 
from DailyWordApp.getDailyWords import DailyWord, DailyPriorityWord
from DailyWordApp.makeAppContents import makeAppContents
from DailyWordApp.utils import SetWindowTitle
from DailyWordApp.main import runDailyWordApp
from Timer.main import runTimer
from EditWordList.main import makeEditWordListApp

# Store a reference to each dependency above
dep = StoreDependencies(globals())

print(dep)

class Controller(QObject):
    
    # Define the signals in which the controller will send messages to workers (the channels)
    startTask = pyqtSignal(str)
    shutdownTask = pyqtSignal(str)

    def __init__(self, app, dep):
        super().__init__()
        self.app = app
        self.dep = dep

        # Start the listener to listen for messages from other processes (e.g., other binaries)
        self.startPortListener()

        # Connect the signals (channels) to the slots (methods) that will be sent down the channels
        self.startTask.connect(self.route_start)
        self.shutdownTask.connect(self.route_shutdown)

        # Define the workers: the wrappers around a particular part of a program, that define specific actions
        self.workers = {
            'dailyWordApp': DailyWordAppWrapper('DailyWordApp', app, dep),
            'timer': TimerWrapper('Timer', dep),
            'editWordList': EditWordListWrapper('EditWordList', dep)
        }

        # Connect internal signals to controller's slots - if I want a worker to interact with another worker
        self.workers['dailyWordApp'].button_clicked.connect(self.route_start)
        self.workers['timer'].request_start.connect(self.route_start)
        self.workers['timer'].request_shutdown.connect(self.route_shutdown)

        # --- NEW: Create a QThread, move TimerWrapper to that thread ---
        self.timer_thread = QThread()
        self.workers['timer'].moveToThread(self.timer_thread)
        self.timer_thread.start()
        self.workers['timer'].trigger_start.connect(self.workers['timer'].start)
        # --------------------------------------------------------------

    # Commuication with other executables; listener function - to listen for messages from port
    def startPortListener(self):
        portNum = findOpenPort()
        savePortNumberToFile(portNum, self.dep)
        if portNum is not None:
            threading.Thread(target=portListener, args=(portNum,), daemon=True).start()    

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

    button_clicked = pyqtSignal(str)

    # Define the constructor
    def __init__(self, name, app, dep):
        super().__init__()
        self.name = name
        self.app = app
        self.dep = dep
        self.dailyWordAppRunning = False

    def start(self):
        print(f"{self.name}: running app...")
        self.window = runDailyWordApp(self.app, self.dep, self) # pass self to allow the button_clicked signal to be used by the 'Edit Word List' button
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

class EditWordListWrapper(QObject):
    def __init__(self, name, dep):
        super().__init__()
        self.name = name
        self.dep = dep
        self.EditWordListOpen = False

    def start(self):
        print(f"{self.name}: running app...")
        makeEditWordListApp()
        # self.window = makeEditWordListApp()
        self.EditWordListOpen = True # this should actually confirm that the window is open (maybe above use something like 'if self.window is not None:')
        
    def shutdown(self):
        self.window.close()
        self.EditWordListOpen = False # this should actually confirm that the window is closed


def findOpenPort(startingPort=5000, maxTries=5000):
    port = None
    for port in range(startingPort, startingPort + maxTries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue

def savePortNumberToFile(portNum, dep):
    # Get path to text file in accessoryFiles folder to save port number
    baseDir = getBaseDir(dep.sys, dep.os)
    accessoryFiles_dir = os.path.join(baseDir, '..', 'accessoryFiles')
    curFilePath = os.path.join(accessoryFiles_dir, 'portNum_1.txt')
    with open(curFilePath, "w") as f:
        f.write(str(portNum))

def portListener(portNum):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', portNum))
    server.listen(1)
    print(f"Listening for pings on port {portNum}...")
    while True:
        conn, addr = server.accept()
        msg = conn.recv(1024).decode()
        print(f"Received message: {msg}")
        if msg == "ping":
            print("Ping received!")
            # do stuff: namely, send a message to the controller, to start stuff, send a message back to sender, etc
        conn.close()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    dep.QTimer.singleShot(20000, app.quit)  # quits after 2 seconds
    controller = Controller(app, dep)
    controller.workers['timer'].trigger_start.emit()

    # window = runDailyWordApp(app, dep)
    
    # Start the event loop and get the exit code
    exit_code = app.exec_()
    sys.exit(exit_code)