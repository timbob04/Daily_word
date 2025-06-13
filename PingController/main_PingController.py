import sys
import os
import platform
import subprocess
import socket
from utils.utils import getBaseDir
import time
import threading
from utils.utils import PortListener, PortSender, StoreDependencies
from utils.utils import isProgramAlreadyRunning
from PyQt5.QtNetwork  import (
    QLocalServer, QLocalSocket
)

# Store a reference to each dependency above
dep = StoreDependencies(globals())

def runPingController():

    executableName = 'DailyWordDefinitionPingController'

    # Don't run if another instance is already running
    if isProgramAlreadyRunning(executableName, dep):
        print(f'{executableName} is already running')
        return
    
    # Create a named local socket so other copies can check if this one is running (to prevent multiple instances)
    server = QLocalServer()
    server.listen(executableName)

    # Set up a port listener for receiving messages from the Controller
    portListener = PortListener(dep, 'portNum_PingController.txt', 'portNum_Controller.txt')
    # Set up a port sender for sending messages to the Controller
    portSender = PortSender(dep, 'portNum_Controller.txt')
    # Send ping to Controller
    print("Sending ping to Controller")
    portSender.sendPing(0, 'UserClickedOnIcon')
    # Start listening for a response from the Controller
    print("Listening for response from Controller")
    portListener.listenForCertainTime(5)
    # Wait for response from Controller
    if portListener.responseReceived:
        print("Response received from Controller after first ping")
    else:
        print("No response received from Controller after first ping.  Running its executable...")
        runControllerExecutable()
        portListener.listenForCertainTime(20) # instead of pinging the Controller again, just have the Controller ping this executable once it starts up
        print("Listening for response from Controller after running its executable")
        if portListener.responseReceived:
            print("Response received from Controller after running its executable")
            portSender.sendPing(0, 'UserClickedOnIcon')
        else:
            print("No response received from Controller after running its executable.  Exiting...")
    # Clean up (clear) the port number in portNum_PingController.txt
    portListener.clearPortNumber()

def runControllerExecutable():
    # First check to see if this script is running as a .py or executable
    runingCodeFromExecutable = getattr(sys, 'frozen', False) # The 'frozen' attribute in sys is set to True if the script is running as an executable
    if runingCodeFromExecutable:
        root_dir, _ = getBaseDir(sys, os)
        print("\nRunning executable on Mac")
        exePath_Controller = os.path.join(root_dir, "bin", "main_Controller.app")
        subprocess.Popen(['open', exePath_Controller])
    else:
        print("Running as main_Controller.py")

if __name__ == "__main__":
    runPingController()