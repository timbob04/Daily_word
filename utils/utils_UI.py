class DefineFontSizes:
    def __init__(self,app,dep):
        # Input values
        self.app = app
        self.dep = dep
        # Default values
        self.fontScalers = { "small":0.8, "default":1, "large":1.3 }        
        # Constructor functions
        self.getSystemDefaultFont()
        self.getBaseDPI()
        self.getScreenDPI()
        self.getExtraScaleFactor()
        self.defineDefaultFontSize()

    def getSystemDefaultFont(self):
        self.default_font = self.app.font()

    def getBaseDPI(self):
        self.baseDPI = 96 if self.dep.sys.platform == "win32" else 72

    def getScreenDPI(self):    
        screen = self.app.primaryScreen()
        dpi = screen.logicalDotsPerInch()
        self.DPIscaleFactor = dpi / self.baseDPI  # Normalize to OS's standard dpi

    def getExtraScaleFactor(self):
        self.extraScaleFactor = 1.33 if self.dep.sys.platform != "win32" else 1.67

    def defineDefaultFontSize(self):         
        self.defaultFontSize = self.default_font.pointSize()*self.DPIscaleFactor*self.extraScaleFactor

class DefineUIsizes:
    def __init__(self,appSizeOb):
        # Input values
        self.appSizeOb = appSizeOb
        # Default values
        self.toggleWidth = None
        # Initializer methods
        self.defineSizes()
        self.defineSizesRelToAppSize()
        self.setSizesAsObjectAttributes()

    def defineSizes(self):    
        self.sizesInputs = {
        "pad_small": 0.01,
        "pad_medium": 0.02,
        "pad_large": 0.04,
        }

    def defineSizesRelToAppSize(self):  
        # Create new dictionary with scaled values
        self.sizesScaled = {
            name: obj * min(self.appSizeOb.sentenceWidth,self.appSizeOb.screenWidth) 
            for name, obj in self.sizesInputs.items()
        }

    def setSizesAsObjectAttributes(self):
        for name, obj in self.sizesScaled.items():
            setattr(self, name, obj)

class StaticText:
    def __init__(self, dep, window, fontSize, text, textAlignment, textPos, italic=False, bold=False):
        # Input values
        self.dep = dep
        self.window = window
        self.fontSize = fontSize
        self.text = text
        self.textAlignment = textAlignment
        self.textPos = textPos
        # Default values        
        self.color = 'black'    
        self.wordWrap = True    
        self.italic = italic
        self.bold = bold
        # Initialize some variables
        self.positionAdjust = None
        self.Vcenter = None
        self.Hcenter = None    
        # Constructor functions
        self.makeFont()
        self.getActualPosition()

    def makeFont(self):
        self.font = self.dep.QFont()
        self.font.setPointSizeF(self.fontSize)
        self.font.setItalic(self.italic)
        self.font.setBold(self.bold)
        self.fontMetrics = self.dep.QFontMetrics(self.font) 

    def getActualPosition(self):
        if self.textPos[2] > 0:
            bounding_rect = self.fontMetrics.boundingRect(0,0,int(self.textPos[2]),int(self.textPos[3]), self.textAlignment | self.dep.Qt.TextWordWrap, self.text)       
        else:
            bounding_rect = self.fontMetrics.boundingRect(0,0,0,0, self.textAlignment, self.text)       
        self.positionAdjust = [int(self.textPos[0]), int(self.textPos[1]), int(bounding_rect.width()), int(bounding_rect.height())]
    
    def makeTextObject(self):
        self.textOb = self.dep.QLabel(self.text, self.window)
        self.textOb.setWordWrap(self.wordWrap)    
        self.textOb.setGeometry(*(int(x) for x in self.positionAdjust))
        self.textOb.setFont(self.font)
        self.textOb.setAlignment(self.textAlignment)
        self.textOb.setStyleSheet(f"QLabel {{ color : {self.color}; }}")        
        self.textOb.hide()
        return self.textOb   

    def getVandHcenter(self):
        self.Hcenter = self.positionAdjust[0] + self.positionAdjust[2]/2
        self.Vcenter = self.positionAdjust[1] + self.positionAdjust[3]/2

    def centerAlign_V(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)

    def centerAlign_H(self):
        self.positionAdjust[0] = int(self.positionAdjust[0] - self.positionAdjust[2]/2)

    def alignBottom(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3])
    
    def showTextObject(self):
        self.textOb.show()

    def hideTextObject(self):
        self.textOb.hide()

