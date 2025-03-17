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
    def __init__(self):
        # Initializer methods
        self.defineSizes()
        self.setSizesAsObjectAttributes()

    def defineSizes(self):    
        self.sizesInputs = {
        "pad_small": 5,
        "pad_medium": 10,
        "pad_large": 20,
        "maxButtonWidth_small": 100,
        "maxButtonWidth_med": 200,
        "maxButtonWidth_large": 300
        }
        
    def setSizesAsObjectAttributes(self):
        for name, obj in self.sizesInputs.items():
            setattr(self, name, obj)

# Create static text boxes
class StaticText:
    def __init__(self, dep, fontSize, text, textAlignment):
        # Input values
        self.dep = dep
        self.fontSize = fontSize
        self.text = text
        self.textAlignment = textAlignment
        # Default values        
        self.color = 'black'    
        self.wordWrap = True    
        # Initialize some variables
        self.positionAdjust = None
        self.Vcenter = None
        self.Hcenter = None    
        # Constructor functions
    
    def makeTextObject(self):
        textOb = self.dep.QLabel(self.text)
        textOb.setWordWrap(self.wordWrap)    
        font = self.dep.QFont()
        font.setPointSizeF(self.fontSize)  # or .setPointSize(12)
        textOb.setFont(font)
        textOb.setAlignment(self.textAlignment)
        textOb.setStyleSheet(f"QLabel {{ color : {self.color}; }}")        
        textOb.show()
        return textOb       

class MakeTextWithMaxHeight:
    def __init__(self, dep, fonts, fontSize, text, maxWidth, maxHeight):
        # Inputs and default parameters
        self.dep = dep
        self.fonts = fonts
        self.fontSize = fontSize 
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        self.textAlignment = dep.Qt.AlignLeft
        self.setWordWrap = True
        self.text = dep.softHyphenateLongWords(text)
        # Initializer methods
        self.makeFont()
        self.makeDummyTextDoc()   
        self.getHeightOfDummyTextDoc()     
        self.makeTextObject()  
        
    def makeFont(self):
        self.font = self.dep.QFont()
        fontSize = self.fonts.defaultFontSize * self.fonts.fontScalers[self.fontSize]
        self.font.setPointSizeF(fontSize) 
        
    def makeDummyTextDoc(self):      
        self.doc = self.dep.QTextDocument()
        text_option = self.dep.QTextOption(self.textAlignment)
        text_option.setWrapMode(self.dep.QTextOption.WordWrap)
        self.doc.setDefaultTextOption(text_option)
        self.doc.setDefaultFont(self.font)
        self.doc.setTextWidth(self.maxWidth)
        self.doc.setPlainText(self.text)
        
    def getHeightOfDummyTextDoc(self):   
        self.height = self.doc.size().height()  
        
    def makeTextObject(self):
        fontScaler = self.fonts.fontScalers[self.fontSize]        
        t = self.dep.StaticText(self.dep, self.fonts.defaultFontSize*fontScaler, self.text, self.textAlignment)     
        self.t_wordOfDay = t.makeTextObject()
        self.t_wordOfDay.setMaximumWidth(self.maxWidth)
            
    def makeScrollableText(self):
        if self.height > self.maxHeight:
            self.makeVerticalScrollBar()
            self.scroll_area.setWidget(self.t_wordOfDay)
        else:
            self.scroll_area = self.t_wordOfDay
        return self.scroll_area    
    
    def makeVerticalScrollBar(self):
        self.scroll_area = self.dep.QScrollArea()
        self.scroll_area.setWidgetResizable(True)             
        self.scroll_area.setHorizontalScrollBarPolicy(self.dep.Qt.ScrollBarAlwaysOff)  
        self.scroll_area.setVerticalScrollBarPolicy(self.dep.Qt.ScrollBarAlwaysOn) 
        self.scroll_area.setMaximumHeight(self.maxHeight)
        self.scroll_area.show()                
    
def centerWindowOnScreen(window,QApplication):
    frameGm = window.frameGeometry()
    screen = QApplication.primaryScreen()
    centerPoint = screen.availableGeometry().center()
    frameGm.moveCenter(centerPoint)
    window.move(frameGm.topLeft())         

class GetAppSizeUsingSentence:
    def __init__(self,dep,fonts,sentence):
        # Input values  
        self.dep = dep        
        self.fonts = fonts
        self.sentence = sentence
        # Constructor functions
        self.makeFont()
        self.getSentenceWidth()
        self.getScreenSize()
        self.getAppWidth()

    def makeFont(self):
        self.font = self.dep.QFont()
        fontSize = self.fonts.defaultFontSize * self.fonts.fontScalers["default"]
        self.font.setPointSizeF(fontSize)

    def getSentenceWidth(self):
        fontMetrics = self.dep.QFontMetrics(self.font)
        boundingRect = fontMetrics.boundingRect(self.sentence)
        self.sentenceWidth = boundingRect.width()

    def getScreenSize(self):
        screen = self.dep.QApplication.primaryScreen()
        self.screenSize = screen.size()
        self.screenWidth = self.screenSize.width()
        self.screenHeight = self.screenSize.height()

    def getAppWidth(self):
        self.appWidth = min(self.sentenceWidth,self.screenWidth)
