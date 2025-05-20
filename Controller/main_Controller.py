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
    QPushButton, QStyle, QCheckBox,
    QLineEdit, QMessageBox
)
from PyQt5.QtCore import (
    Qt, QObject, pyqtSignal, pyqtSlot,
    QTimer, QThread
)
from PyQt5.QtGui import (
    QFont, QFontMetrics, QCursor, 
    QTextDocument, QTextOption,
    QPainter, QPen
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

# Store a reference to each dependency above
dep = StoreDependencies(globals())

def startController():
    print('Inside the Controller executable')

    # This is where the Mutex checking will go.
    # If not already running, then start the things below, including 'app' and 'controller'
    # If already running, then send a ping to the already running controller (I guess on the relevant port), then quit

    app = QApplication(sys.argv)
    
    # dep.QTimer.singleShot(20000, app.quit)  # quits after 2 seconds
    
    controller = Controller(app, dep)
    
    # Testing - run certain workers to run certain apps
    # controller.workers['timer'].trigger_start.emit()
    controller.workers['startProgram'].start()  # Start the StartProgramApp

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

        # Connect the signals (channels) to the slots (methods) that will be sent down the channels
        self.startTask.connect(self.route_start)
        self.shutdownTask.connect(self.route_shutdown)

        # Define the workers: the wrappers around a particular part of a program, that define specific actions
        self.workers = {
            'dailyWordApp': DailyWordAppWrapper('DailyWordApp', app, dep),
            'timer': TimerWrapper('Timer', dep),
            'editWordList': EditWordListWrapper('EditWordList', app, dep),
            'startProgram': StartProgramWrapper('StartProgram', app, dep)
        }

        # Connect internal signals to controller's slots - if I want a worker to interact with another worker
        self.workers['dailyWordApp'].button_clicked.connect(self.route_start) # to allow the dailyWordApp worker to start the EditWordList
        self.workers['startProgram'].button_clicked.connect(self.route_start) # to allow the startProgram worker to start the EditWordList
        self.workers['timer'].request_start.connect(self.route_start) # to allow the timer worker to start the dailyWordApp
        self.workers['startProgram'].request_start.connect(self.route_start) # to allow the startProgram worker to start the timer, and the consoleMessage
        # self.workers['timer'].request_shutdown.connect(self.route_shutdown)

        # Initialize the port listener and sender objects - to talk to the UserInput executable
        self.portListener = PortListener(self.dep, 'portNum_Controller.txt', 'portNum_UserInput.txt')
        threading.Thread(target=self.portListener.listenIndefinitely, args=(self.pingReceivedFromUser,), daemon=True).start() # start listening
        self.portSender = PortSender(self.dep, 'portNum_UserInput.txt')  
        print("CON. Sending ping to UserInput on startup")
        threading.Thread(target=self.portSender.sendPing, args=(1.5,), daemon=True).start() # send ping to UserInput

        # Create a QThread for the TimerWrapper - it needs to be QThread rather than threading.Thread because it starts another worker using PyQt5 stuff
        self.timer_thread = QThread()
        self.workers['timer'].moveToThread(self.timer_thread)
        self.timer_thread.start()
        self.workers['timer'].trigger_start.connect(self.workers['timer'].start)

        # Connect cleanup to application quit
        self.app.aboutToQuit.connect(self.cleanUp)

    def cleanUp(self):
        self.portListener.closeSocket()
        self.portListener.clearPortNumber()

    def __del__(self):
        # Clean up the timer QThread when the Controller is destroyed
        if hasattr(self, 'timer_thread') and self.timer_thread.isRunning():
            self.timer_thread.quit()
            self.timer_thread.wait()

    def pingReceivedFromUser(self):
        # here is where I run the logic to do:
        # 1. send ping to UserInput, so it knows its ping has been received
        threading.Thread(target=self.portSender.sendPing, args=(1.5,), daemon=True).start()
        print("Con.  Inside pingReceivedFromUser.  Sending ping back to UserInput")
        # 2. figure out if the app is already running:
        # 2a. if it is, then run the startProgram stuff
        # 2b. if it is not, then run the startProgram stuff
        pass  # Do nothing when ping received

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
    def __init__(self, name, app, dep):
        super().__init__()
        self.name = name
        self.app = app
        self.dep = dep
        self.EditWordListOpen = False

    def start(self):
        print(f"{self.name}: running app...")
        self.window = makeEditWordListApp(self.app, self.dep)
        self.EditWordListOpen = True # this should actually confirm that the window is open (maybe above use something like 'if self.window is not None:')
        
    def shutdown(self):
        self.window.close()
        self.EditWordListOpen = False # this should actually confirm that the window is closed

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
        self.window = runStartProgramApp(self.app, self.dep, self)
        self.StartProgramOpen = True 
        
    def shutdown(self):
        print('\n\nController to start main app here')
        self.StartProgramOpen = False
        self.saveTimeToRunMainApp()
        self.request_start.emit("consoleMessages") # run console message to let the user know that the main program is now running in the background
        self.window.close()
        self.request_start.emit("timer") # start timer script   

    def saveTimeToRunMainApp(self):
        timeToSave = self.window.startTimeOb.timeEntered  
        root_dir, _ = self.dep.getBaseDir(self.dep.sys, self.dep.os)
        dir_accessoryFiles = self.dep.os.path.join(root_dir, 'accessoryFiles')
        self.filePath = self.dep.os.path.join(dir_accessoryFiles, 'timeToRunApplication.txt')
        with open(self.filePath, 'w') as f:
            f.write(timeToSave)

if __name__ == "__main__":
    startController()