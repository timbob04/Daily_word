class addNewWordTextBoxes:
    def __init__(self, dep, window, fonts):
        self.dep = dep
        self.window = window
        self.fonts = fonts                         
        self.inputTextOb_word = None
        self.inputTextOb_definition = None   
        self.newWord = None
        self.newDefinition = None   
        self.fontSizeToUse = self.fonts.fontScalers["default"]                

    def makeEditTextBox(self,left,top,width):    
        tb = self.dep.QLineEdit(self.window)  
        self.getFont()  
        tb.setFont(self.font)
        tb.setGeometry(int(left), int(top), int(width), int(self.getTextHeight()) )
        tb.setAlignment(self.dep.Qt.AlignLeft | self.dep.Qt.AlignVCenter)
        tb.setStyleSheet("QLineEdit { border: 1px solid black; }")
        return tb
    
    def getFont(self):
        self.font = self.dep.QFont()
        self.font.setPointSizeF(int(self.fonts.defaultFontSize * self.fontSizeToUse))
    
    def getTextHeight(self):
        fontMetrics = self.dep.QFontMetrics(self.font) 
        bounding_rect = fontMetrics.boundingRect(0,0,0,0, self.dep.Qt.AlignLeft | self.dep.Qt.AlignVCenter, "0") 
        height = bounding_rect.height()
        heightBox = height + height*0.1
        return heightBox

    def makeEditTextBox_word(self,left,top,width):
        self.inputTextOb_word = self.makeEditTextBox(left,top,width)
        self.pos_word = self.getPosition(self.inputTextOb_word)

    def makeEditTextBox_definition(self,left,top,width):
        self.inputTextOb_definition = self.makeEditTextBox(left,top,width)    
        self.pos_definition = self.getPosition(self.inputTextOb_definition)

    def getPosition(self, inputTextOb):
        xy = inputTextOb.pos()
        wh = inputTextOb.size()
        return [xy.x(), xy.y(), wh.width(), wh.height()]
  
    def AddButtonPressed(self):
        self.getNewWordDef()
        self.addWordToJSONfile()        
        self.clearEditTextBoxes()   

    def getNewWordDef(self):
        self.newWord = self.inputTextOb_word.text()
        self.newDefinition = self.inputTextOb_definition.text()    

    def addWordToJSONfile(self):  
        self.jsonFileName = getWordListPath(self.dep)       
        self.dataIn = self.dep.readJSONfile(self.dep.json, self.jsonFileName)      
        # Make the new word/def json entry
        new_entry = {
            "word": self.newWord,
            "definition": self.newDefinition,
            "wordShown": False,
            "isPriorityWord": False,
            "priorityWordShown": False
            }        

        # Append new word/def to current word/def json list
        if self.dataIn is not None:
            self.dataIn.append(new_entry)
        else:
            self.dataIn = [new_entry]
        # Save new list with new word/def
        with open(self.jsonFileName, 'w') as file:
            self.dep.json.dump(self.dataIn, file, indent=4)     

    def clearEditTextBoxes(self):
        self.inputTextOb_word.clear()
        self.inputTextOb_definition.clear()        

def getWordListPath(dep):
    # Get path of accessory files
    base_dir = dep.getBaseDir(dep.sys, dep.os)
    accessoryFiles_dir = dep.os.path.join(base_dir, '..', 'accessoryFiles')
    # Path to json file for words and definitions
    return dep.os.path.join(accessoryFiles_dir, 'WordsDefsCodes.json')   