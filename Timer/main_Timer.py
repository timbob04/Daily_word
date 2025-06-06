from datetime import time

def runTimer(timer_wrapper, dep):
    # For checking when the API should be presented
    timingControl = TimingControl(dep)
    
    while True:  
        if timingControl.checkIfTimeToRunProgram():     
            print("Time to run the program")       
            timer_wrapper.request_start.emit('dailyWordApp')  # Emit signal to start DailyWordApp
        dep.time.sleep(5)

class TimingControl():
    def __init__(self, dep):
        self.dep = dep

    def checkIfTimeToRunProgram(self):
        if self.checkIfTimeIsReached() and not self.isDateLastRunToday():
            self.writeNewDate() # Update the dateLastRun text file
            return True           
            
    def checkIfTimeIsReached(self):
        # Get the current time of day
        current_time = self.dep.datetime.now().time()
        # Get time to show word
        timeToShowDailyWord = self.getTimeToShowAPI()
        # Compare the current time to the target time
        return timeToShowDailyWord <= current_time <= time(23, 59)  # time(hour, minute, second)
    
    def getTimeToShowAPI(self):
        time_dir = self.getTimeToRunApplicationPath()
        with open(time_dir, 'r') as file:
            time_str = file.read().strip()  # Read the time string and remove any extra whitespace
            return self.dep.datetime.strptime(time_str, "%H:%M").time()
        
    def getTimeToRunApplicationPath(self):
        # Get path of accessory files
        root_dur, _ = self.dep.getBaseDir(self.dep.sys, self.dep.os)
        accessoryFiles_dir = self.dep.os.path.join(root_dur, 'accessoryFiles')
        # Path to json file for words and definitions
        return self.dep.os.path.join(accessoryFiles_dir, 'timeToRunApplication.txt')    
    
    def isDateLastRunToday(self):
        dateLastRun = self.readDateLastRun()
        if dateLastRun is None:
            return False
        return dateLastRun == self.dep.datetime.now().date()

    def readDateLastRun(self):
        file_path = self.getDateLastRunPath()
        if not self.dep.os.path.exists(file_path):
            return None  # Return None if file doesn't exist
        with open(file_path, 'r') as file:
            try:
                date_str = file.read().strip()
                return self.dep.datetime.strptime(date_str, "%m/%d/%Y").date()
            except Exception:
                return None
            
    def getDateLastRunPath(self):             
        root_dur, _ = self.dep.getBaseDir(self.dep.sys, self.dep.os)
        common_dir = self.dep.os.path.join(root_dur, 'accessoryFiles')    
        return self.dep.os.path.join(common_dir, 'dateLastRun.txt')          
        
    def writeNewDate(self):
        file_path = self.getDateLastRunPath()
        current_date = self.dep.datetime.now().strftime("%m/%d/%Y")  
        with open(file_path, 'w') as file:
            file.write(current_date)


    