class MakeTextWithMaxHeight:
    def __init__(self, dep, window, fontSize, text, position, maxHeight, italic=False, bold=False):
        # Inputs
        self.dep = dep
        self.window = window
        self.fontSize = fontSize  # This is already the calculated font size
        self.position = position
        self.maxHeight = maxHeight
        self.maxWidth = position[2]
        # Default parameters
        self.textAlignment = dep.Qt.AlignLeft
        self.setWordWrap = True
        self.text = dep.softHyphenateLongWords(text)
        # Font style defaults
        self.italic_state = italic
        self.bold_state = bold
        # Initializer methods
        self.makeFont()
        self.getTextHeight()     

    def makeFont(self):
        self.font = self.dep.QFont()
        self.font.setPointSizeF(self.fontSize)  # Use the direct font size
        self.font.setItalic(self.italic_state)
        self.font.setBold(self.bold_state)
        self.fontMetrics = self.dep.QFontMetrics(self.font)

    def getTextHeight(self):
        boundingRect = self.fontMetrics.boundingRect(0, 0, int(self.position[2]), 0, self.textAlignment | self.dep.Qt.TextWordWrap, self.text)     
        self.textHeight = boundingRect.height()
        
    def makeScrollableText(self):
        if self.textHeight > self.maxHeight:
            self.makeVerticalScrollBar()
            self.makeTextObject(in_scroll_area=True)
            self.scroll_area.setWidget(self.t_wordOfDay.textOb)
            # Update position for scroll area
            self.position = [self.scroll_area.x(), self.scroll_area.y(), 
                           self.scroll_area.width(), self.scroll_area.height()]
        else:
            self.makeTextObject(in_scroll_area=False)
            # Update position for text object
            self.position = self.t_wordOfDay.positionAdjust
            return self.t_wordOfDay.textOb
    
    def makeVerticalScrollBar(self):
        self.scroll_area = self.dep.QScrollArea(self.window)
        self.scroll_area.setWidgetResizable(True)             
        self.scroll_area.setHorizontalScrollBarPolicy(self.dep.Qt.ScrollBarAlwaysOff)  
        self.scroll_area.setVerticalScrollBarPolicy(self.dep.Qt.ScrollBarAlwaysOn)
        # Set geometry for scroll area
        x, y, width, _ = self.position
        self.scroll_area.setGeometry(int(x), int(y), int(width), int(self.maxHeight))
        self.scroll_area.hide()
        
    def makeTextObject(self, in_scroll_area):
        if in_scroll_area:
            # For scroll area, create widget that can be larger than visible area
            position = [0, 0, self.maxWidth, self.textHeight]
            parent = self.scroll_area
        else:
            # For normal display, use original position
            position = self.position
            parent = self.window
            
        self.t_wordOfDay = self.dep.StaticText(self.dep, parent, 
                                              self.fontSize,  # Use fontSize directly
                                              self.text, self.textAlignment, position, italic=self.italic_state, bold=self.bold_state)
        self.t_wordOfDay.makeTextObject()

    def showTextObject(self):
        if self.textHeight > self.maxHeight:
            self.scroll_area.show()
        self.t_wordOfDay.showTextObject()

    def hideTextObject(self):
        if self.textHeight > self.maxHeight:
            self.scroll_area.hide()
        self.t_wordOfDay.hideTextObject()

