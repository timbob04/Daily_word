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
from Foundation import NSProcessInfo 

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

# Add these imports after the existing PyQt5 imports (near other third-party imports)
from AppKit import NSWorkspace
from Foundation import NSObject, NSDistributedNotificationCenter # Gives access to macOS workspace & its notifications
import objc  # PyObjC bridge: allows calling Objective-C selectors

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
    buttonStyle, toggleStyle, textStyle, checkForDarkMode_reset
) 
from DailyWordApp.getDailyWords import DailyWord, DailyPriorityWord
from DailyWordApp.utils import SetWindowTitle
from DailyWordApp.main_DailyWordApp import runDailyWordApp
from Timer.main_Timer import runTimer
from EditWordList.main_EditWordList import makeEditWordListApp
from StartProgramGUI.main_StartProgramGUI import runStartProgramApp
from Controller.LaunchAgent import CreateLaunchAgent, checkIfRunningFromLaunchAgent
from StopProgramGUI.main_StopProgramGUI import runStopProgramApp
from Controller.makeMenuIcon import makeMenuIcon
from utils.utils import isProgramAlreadyRunning
from EditTime.main_EditTime import runEditTimeApp
from Controller.raiseWindowOnUnlock import RaiseWindowOnUnlock

# Store a reference to each dependency above
dep = StoreDependencies(globals())

# Main Controller function
def startController():
    print('Inside the Controller executable')

    executableName = 'DailyWordDefinitionController'
    
    # Shut down current script if a previous instance is already running, to prevent multiple instances
    if isProgramAlreadyRunning(executableName, dep):
        print(f'{executableName} is already running')
        sys.exit(0)
    
    print(f'{executableName} is NOT already running.  Carrying on...')
    
    app = QApplication(sys.argv) # start the application

    # Create a named local socket so other copies can check if this one is running (to prevent multiple instances)
    server = QLocalServer()
    if not server.listen(executableName):
        QLocalServer.removeServer(executableName)
        server.listen(executableName)
    app.server = server # Store it on the app to prevent it from being garbage collected

    # Create the controller object
    controller = Controller(app, dep)

    # Make the menu icon for the mac's toolbar
    makeMenuIcon(dep, app, controller)

    # If running from launch agent (on startup), start the main program (timer and dailyWordApp) directly.  Else, run the the controller (above) and wait for user inputs
    if checkIfRunningFromLaunchAgent(dep, 'main_Controller'):
        print("Running from launch agent - starting timer directly")
        controller.startTask.emit('timer')

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
            'timer': TimerWrapper('Timer', dep, self),  # pass controller so timer can access sessionObserver
            'editWordList': EditWordListWrapper('EditWordList', app, dep),
            'startProgram': StartProgramWrapper('StartProgram', app, dep),
            'stopProgram': StopProgramWrapper('StopProgram', app, dep),
            'editTime': EditTimeWrapper('EditTime', app, dep)
        }

        # Connect internal signals to controller's slots - if I want a worker to interact with another worker        
        self.workers['timer'].request_start.connect(self.route_start) # to allow the timer worker to start the dailyWordApp
        self.workers['startProgram'].request_start.connect(self.route_start) # to allow the startProgram worker to start the timer, and the consoleMessage

        # Initialize the port listener and sender objects - to talk to the PingController executable (what the user runs to interact with the controller)
        # Listener
        self.portListener = PortListener(self.dep, 'portNum_Controller.txt', 'portNum_PingController.txt')
        threading.Thread(target=self.portListener.listenIndefinitely, args=(self.pingReceivedFromUser,), daemon=True).start() # start listening
        # Sender
        self.portSender = PortSender(self.dep, 'portNum_PingController.txt')  
        print("CON. Sending ping to PingController on startup")
        threading.Thread(target=self.portSender.sendPing, args=(1.5,), daemon=True).start() # send ping to PingController

        # Connect cleanup function to application quit
        self.app.aboutToQuit.connect(self.cleanUp)
        
        # If the time to display word occurs when display is not on (mac locked, etc), for the first unlock after this, bring DailyWordApp to the forefront on unlock
        self.sessionObserver = RaiseWindowOnUnlock(self.app, self.dep, self.workers)

    def userInitiatedQuit(self):
        print("User initiated quit - unlinking launch agent")
        launchAgent = CreateLaunchAgent(self.dep, 'main_Controller')
        launchAgent.unlinkPlist()
        self.app.quit()

    def cleanUp(self):
        self.portListener.closeSocket()
        self.portListener.clearPortNumber()
        NSDistributedNotificationCenter.defaultCenter().removeObserver_(self.sessionObserver)

    # Once a ping is received from the user (PingController), do stuff (either start program, if not already running, or stop program, if already running)
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

###### Workers for the Controller ######

