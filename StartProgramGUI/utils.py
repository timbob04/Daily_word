class CheckIfTimeEnteredCorrectly:
    def __init__(self, dep, hoursOb, minutesOb, textOb, launchMainApp):
        self.dep = dep
        self.hoursOb = hoursOb
        self.minutesOb = minutesOb
        self.textOb = textOb
        self.launchMainApp = launchMainApp
        # Default values
        self.correctYN_HH = False
        self.correctYN_MM = False
        self.correctYN_both = False  
        self.buttonHasBeenPressed = False # becomes true once the Start button is pressed
        self.timeEntered = None

    def buttonPressed(self, checked=False):
        self.buttonHasBeenPressed = True
        self.showOrHideText()
        if self.correctYN_both:
            self.launchMainApp()

    def checkTime_HH(self):
        if self.dep.re.fullmatch(r'([0-1]?[0-9]|2[0-3])', self.hoursOb.tb.text()): # is the hour entered between 00 and 23
            self.correctYN_HH = True
        else: 
            self.correctYN_HH = False
        self.bothCorrect()    
        self.showOrHideText()

    def checkTime_MM(self):
        if self.dep.re.fullmatch(r'([0-5]?[0-9])', self.minutesOb.tb.text()): # is the minute entered between 00 and 59
            self.correctYN_MM = True
        else: 
            self.correctYN_MM = False
        self.bothCorrect()
        self.showOrHideText()

    def bothCorrect(self):
        if self.correctYN_HH & self.correctYN_MM:
            self.correctYN_both = True
            self.storeTimeEntered()
        else:
            self.correctYN_both = False

    def storeTimeEntered(self):
        hh = self.hoursOb.tb.text().zfill(2)
        mm = self.minutesOb.tb.text().zfill(2)
        self.timeEntered = f"{hh}:{mm}"

    def showOrHideText(self):        
        if not self.buttonHasBeenPressed:
            return
        
        if self.correctYN_both:
            self.textOb.hideTextObject()
        else:
            self.textOb.showTextObject()