def centerWindowOnScreen(window,app):
    frameGm = window.frameGeometry()
    screen = app.primaryScreen()
    centerPoint = screen.availableGeometry().center()
    frameGm.moveCenter(centerPoint)
    window.move(frameGm.topLeft())         

class AppSize:
    def __init__(self,app,dep,fonts,sentence,numLines):
        # Input values  
        self.app = app
        self.dep = dep        
        self.fonts = fonts
        self.sentence = sentence
        self.numLines = numLines
        # Constructor functions
        self.makeFont()
        self.getSentenceWidthAndHeight()
        self.getAppHeight()
        self.getScreenSize()
        
    def makeFont(self):
        self.font = self.dep.QFont()
        fontSize = self.fonts.defaultFontSize * self.fonts.fontScalers["default"]
        self.font.setPointSizeF(fontSize)

    def getSentenceWidthAndHeight(self):
        self.fontMetrics = self.dep.QFontMetrics(self.font)
        boundingRect = self.fontMetrics.boundingRect(self.sentence)
        self.sentenceWidth = boundingRect.width()
        self.sentenceHeight = boundingRect.height()
        
    def getAppHeight(self):
        self.lineSpacing = self.fontMetrics.lineSpacing() 
        self.appHeight = self.lineSpacing * self.numLines

    def getScreenSize(self):
        screen = self.app.primaryScreen()
        screenSize = screen.size()
        self.screenWidth = screenSize.width()
        self.screenHeight = screenSize.height()

class AppBoundaries:
    def __init__(self):
        self.bottom = 0
        self.right = 0

    def setNewBoundaries(self, bottom=None, right=None, store=None):
        if bottom is not None:
            self.bottom = max(self.bottom, bottom)
        if right is not None:
            self.right = max(self.right, right)
        if store:
            for key, value in store.items():
                setattr(self, key, value)

class PushButton:
    def __init__(self, dep, window, fontSize, text, position, italic=False, bold=False):
        # Input values
        self.dep = dep
        self.window = window
        self.fontSize = fontSize
        self.text = text        
        self.position = position
        self.italic = italic
        self.bold = bold
        # Default values
        self.buttonPaddingPer = 0.5  # padding is determined as a multiplier of a single letter's width
        # Constructor functions
        self.makeFont()
        self.getButtonPaddingSize()
        self.getButtonPosition()

    def makeFont(self):
        self.font = self.dep.QFont()
        self.font.setPointSizeF(self.fontSize)
        self.font.setItalic(self.italic)
        self.font.setBold(self.bold)
        self.fontMetrics = self.dep.QFontMetrics(self.font) 

    def getButtonPaddingSize(self):   
        boundingRect = self.fontMetrics.boundingRect(0, 0, 0, 0, self.dep.Qt.AlignHCenter, "0") 
        self.letterWidth = boundingRect.width()
        self.padding = int(self.letterWidth * self.buttonPaddingPer)

    def getButtonPosition(self):
        # Calculate available width for text (total width minus padding)
        if self.position[2] > 0:
            # If width is constrained, account for padding in available space
            available_width = int(self.position[2]) - (2 * self.padding)
            bounding_rect = self.fontMetrics.boundingRect(
                0, 0, available_width, 0, 
                self.dep.Qt.AlignCenter | self.dep.Qt.TextWordWrap, 
                self.text
            )
            # Use the constrained width for button
            button_width = int(self.position[2])
        else:
            # If no width constraint, get natural text width
            bounding_rect = self.fontMetrics.boundingRect(
                0, 0, 0, 0, 
                self.dep.Qt.AlignCenter, 
                self.text
            )
            # Add padding to both sides of text width plus a small extra margin for anti-aliasing
            button_width = bounding_rect.width() + (2 * self.padding) + 6  # Added 4px extra margin
        
        # Height always gets padding added plus a small extra margin for anti-aliasing
        button_height = bounding_rect.height() + (2 * self.padding) + 6  # Added 4px extra margin
        
        # Set the button bounds
        self.positionAdjust = [
            int(self.position[0]),
            int(self.position[1]),
            int(button_width),
            int(button_height)
        ]

    def getVandHcenter(self):
        self.Hcenter = self.positionAdjust[0] + self.positionAdjust[2]/2
        self.Vcenter = self.positionAdjust[1] + self.positionAdjust[3]/2

    def centerAlign_V(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)

    def centerAlign_H(self):
        self.positionAdjust[0] = int(self.positionAdjust[0] - self.positionAdjust[2]/2)

    def rightAlign(self):
        self.positionAdjust[0] = self.positionAdjust[0] - self.positionAdjust[2] 

    def bottomAlign(self):
        self.positionAdjust[1] = self.positionAdjust[1] - self.positionAdjust[3]

    def makeButton(self):
        self.button = self.dep.QPushButton(self.text, self.window)
        self.button.setGeometry(*(int(x) for x in self.positionAdjust))    
        self.button.setFont(self.font)
        if self.position[2] > 0:
            self.button.setWordWrap(True)
        self.button.setStyleSheet(self.dep.buttonStyle(self.padding))
        self.button.hide()
        return self.button

    def showButton(self):
        if hasattr(self, 'button'):
            self.button.show()

    def hideButton(self):
        if hasattr(self, 'button'):
            self.button.hide()

