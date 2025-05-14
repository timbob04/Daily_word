import socket
import sys
import os
import platform
import subprocess
from utils.utils import getBaseDir
import time
import threading
from Controller.main_Controller import startController

class PingController:
    def __init__(self):
        # Parameters
        self.portNum = None
        self.messageSent = False
        self.portNumFileName = 'portNum_1.txt' # Which text file to read the port number to communicate with Controller
        self.responseReceived = False
        # Constructor methods
        self.getPortNumber()
        self.sendPingToController()
        self.waitForResponseFromController()

    def getPortNumber(self):
        # Get path to text file in accessoryFiles folder that has port number to communicate with controller
        baseDir = getBaseDir(sys, os)
        accessoryFiles_dir = os.path.join(baseDir, '..', 'accessoryFiles')
        curFilePath = os.path.join(accessoryFiles_dir, self.portNumFileName)
        # Read port number from file
        if os.path.exists(curFilePath):
            with open(curFilePath, "r") as f:
                self.portNum = int(f.read().strip())  # Convert to integer and strip any whitespace

    def sendPingToController(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # print("Trying to send ping...")
            self.socket.connect(('127.0.0.1', self.portNum))
            self.socket.sendall(b'pingFromUserInputExecutable')
            self.messageSent = True
            # print("Message sent!")
        except Exception:
            pass

    def waitForResponseFromController(self, timeout=5):
        if self.messageSent:
            self.socket.settimeout(timeout) # Listen for a response from the Controller for 'timeout' seconds
            try:
                response = self.socket.recv(1024)  # Listen to Controller
                if response == b'pingFromController':
                    # print("Received expected response: pingFromController")
                    self.responseReceived = True
                else:
                    # print("Received unexpected response: ", response)
                    pass
            except socket.timeout:
                # print("No response received within the timeout period.")
                pass
            finally:
                self.socket.close()  # Ensure the socket is closed no matter what       

def runControllerExecutable():
    # First check to see if this script is running as a .py or executable
    runingCodeFromExecutable = getattr(sys, 'frozen', False) # The 'frozen' attribute in sys is set to True if the script is running as an executable
    if runingCodeFromExecutable:
        baseDir = getBaseDir(sys, os)
        system = platform.system()
        if system == "Windows":
            flags = (subprocess.CREATE_NEW_PROCESS_GROUP |
                subprocess.DETACHED_PROCESS)   # launch *detached*
            subprocess.Popen([os.path.join(baseDir, "main_Controller.exe")], creationflags=flags)
        elif system == "Darwin":
            print("\nRunning executable on Mac")
            controller_path = os.path.join(baseDir, "main_Controller")
            subprocess.Popen(['open', '-a', 'Terminal', controller_path])
    else:
        # print("Running as main_Controller.py")
        startController()

def loadingMessage():
    print("Loading")
    while True:
        print(".", end="", flush=True)
        time.sleep(1)

if __name__ == "__main__":
    # Start a thread to display a loading message
    threading.Thread(target=loadingMessage,daemon=True).start()
    # Ping the Controller
    controller = PingController()
    if not controller.responseReceived:
        # print("No response received from Controller. Running its executable...")
        runControllerExecutable()

    time.sleep(5) # for testing - to see if the loading message in its own console opens and then closes after this 10 seconds, even if the Controller and associated things are running