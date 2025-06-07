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
import ctypes
import subprocess
import pathlib
import textwrap
import stat

# Third-party imports
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, 
    QVBoxLayout, QWidget, QScrollArea, 
    QPushButton, QStyle, QCheckBox,
    QLineEdit, QMessageBox, QSystemTrayIcon,
    QMenu, QAction
)
from PyQt5.QtCore import (
    Qt, QObject, pyqtSignal, pyqtSlot,
    QTimer, QThread, QCoreApplication
)
from PyQt5.QtGui import (
    QFont, QFontMetrics, QCursor, 
    QTextDocument, QTextOption,
    QPainter, QPen, QIcon
)

from PyQt5.QtNetwork  import (
    QLocalServer, QLocalSocket
)

# Local imports
from utils.utils import (
    readJSONfile, getBaseDir, 
    StoreDependencies, softHyphenateLongWords,
    PortListener, PortSender
)
from utils.utils_UI import (
    DefineUIsizes, DefineFontSizes, StaticText,
    centerWindowOnScreen, MakeTextWithMaxHeight,
    AppSize, AppBoundaries, PushButton, Toggle,
    makeScrollAreaForCentralWidget, resizeWindow,
    EditTextBox
)
from utils.styles import (
    buttonStyle, toggleStyle
) 
from DailyWordApp.getDailyWords import DailyWord, DailyPriorityWord
from DailyWordApp.utils import SetWindowTitle
from DailyWordApp.main_DailyWordApp import runDailyWordApp
from Timer.main_Timer import runTimer
from EditWordList.main_EditWordList import makeEditWordListApp
from StartProgramGUI.main_StartProgramGUI import runStartProgramApp
from consoleMessages.programStarting import consoleMessage_startProgram
from Controller.createLaunchAgent import CreateLaunchAgent
from StopProgramGUI.main_StopProgramGUI import runStopProgramApp
from Controller.makeMenuIcon import makeMenuIcon
from Controller.utils import isProgramAlreadyRunning

# Store a reference to each dependency above
dep = StoreDependencies(globals())

# This is to stop the icon from appearing in the dock on macOS
if platform.system() == 'Darwin':
    from Foundation import NSBundle
    bundle = NSBundle.mainBundle()
    info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
    info['LSUIElement'] = 1

def startController():
    print('Inside the Controller executable')

    executableName = 'DailyWordDefinitionController'

    app = QApplication(sys.argv)

    # Shut down script if a previous instance is already running
    if isProgramAlreadyRunning(executableName, dep):
        print('DailyWordDefinitionController is already running')
        return

    # Create a named local socket so other copies can check if this one is running (to prevent multiple instances)
    server = QLocalServer()
    server.listen(executableName)
    app.server = server # Store it on the app to prevent it from being garbage collected

    # Create the controller object
    controller = Controller(app, dep)

    # Start the startProgram app (this will also start the timer)
    controller.workers['startProgram'].start()

    # Make the menu icon
    makeMenuIcon(dep, app, controller)

    # Start the event loop and get the exit code
    exit_code = app.exec_()
    sys.exit(exit_code)

class Controller(QObject):
    
    # Define the signals in which the controller will send messages to workers (the channels)
    startTask = pyqtSignal(str)
    shutdownTask = pyqtSignal(str)

    def __init__(self, app, dep):
        super().__init__()
        self.app = app
        self.dep = dep
        # Default values
        self.launchAgent = None

        # Connect the signals (channels) to the slots (methods) that will be sent down the channels
        self.startTask.connect(self.route_start)
        self.shutdownTask.connect(self.route_shutdown)

        # Define the workers: the wrappers around a particular part of a program, that define specific actions
        self.workers = {
            'dailyWordApp': DailyWordAppWrapper('DailyWordApp', app, dep),
            'timer': TimerWrapper('Timer', dep),
            'editWordList': EditWordListWrapper('EditWordList', app, dep),
            'startProgram': StartProgramWrapper('StartProgram', app, dep),
            'stopProgram': StopProgramWrapper('StopProgram', app, dep)
        }

        # Connect internal signals to controller's slots - if I want a worker to interact with another worker
        self.workers['dailyWordApp'].button_clicked.connect(self.route_start) # to allow the dailyWordApp worker to start the EditWordList
        self.workers['startProgram'].button_clicked.connect(self.route_start) # to allow the startProgram worker to start the EditWordList
        self.workers['timer'].request_start.connect(self.route_start) # to allow the timer worker to start the dailyWordApp
        self.workers['startProgram'].request_start.connect(self.route_start) # to allow the startProgram worker to start the timer, and the consoleMessage

        # Initialize the port listener and sender objects - to talk to the PingController executable
        self.portListener = PortListener(self.dep, 'portNum_Controller.txt', 'portNum_PingController.txt')
        threading.Thread(target=self.portListener.listenIndefinitely, args=(self.pingReceivedFromUser,), daemon=True).start() # start listening
        self.portSender = PortSender(self.dep, 'portNum_PingController.txt')  
        print("CON. Sending ping to PingController on startup")
        threading.Thread(target=self.portSender.sendPing, args=(1.5,), daemon=True).start() # send ping to PingController

        # Connect cleanup to application quit
        self.app.aboutToQuit.connect(self.cleanUp)

    def cleanUp(self):
        self.portListener.closeSocket()
        self.portListener.clearPortNumber()
        # remove the launch agent so the program doesn't start on login
        if self.launchAgent:
            self.launchAgent.unlinkPlist() 

    def pingReceivedFromUser(self, message):
        print(f"pingReceivedFromUser: {message}")
        # Send ping to PingController, so it knows its ping has been received
        threading.Thread(target=self.portSender.sendPing, args=(1.5,), daemon=True).start()
        # Run the start or stop program stuff
        if not self.workers['timer'].timerRunning:
            self.startTask.emit('startProgram') 
        else:
            self.startTask.emit('stopProgram')

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
        # Close any previous instances of the dailyWordApp
        if hasattr(self, 'window') and self.window:
            self.window.close()
        # Now run the dailyWordApp
        self.window = runDailyWordApp(self.app, self.dep, self) # pass self to allow the button_clicked signal to be used by the 'Edit Word List' button
        self.dailyWordAppRunning = True
        
    def shutdown(self):
        self.window.close()
        self.dailyWordAppRunning = False

