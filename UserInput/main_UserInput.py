import socket
import sys
import os
import platform
import subprocess
from utils.utils import getBaseDir
import time
import threading
from Controller.main_Controller import startController

class PortListener:
    def __init__(self):
        # Parameters
        self.portNum = None
        self.portNumFileName_UserInput = 'portNum_UserInput.txt' # Which text file to write the port number that the Controller will read and send pings
        self.responseReceived = False
        # Constructor methods
        self.startPortListener()    

    # Commuication with other executables; listener function - to listen for messages from port
    def startPortListener(self):
        portNum = self.findOpenPort()
        self.savePortNumberToFile(portNum)
        if portNum is not None:
            self.portListener(portNum)
        else:
            print("Port listener setup failed")

    def findOpenPort(self, startingPort=5000, maxTries=5000):
        # First read the Controller's port number to avoid it
        root_dir, _ = getBaseDir(sys, os)
        accessoryFiles_dir = os.path.join(root_dir, 'accessoryFiles')
        controllerPortFile = os.path.join(accessoryFiles_dir, 'portNum_Controller.txt')
        controllerPort = None
        if os.path.exists(controllerPortFile):
            with open(controllerPortFile, "r") as f:
                controllerPort = int(f.read().strip())

        port = None
        for port in range(startingPort, startingPort + maxTries):
            # Skip if this is the Controller's port
            if port == controllerPort:
                continue
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(("127.0.0.1", port))
                    return port
                except OSError:
                    continue       

    def savePortNumberToFile(self, portNum):
        # Get path to text file in accessoryFiles folder to save port number
        root_dir, _ = getBaseDir(sys, os)
        accessoryFiles_dir = os.path.join(root_dir, 'accessoryFiles')
        curFilePath = os.path.join(accessoryFiles_dir, self.portNumFileName_UserInput)
        with open(curFilePath, "w") as f:
            f.write(str(portNum))     

    def portListener(self, portNum):
        print(f"Listening on port {portNum}")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('127.0.0.1', portNum))
        self.socket.listen(1)
        print(f"Listening on port {portNum}")

    def waitForPingBack(self, timeout=5):
        try:
            self.socket.settimeout(timeout)
        except OSError:  # Socket is closed
            self.startPortListener()  # Restart the listener
            self.socket.settimeout(timeout)
            
        try:
            conn, addr = self.socket.accept()  # Blocks until ping received or timeout
            data = conn.recv(1024)
            if data:
                self.responseReceived = True
            conn.close()
        except socket.timeout:
            self.responseReceived = False
        finally:
            self.socket.close()

class PortSender:
    def __init__(self):
        # Parameters
        self.portNum = None
        self.messageSent = False        
        self.portNumFileName_Controller = 'portNum_Controller.txt' # Which text file to read the port number to send pings to the Controller
        # WARNING: Do not use the same port number as portNum_UserInput.txt - this will cause the script to receive its own pings
        # Constructor methods    

    def sendPingToController(self):
        self.readPortNumber()
        if self.portNum is None:
            return
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:    
            # print("Trying to send ping...")
            self.socket.connect(('127.0.0.1', self.portNum))
            self.socket.sendall(b'pingFromUserInputExecutable')
            self.messageSent = True
            # print("Message sent!")
        except Exception:
            pass
        finally:
            self.socket.close()

    def readPortNumber(self):
        # Get path to text file in accessoryFiles folder to save port number
        root_dir, _ = getBaseDir(sys, os)
        accessoryFiles_dir = os.path.join(root_dir, 'accessoryFiles')
        curFilePath = os.path.join(accessoryFiles_dir, self.portNumFileName_Controller)
        if os.path.exists(curFilePath):
            with open(curFilePath, "r") as f:
                self.portNum = int(f.read().strip())  # Convert to integer and strip any whitespace
        else:
            self.portNum = None

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
            exePath_Controller = os.path.join(root_dir, "bin", "main_Controller.app", "Contents", "MacOS", "main_Controller")
            subprocess.Popen(['open', '-a', 'Terminal', exePath_Controller])
    else:
        print("Running as main_Controller.py")

def loadingMessage():
    print("Loading")
    while True:
        print(".", end="", flush=True)
        time.sleep(1)

if __name__ == "__main__":

    # # Start loading message in a daemon thread
    # threading.Thread(target=loadingMessage, daemon=True).start()

    # Set up a port listener for receiving messages from the Controller
    portListener = PortListener()
    # Set up a port sender for sending messages to the Controller
    portSender = PortSender()
    # Send ping to Controller
    portSender.sendPingToController()
    # Wait for response from Controller
    portListener.waitForPingBack(4)
    if portListener.responseReceived:
        print("Response received from Controller")
    else:
        print("No response received from Controller.  Running its executable...")
        runControllerExecutable()
        portListener.waitForPingBack(10) # instead of pinging the Controller again, just have the Controller ping this executable once it starts up
        if portListener.responseReceived:
            print("Response received from Controller")
        else:
            print("No response received from Controller after running its executable. Fix stuff.")

    