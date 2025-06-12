class SetWindowTitle():
    def __init__(self, window, datetime, dep):
        # Inputs
        self.window = window
        self.datetime = datetime   
        self.dep = dep
        # Initializer methods
        self.getTodaysDay()
        self.getSuffixForTodaysDay()
        self.formatTitleToIncludeDay()
        self.setTitle()
        self.getTitleWidth()

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
        self.title = "Word of the day.  " + self.dateForTitle
        self.window.setWindowTitle(self.title)     

    def getTitleWidth(self):
        # Get the title text width using QFontMetrics
        font = self.window.font()
        fontMetrics = self.dep.QFontMetrics(font)
        self.titleTextWidth = fontMetrics.horizontalAdvance(self.title)
        
        # Get the width of the window control buttons (close, minimize, zoom)
        style = self.window.style()
        # Get the width of a single button
        buttonWidth = style.pixelMetric(self.dep.QStyle.PM_TitleBarButtonSize)
        # On macOS, there are 3 buttons (close, minimize, zoom)
        self.controlButtonsWidth = buttonWidth * 3
        # Add some padding for the buttons (using standard spacing)
        self.controlButtonsWidth += 50 # Standard padding for macOS window controls
        
        # Total width including text and controls
        self.totalTitleWidth = self.titleTextWidth + self.controlButtonsWidth
        