class TimerWrapper(QObject):
   
    request_start = pyqtSignal(str)

    def __init__(self, name, dep):
        super().__init__()
        self.name = name
        self.dep = dep
        self.timerRunning = False
        self.timer_thread = None

    def start(self):
        self.timerRunning = True
        self.timer_thread = self.dep.threading.Thread(target=runTimer, args=(self, self.dep), daemon=True)
        self.timer_thread.start()

class EditWordListWrapper(QObject):
    def __init__(self, name, app, dep):
        super().__init__()
        self.name = name
        self.app = app
        self.dep = dep
        self.EditWordListOpen = False

    def start(self):
        print(f"{self.name}: running app...")
        if hasattr(self, 'window') and self.window:
            self.window.raise_()  # Bring window to front
            self.window.activateWindow()  # Make it the active window
        else:
            self.window = makeEditWordListApp(self.app, self.dep)
            self.EditWordListOpen = True

class StartProgramWrapper(QObject):

    request_start = pyqtSignal(str)
    button_clicked = pyqtSignal(str)

    def __init__(self, name, app, dep):
        super().__init__()
        self.name = name
        self.app = app
        self.dep = dep
        self.StartProgramOpen = False

    def start(self):
        print(f"{self.name}: running app...")
        if hasattr(self, 'window') and self.window:
            self.window.raise_()  # Bring window to front
            self.window.activateWindow()  # Make it the active window
        else:
            self.window = runStartProgramApp(self.app, self.dep, self)
            self.window.closeEvent = lambda event: self.app.quit()  # Quit app when window is closed
            self.StartProgramOpen = True

    def shutdown(self):
        print('\n\nThe user has clicked the Start button')
        self.StartProgramOpen = False
        self.saveTimeToRunMainApp()
        self.window.close()
        self.request_start.emit("timer") # start timer script   
        self.launchAgent = CreateLaunchAgent(self.dep, 'main_Controller') # create a lanch agent for this program, so it now starts up on login

    def saveTimeToRunMainApp(self):
        timeToSave = self.window.startTimeOb.timeEntered  
        root_dir, _ = self.dep.getBaseDir(self.dep.sys, self.dep.os)
        dir_accessoryFiles = self.dep.os.path.join(root_dir, 'accessoryFiles')
        self.filePath = self.dep.os.path.join(dir_accessoryFiles, 'timeToRunApplication.txt')
        with open(self.filePath, 'w') as f:
            f.write(timeToSave)

class StopProgramWrapper(QObject):

    def __init__(self, name, app, dep):
        super().__init__()
        self.name = name
        self.app = app
        self.dep = dep
        self.StopProgramOpen = False

    def start(self):
        print(f"{self.name}: running app...")
        if hasattr(self, 'window') and self.window:
            self.window.raise_()  # Bring window to front
            self.window.activateWindow()  # Make it the active window
        else:
            self.window = runStopProgramApp(self.app, self.dep, self)
            self.StopProgramOpen = True

    def shutdown(self):
        print('\n\nController to stop main app here')
        self.StopProgramOpen = False
        self.window.close()
        self.app.quit()  # This will trigger cleanup and exit the application

if __name__ == "__main__":
    startController()