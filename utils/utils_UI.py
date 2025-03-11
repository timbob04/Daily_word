class SystemScalingFactors():
    def __init__(self,dep,app):
        # Inputs
        self.dep = dep
        self.app = app
        # Initializer methods
        self.getScaleFactors()

    def getScaleFactors(self):
        self.dpi_base = 96
        screen = self.app.primaryScreen()
        self.screenDPI = screen.logicalDotsPerInch() * screen.devicePixelRatio()
        # self.fontScaleFactor = self.screenDPI / self.dpi_base
        self.fontScaleFactor = screen.devicePixelRatio()
        self.UIelementsScaleFactor = self.screenDPI / 25.4

class DefineFontSizes:
    def __init__(self,QApplication):
        self.QApplication = QApplication
        self.getSystemDefaultFont()
        self.defineDefaultFontSize()
        self.defineFontScalers()
         
    def getSystemDefaultFont(self):
        self.default_font = self.QApplication.font()
        
    def defineDefaultFontSize(self): 
        scaleFactor = 2   
        self.defaultFontSize = self.default_font.pointSize()*scaleFactor
        
    def defineFontScalers(self):    
        self.fontScalers = { "small":0.8, "default":1, "large":1.3 }

class DefineUIsizes:
    def __init__(self):
        # Initializer methods
        self.defineSizes()

    def defineSizes(self):    
        self.sizesInputs = {
        "padding_small": 10,
        "padding_medium": 20,
        "padding_large": 40,
        "maxButtonWidth_small": 100,
        "maxButtonWidth_med": 200,
        "maxButtonWidth_large": 300
        }

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
        t = self.dep.StaticText(self.dep, self.fonts.defaultFontSize*fontScaler, self.text, self.textAlignment )     
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
        self.scroll_area.show()                
    
def centerWindowOnScreen(window,QApplication):
    frameGm = window.frameGeometry()
    screen = QApplication.primaryScreen()
    centerPoint = screen.availableGeometry().center()
    frameGm.moveCenter(centerPoint)
    window.move(frameGm.topLeft())           

