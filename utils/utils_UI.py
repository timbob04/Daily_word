class DefineFontSizes:
    def __init__(self,QApplication,dep):
        # Input values
        self.QApplication = QApplication
        self.dep = dep
        # Default values
        self.extraScaleFactor = 1.33
        self.fontScalers = { "small":0.8, "default":1, "large":1.3 }
        # Constructor functions
        self.getSystemDefaultFont()
        self.getScreenDPI()
        self.defineDefaultFontSize()

    def getSystemDefaultFont(self):
        self.default_font = self.QApplication.font()

    def getScreenDPI(self):    
        screen = self.QApplication.primaryScreen()
        dpi = screen.logicalDotsPerInch()
        self.DPIscaleFactor = dpi / 96  # Normalize to 96 (standard) DPI
        
    def defineDefaultFontSize(self):         
        self.defaultFontSize = self.default_font.pointSize()*self.DPIscaleFactor*self.extraScaleFactor

class DefineUIsizes:
    def __init__(self,appSizeOb):
        # Input values
        self.appSizeOb = appSizeOb
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
            name: obj * self.appSizeOb.sentenceWidth 
            for name, obj in self.sizesInputs.items()
        }

    def setSizesAsObjectAttributes(self):
        for name, obj in self.sizesScaled.items():
            setattr(self, name, obj)


class StaticText:
    def __init__(self, dep, window, fontSize, text, textAlignment, textPos):
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
        # Initialize some variables
        self.positionAdjust = None
        self.Vcenter = None
        self.Hcenter = None    
        # Constructor functions
        self.makeFont()
        self.getActualPosition()
        self.makeTextObject()

    def makeFont(self):
        self.font = self.dep.QFont()
        self.font.setPointSizeF(self.fontSize)
        self.fontMetrics = self.dep.QFontMetrics(self.font) 

    def getActualPosition(self):
        if self.textPos[2] > 0:
            bounding_rect = self.fontMetrics.boundingRect(0,0,int(self.textPos[2]),int(self.textPos[3]), self.textAlignment | self.dep.Qt.TextWordWrap, self.text)       
        else:
            bounding_rect = self.fontMetrics.boundingRect(0,0,int(self.textPos[2]),int(self.textPos[3]), self.textAlignment, self.text)       
        self.positionAdjust = [int(self.textPos[0]), int(self.textPos[1]), int(bounding_rect.width()), int(bounding_rect.height())]

    def makeTextObject(self):
        self.textOb = self.dep.QLabel(self.text, self.window)
        self.textOb.setWordWrap(self.wordWrap)    
        self.textOb.setGeometry(*self.positionAdjust)
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
    def __init__(self, dep, window, fonts, fontSize, text, position, maxHeight):
        # Inputs
        self.dep = dep
        self.window = window
        self.fonts = fonts
        self.fontSize = fontSize 
        self.position = position
        self.maxHeight = maxHeight
        self.maxWidth = position[2]  # Width from position tuple
        # Default parameters
        self.textAlignment = dep.Qt.AlignLeft
        self.setWordWrap = True
        self.text = dep.softHyphenateLongWords(text)
        # Initializer methods
        self.makeFont()
        self.getTextHeight()   
        self.makeScrollableText()     
        
    def makeFont(self):
        self.font = self.dep.QFont()
        fontSize = self.fonts.defaultFontSize * self.fonts.fontScalers[self.fontSize]
        self.font.setPointSizeF(fontSize) 
        self.fontMetrics = self.dep.QFontMetrics(self.font)

    def getTextHeight(self):
        boundingRect = self.fontMetrics.boundingRect(0, 0, int(self.position[2]), 0, self.textAlignment | self.dep.Qt.TextWordWrap, self.text)     
        self.textHeight = boundingRect.height()
        
    def makeScrollableText(self):
        if self.textHeight > self.maxHeight:
            self.makeVerticalScrollBar()
            self.makeTextObject(in_scroll_area=True)
            self.scroll_area.setWidget(self.t_wordOfDay.textOb)
            return self.scroll_area
        else:
            self.makeTextObject(in_scroll_area=False)
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
                                              self.fonts.defaultFontSize*self.fonts.fontScalers[self.fontSize], 
                                              self.text, self.textAlignment, position)

    def showTextObject(self):
        if self.textHeight > self.maxHeight:
            self.scroll_area.show()
        self.t_wordOfDay.showTextObject()


def centerWindowOnScreen(window,QApplication):
    frameGm = window.frameGeometry()
    screen = QApplication.primaryScreen()
    centerPoint = screen.availableGeometry().center()
    frameGm.moveCenter(centerPoint)
    window.move(frameGm.topLeft())         

class AppSize:
    def __init__(self,dep,fonts,sentence,numLines):
        # Input values  
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
        screen = self.dep.QApplication.primaryScreen()
        self.screenSize = screen.size()
        self.screenWidth = self.screenSize.width()
        self.screenHeight = self.screenSize.height()

