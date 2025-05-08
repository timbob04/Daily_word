import time
import sys
from datetime import datetime
import os
from utils.utils import getBaseDir

# So installed executables can find their dependencies
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), "_internal"))

def consoleMessage_startProgram():

    programRunTimeOb = ReadProgramRunTime()

    time.sleep(1)
    print('\nThe program will now run in the background')
    time.sleep(2)    
    print(f'\nA word and its definition will appear daily at {programRunTimeOb.time.strftime("%H:%M")}')    
    time.sleep(2.5)
    print("\nTo stop or edit the program, click on the same 'Daily Word Definition' icon you used to start the program")
    time.sleep(5)
    print('\n---- Goodbye ----\n')
    time.sleep(2)

class ReadProgramRunTime():
    def __init__(self):
        self.time = None
        self.getTime()

    def getTime(self):
        time_dir = self.getTimeFilePath()
        with open(time_dir, 'r') as file:
            time_str = file.read().strip()  # Read the time string and remove any extra whitespace
            self.time = datetime.strptime(time_str, "%H:%M").time()
        
    def getTimeFilePath(self):
        # Get path of accessory files
        base_dir = getBaseDir(sys, os)
        accessoryFiles_dir = os.path.join(base_dir, '..', 'accessoryFiles')
        # Path to json file for words and definitions
        return os.path.join(accessoryFiles_dir, 'timeToRunApplication.txt')                      

if __name__ == "__main__":    
    consoleMessage_startProgram()    

