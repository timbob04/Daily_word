import socket
import sys
import os
import platform
import subprocess
from utils.utils import getBaseDir
import time
import threading
from Controller.main_Controller import startController
from utils.utils import PortListener, PortSender, StoreDependencies

# Store a reference to each dependency above
dep = StoreDependencies(globals())

def runControllerExecutable():
    # First check to see if this script is running as a .py or executable
    runingCodeFromExecutable = getattr(sys, 'frozen', False) # The 'frozen' attribute in sys is set to True if the script is running as an executable
    if runingCodeFromExecutable:
        root_dir, _ = getBaseDir(sys, os)
        system = platform.system()
        if system == "Windows":
            flags = (subprocess.CREATE_NEW_PROCESS_GROUP |
                subprocess.DETACHED_PROCESS)   # launch *detached*
            exePath_Controller = os.path.join(root_dir, "bin" , "main_Controller" , "main_Controller.exe")
            subprocess.Popen(exePath_Controller, creationflags=flags)
        elif system == "Darwin":
            print("\nRunning executable on Mac")
            exePath_Controller = os.path.join(root_dir, "bin", "main_Controller.app")
            subprocess.Popen(['open', exePath_Controller])
    else:
        print("Running as main_Controller.py")

def loadingMessage():
    print("\n")

    # print("Loading ")
    # while True:
    #     print(".", end="", flush=True)
    #     time.sleep(1)

    # Option 2: Revolving dash
    chars = ['-', '\\', '|', '/']
    i = 0
    while True:
        print(f"\rLoading {chars[i]}", end="", flush=True)
        i = (i + 1) % len(chars)
        time.sleep(0.2)

if __name__ == "__main__":

    # threading.Thread(target=loadingMessage, daemon=True).start()
    # time.sleep(4)

    # # Start loading message in a daemon thread
    # threading.Thread(target=loadingMessage, daemon=True).start()

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