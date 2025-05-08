class CheckIfTimeEnteredCorrectly:
    def __init__(self, dep, hoursOb, minutesOb, textOb):
        self.dep = dep
        self.hoursOb = hoursOb
        self.minutesOb = minutesOb
        self.textOb = textOb
        # Default values
        self.correctYN_HH = False
        self.correctYN_MM = False
        self.correctYN_both = False  
        self.startButtonHasBeenPressed = False # becomes true once the Start button is pressed
        self.timeEntered = None

    def startButtonPressed(self, checked=False):
        self.startButtonHasBeenPressed = True
        self.showOrHideText()
        print('start button pressed')

    def checkTime_HH(self):
        if self.dep.re.fullmatch(r'([0-1]?[0-9]|2[0-3])', self.hoursOb.tb.text()): # is the hour entered between 00 and 23
            self.correctYN_HH = True
            print('HH is correct')
        else: 
            self.correctYN_HH = False
            print('HH is false')
        self.bothCorrect()    
        self.showOrHideText()

    def checkTime_MM(self):
        if self.dep.re.fullmatch(r'([0-5]?[0-9])', self.minutesOb.tb.text()): # is the minute entered between 00 and 59
            self.correctYN_MM = True
            print('MM is correct')
        else: 
            self.correctYN_MM = False
            print('MM is false')
        self.bothCorrect()
        self.showOrHideText()

    def bothCorrect(self):
        if self.correctYN_HH & self.correctYN_MM:
            self.correctYN_both = True
            print('both are correct\n\n')
        else:
            self.correctYN_both = False
            print('one or both are false\n\n')

    def showOrHideText(self):        
        if not self.startButtonHasBeenPressed:
            return
        
        if self.correctYN_both:
            self.textOb.hideTextObject()
        else:
            self.textOb.showTextObject()