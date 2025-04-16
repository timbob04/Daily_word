import socket
import sys
import os

from utils.utils import getBaseDir
from utils.utils import StoreDependencies

dep = StoreDependencies(globals())

def getPortNumber():
    portNum = None
    # Get path to text file in accessoryFiles folder that has port number to communicate with controller
    baseDir = getBaseDir(dep.sys, dep.os)
    accessoryFiles_dir = os.path.join(baseDir, '..', 'accessoryFiles')
    curFilePath = os.path.join(accessoryFiles_dir, 'portNum_1.txt')
    # Read port number from file
    if os.path.exists(curFilePath):
        with open(curFilePath, "r") as f:
            portNum = int(f.read().strip())  # Convert to integer and strip any whitespace
    return portNum

def sendPing(portNum):
    if portNum is not None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Trying to send ping...")
            # Need some stuff to handle exceptions here
            s.connect(('127.0.0.1', portNum))
            s.sendall(b'ping')
            print("Message sent!")

if __name__ == "__main__":
    portNum = getPortNumber()
    sendPing(portNum)