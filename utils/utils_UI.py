class SystemScalingFactors():
    def __init__(self,dep,app):
        # Inputs
        self.dep = dep
        self.app = app
        # Initializer methods
        self.getScaleFactors()

    def getScaleFactors(self):
        self.dpi_base = 96
        screen = self.app.screenAt(self.dep.QCursor.pos())
        self.screenDPI = screen.logicalDotsPerInch()
        # self.fontScaleFactor = self.screenDPI / self.dpi_base
        self.fontScaleFactor = screen.devicePixelRatio()
        self.UIelementsScaleFactor = self.screenDPI / 25.4

class DefineFontSizes:
    def __init__(self,scalingFactor,Qfont):
        self.scalingFactor = scalingFactor
        self.Qfont = Qfont 
        self.fontFamily = "Arial"
        # Initializer methods
        self.defineFontSizes()
        self.convertFontSizes()
        self.makeFonts()

    def defineFontSizes(self):
        self.fontSizes = {str(num): num for num in range(5, 16)}

    def convertFontSizes(self):
        self.fontSizes = {key: value * self.scalingFactor for key, value in self.fontSizes.items()}

    def makeFonts(self):
        # Make standard fonts
        self.fonts = {key: self.Qfont(self.fontFamily, int(size), self.Qfont.Normal, False) 
            for key, size in self.fontSizes.items()}
        # Make bold fonts
        self.fonts.update({
        f"{key}_bold": self.Qfont(self.fontFamily, int(size), self.Qfont.Bold, False) 
            for key, size in self.fontSizes.items()
        })

    def returnFonts(self):        
        return self.fonts

class DefineUIsizes:
    def __init__(self,scalingFactor):
        self.scalingFactor = scalingFactor
        # Initializer methods
        self.defineSizes_mm()
        self.convert_mmToPixels()

    def defineSizes_mm(self):    
        self.sizesInputs = {
        "padding_small": 10,
        "padding_medium": 20,
        "padding_large": 40
        }

    def convert_mmToPixels(self):    
        self.UIsizes = {key: value * self.scalingFactor for key, value in self.sizesInputs.items()}

    def returnSizes(self):        
        return self.UIsizes
 
class Boundaries:
    def __init__(self):
        self.bottom = 0
        self.right = 0
        self.savePoints = {}

    def storeBoundaries(self,bottom,right,new=None):
        self.bottom = max(self.bottom,bottom)
        self.right = max(self.right,right)
        if new is not None:
            self.savePoints.update(new)

def centerWindowOnScreen(window,QApplication):
    frameGm = window.frameGeometry()
    screen = QApplication.primaryScreen()
    centerPoint = screen.availableGeometry().center()
    frameGm.moveCenter(centerPoint)
    window.move(frameGm.topLeft())           

# Create static text boxes
class StaticText:
    def __init__(self, dep, window, font, text, position, textAlignment):
        # Input values
        self.dep = dep
        self.window = window
        self.font = font
        self.text = text
        self.textAlignment = textAlignment
        self.position = position
        # Default values        
        self.fontMetrics = self.dep.QFontMetrics(font)  
        self.color = 'black'        
        # Initialize some variables
        self.positionAdjust = None
        self.Vcenter = None
        self.Hcenter = None    
        # Constructor functions
        self.getActualPosition()
        self.getVandHcenter()

    def getActualPosition(self):
        if self.position[2] > 0:
            bounding_rect = self.fontMetrics.boundingRect(0,0,int(self.position[2]),int(self.position[3]), self.textAlignment | Qt.TextWordWrap, self.text)       
        else:
            bounding_rect = self.fontMetrics.boundingRect(0,0,int(self.position[2]),int(self.position[3]), self.textAlignment, self.text)       
        self.positionAdjust = [int(self.position[0]), int(self.position[1]), int(bounding_rect.width()), int(bounding_rect.height())]

    def getVandHcenter(self):
        self.Hcenter = self.positionAdjust[0] + self.positionAdjust[2]/2
        self.Vcenter = self.positionAdjust[1] + self.positionAdjust[3]/2

    def centerAlign_V(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3]/2)

    def centerAlign_H(self):
        self.positionAdjust[0] = int(self.positionAdjust[0] - self.positionAdjust[2]/2)

    def alignBottom(self):
        self.positionAdjust[1] = int(self.positionAdjust[1] - self.positionAdjust[3])
            
    def makeTextObject(self):
        textOb = self.dep.QLabel(self.text, self.window)
        textOb.setWordWrap(True)    
        textOb.setFont(self.font)
        textOb.setAlignment(self.textAlignment)
        textOb.setGeometry(*self.positionAdjust) 
        textOb.setStyleSheet(f"QLabel {{ color : {self.color}; }}")        
        textOb.show()
        return textOb        
    