class Toggle:
    def __init__(self,dep,window,sizes,center,middle,toggleStatus):
        self.dep = dep
        self.window = window
        self.sizes = sizes
        self.center = center
        self.middle = middle
        self.toggleStatus = toggleStatus
        # Constructor functions
        self.createToggle()
        self.getToggleSize()
        self.getXandYPoints()
        self.setTogglePosition()
        self.applyToggleStyle()

    def createToggle(self):
        self.toggle = self.dep.QCheckBox('',self.window)
        self.setToggleStatus(self.toggleStatus)
        self.toggle.hide()

    def setToggleStatus(self,status):
        self.toggle.setChecked(status)

    def getToggleSize(self):
        if self.sizes.toggleWidth is None:
            style = self.toggle.style()
            defaultSize = style.pixelMetric(self.dep.QStyle.PM_IndicatorWidth, None, self.toggle)
            self.sizes.toggleWidth = defaultSize * 1

    def getXandYPoints(self):
        self.xPoint = self.center - self.sizes.toggleWidth/2
        self.yPoint = self.middle - self.sizes.toggleWidth/2

    def setTogglePosition(self):
        self.position = [self.xPoint,self.yPoint,self.sizes.toggleWidth,self.sizes.toggleWidth]
        self.toggle.setGeometry(*(int(x) for x in self.position))

    def applyToggleStyle(self):
        self.toggle.setStyleSheet(self.dep.toggleStyle(self.sizes.toggleWidth))

    def showToggle(self):
        self.toggle.show()

    def hideToggle(self):
        self.toggle.hide() 

def makeScrollAreaForCentralWidget(dep, window, container):
    scrollArea = dep.QScrollArea()
    scrollArea.setWidget(container)
    scrollArea.setHorizontalScrollBarPolicy(dep.Qt.ScrollBarAsNeeded)
    scrollArea.setVerticalScrollBarPolicy(dep.Qt.ScrollBarAsNeeded)
    scrollArea.setAlignment(dep.Qt.AlignCenter)
    scrollArea.setContentsMargins(0, 0, 0, 0)
    window.setCentralWidget(scrollArea)
   
def resizeWindow(window, width, height, appSizeOb, percentage=0.03):
    # Determine desired window size, which is a litte bigger than the contents
    widthOfWindowWithContents = width + width * percentage
    heightOfWindowWithContents = height + height * percentage

    # Make sure the window is not bigger than the screen
    windowFinalWidth = min(widthOfWindowWithContents,appSizeOb.screenWidth)
    windowFinalHeight = min(heightOfWindowWithContents,appSizeOb.screenHeight)

    window.resize(int(windowFinalWidth),int(windowFinalHeight))
           