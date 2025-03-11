class SetWindowTitle():
    def __init__(self,window,datetime):
        # Inputs
        self.window = window
        self.datetime = datetime        
        # Initializer methods
        self.getTodaysDay()
        self.getSuffixForTodaysDay()
        self.formatTitleToIncludeDay()
        self.setTitle()

    def getTodaysDay(self):
        self.todaysDate = self.datetime.now()
        self.todaysDay = self.todaysDate.day

    def getSuffixForTodaysDay(self):
        if 10 <= self.todaysDay <= 20:  # "Teen" numbers always get "th"
            self.suffix = "th"
        else:
            self.suffix = {1: "st", 2: "nd", 3: "rd"}.get(self.todaysDay % 10, "th")

    def formatTitleToIncludeDay(self):        
        day_without_zero = str(self.todaysDay).lstrip("0")  # Remove leading zero
        self.dateForTitle = self.todaysDate.strftime(f"{day_without_zero}{self.suffix} %B %Y")

    def setTitle(self):          
        self.window.setWindowTitle("Word of the day.  " + self.dateForTitle)     