# Worker for the dailyWordApp
class DailyWordAppWrapper(QObject):

    # Define the constructor
    def __init__(self, name, app, dep):
        super().__init__()
        self.name = name
        self.app = app
        self.dep = dep

    def start(self):
        print(f"{self.name}: running app...")
        # Close any previous instances of the dailyWordApp
        if isGUIAlreadyOpen(self):
            self.window.close()
        # Now run the dailyWordApp
        self.window = runDailyWordApp(self.app, self.dep) # pass self to allow the button_clicked signal to be used by the 'Edit Word List' button
        # Bring window to front
        self.window.raise_()
        self.window.activateWindow()

# Worker for the timer which controls when the dailyWordApp is shown
class TimerWrapper(QObject):
   
    # Define the signal to start the dailyWordApp
    request_start = pyqtSignal(str)

    def __init__(self, name, dep, controller):
        super().__init__()
        self.name = name
        self.dep = dep
        self.controller = controller  # keep reference to controller to reset observer flag
        self.timerRunning = False

    def start(self):
        self.timerRunning = True
        self.timer_thread = self.dep.threading.Thread(target=runTimer, args=(self, self.dep), daemon=True)
        self.timer_thread.start()

# Worker for the EditWordList app
class EditWordListWrapper(QObject):

    def __init__(self, name, app, dep):
        super().__init__()
        self.name = name
        self.app = app
        self.dep = dep

    def start(self):
        print(f"{self.name}: running app...")
        if not isGUIAlreadyOpen(self):
            self.window = makeEditWordListApp(self.app, self.dep)
        
        # Always bring window to front
        self.window.raise_()
        self.window.activateWindow()

# Worker for the StartProgram app
class StartProgramWrapper(QObject):

    request_start = pyqtSignal(str)

    def __init__(self, name, app, dep):
        super().__init__()
        self.name = name
        self.app = app
        self.dep = dep

    def start(self):
        print(f"{self.name}: running app...")
        if not isGUIAlreadyOpen(self):
            self.window = runStartProgramApp(self.app, self.dep, self)
            # Quit app if this window is closed via the X button (only),
            # as the user did not decide to start the program
            self.window.closeEvent = (
                lambda event: self.app.quit()
                if not self.window.startButtonClicked
                else None            # Only quit if window is closed via X button,
            )
        # Bring window to front
        self.window.raise_()
        self.window.activateWindow()

    # Perform functions required to start the program, once the user has clicked the Start button
    def shutdown(self):
        print('\n\nThe user has clicked the Start button')
        self.window.startButtonClicked = True  # Set flag to indicate Start button was clicked (used in 'start' function)
        self.saveTimeToRunMainApp()
        self.window.close() 
        self.request_start.emit("timer") # start timer script   
        CreateLaunchAgent(self.dep, 'Controller') # create a lanch agent for this program, so it now starts up on login

    def saveTimeToRunMainApp(self):
        timeToSave = self.window.startTimeOb.timeEntered  
        root_dir, _ = self.dep.getBaseDir(self.dep.sys, self.dep.os)
        dir_accessoryFiles = self.dep.os.path.join(root_dir, 'accessoryFiles')
        self.filePath = self.dep.os.path.join(dir_accessoryFiles, 'timeToRunApplication.txt')
        with open(self.filePath, 'w') as f:
            f.write(timeToSave)

# Worker for the StopProgram app
class StopProgramWrapper(QObject):

    def __init__(self, name, app, dep):
        super().__init__()
        self.name = name
        self.app = app
        self.dep = dep

    # Run the StopProgram app
    def start(self):
        print(f"{self.name}: running app...")
        if not isGUIAlreadyOpen(self):
            self.window = runStopProgramApp(self.app, self.dep, self)
        # Bring window to front
        self.window.raise_()
        self.window.activateWindow()

    # Perform functions required to stop the program, once the user has clicked the Stop button
    def shutdown(self):
        print('\n\nController to stop main app here')
        self.window.close()
        self.app.controller.userInitiatedQuit()  # Use the new function instead of app.quit()

# Worker for the EditTime app - accessed through menu icon only
class EditTimeWrapper(QObject):

    def __init__(self, name, app, dep):
        super().__init__()
        self.name = name
        self.app = app
        self.dep = dep

    def start(self):
        print(f"{self.name}: running app...")
        if not isGUIAlreadyOpen(self):
            self.window = runEditTimeApp(self.app, self.dep, self)
        # Bring window to front
        self.window.raise_()
        self.window.activateWindow()

    def shutdown(self):
        print('\n\nThe user has clicked the Change button')
        self.saveTimeToRunMainApp()
        self.window.close() 

    def saveTimeToRunMainApp(self):
        timeToSave = self.window.EditTimeOb.timeEntered  
        root_dir, _ = self.dep.getBaseDir(self.dep.sys, self.dep.os)
        dir_accessoryFiles = self.dep.os.path.join(root_dir, 'accessoryFiles')
        self.filePath = self.dep.os.path.join(dir_accessoryFiles, 'timeToRunApplication.txt')
        with open(self.filePath, 'w') as f:
            f.write(timeToSave)

def isGUIAlreadyOpen(worker):
    return (hasattr(worker, 'window') and 
            worker.window and 
            not worker.window.isHidden() and
            worker.window.isVisible())


if __name__ == "__main__":
    startController()