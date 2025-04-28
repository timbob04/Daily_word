def makeAppContents_EditWordList(dep, container, fonts, UIsizes, appSizeOb, appBoundaries):

    startPos_y = appBoundaries.bottom + UIsizes.pad_medium

    # Title - "Edit word list"
    text = 'Edit word list'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["large"]
    position = [UIsizes.pad_medium,startPos_y,0,0]
    t_editWordListTitle = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position, bold=True)     
    t_editWordListTitle.makeTextObject()
    t_editWordListTitle.showTextObject()

    # Update app boundaries
    lowestPoint = t_editWordListTitle.positionAdjust[1] + t_editWordListTitle.positionAdjust[3]
    rightMostPoint = t_editWordListTitle.positionAdjust[0] + t_editWordListTitle.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    wordList =MakeWordList(dep, container, fonts, UIsizes, appSizeOb, appBoundaries)
    appBoundaries = wordList.appBoundaries

    container.resize(int(appBoundaries.right), int(appBoundaries.bottom))

    return appBoundaries

class MakeWordList():
    def __init__(self, dep, container, fonts, UIsizes, appSizeOb, appBoundaries):
        self.dep = dep
        self.container = container
        self.fonts = fonts
        self.UIsizes = UIsizes
        self.appSizeOb = appSizeOb
        self.appBoundaries = appBoundaries
        # Default values
        self.wordListFontSize = "small"
        self.editDelButonFontSize = "small"
        self.hSpacer = self.UIsizes.pad_small # horizontal spacer between elements in word list
        # Constructor functions
        # self.makeScrollableArea()
        self.makeTitles()
        self.findListElementPositionsAndSizes()
        self.getWordList()
        self.getWordsWithDefinitons()
        self.getHeightOfEachWordDef()
        self.sortWordListAlphabetically()

    def makeTitles(self):
        curText = "Priority\nword"
        pos = [self.UIsizes.pad_medium, self.appBoundaries.bottom + self.UIsizes.pad_medium, 0, 0]
        self.t_priorityWord = self.dep.StaticText(self.dep, self.container, \
            self.fonts.defaultFontSize*self.fonts.fontScalers["tiny"], \
            curText, self.dep.Qt.AlignCenter, [int(x) for x in pos])
        self.t_priorityWord.makeTextObject()
        self.t_priorityWord.showTextObject()
        # Update app boundaries
        lowestPoint = self.t_priorityWord.positionAdjust[1] + self.t_priorityWord.positionAdjust[3]
        rightMostPoint = self.t_priorityWord.positionAdjust[0] + self.t_priorityWord.positionAdjust[2]
        self.appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    def findListElementPositionsAndSizes(self):   
        # Priority word toggle title width
        self.width_priorityWord = self.t_priorityWord.textOb.width()
        # Delete button width
        curText = "Delete"
        b_deleteButton = self.dep.PushButton(self.dep, self.container, self.fonts.defaultFontSize*self.fonts.fontScalers[self.editDelButonFontSize], curText, [0, 0, 0, 0])
        b_deleteButton.makeButton()
        self.width_deleteButton = b_deleteButton.button.width()
        # Edit button width
        curText = "Edit"
        b_editButton = self.dep.PushButton(self.dep, self.container, self.fonts.defaultFontSize*self.fonts.fontScalers[self.editDelButonFontSize], curText, [0, 0, 0, 0])
        b_editButton.makeButton()
        self.width_editButton = b_editButton.button.width()
        # Button height
        self.height_button = b_deleteButton.button.height()
        # Width of everything apart from word and definition
        width_excludeWordDef = self.UIsizes.pad_medium + self.width_priorityWord + \
            self.hSpacer + self.width_deleteButton + self.hSpacer + self.width_editButton + \
            self.hSpacer + self.UIsizes.pad_medium                       
        # Width of the word and definition area
        self.width_wordDef = self.appBoundaries.right - width_excludeWordDef
        # Toggle height
        toggle = self.dep.Toggle(self.dep,self.container,self.UIsizes,100,100,False)
        self.height_toggle = toggle.toggle.height()
        # Text height
        fontMetrics = self.getFontMetrics(self.wordListFontSize)
        boundingRect = fontMetrics.boundingRect(0,0,0,0,self.dep.Qt.AlignLeft,"0") 
        self.height_text = boundingRect.height()
        # Get starting x-axis positions for each element
        self.findXStartPositions()
        # Get starting y-axis positions for each element
        self.findYStartPositions()
        # Delete things not needed anymore
        b_deleteButton.button.deleteLater()
        b_editButton.button.deleteLater()
        toggle.toggle.deleteLater()

    def getFontMetrics(self, fontSize):
        font = self.dep.QFont()
        font.setPointSizeF(self.fonts.defaultFontSize * self.fonts.fontScalers[fontSize])    
        fontMetrics = self.dep.QFontMetrics(font)
        return fontMetrics       

    def findXStartPositions(self):
        self.xPos_toggle_center = self.UIsizes.pad_medium + self.width_priorityWord / 2
        self.xPos_deleteButton_start = self.UIsizes.pad_medium + self.width_priorityWord + self.hSpacer
        self.xPos_editButton_start = self.xPos_deleteButton_start + self.width_deleteButton + self.hSpacer
        self.xPos_text_start = self.xPos_editButton_start + self.width_editButton + self.hSpacer
        self.xPos_text_end = self.xPos_text_start + self.width_wordDef
   
    def findYStartPositions(self):
        # Finds the distance needed to push down each list element (text, buttonm toggle) to get them all centered on the same line/row
        maxHeight = max(self.height_button, self.height_toggle, self.height_text)
        self.increment_toggle = int( (maxHeight - self.height_toggle) / 2 )
        self.increment_button = int( (maxHeight - self.height_button) / 2 )
        self.increment_text = int( (maxHeight - self.height_text) / 2 )

    def makeScrollableArea(self):
        self.container_wordList = self.dep.QWidget()
        self.dep.makeScrollAreaForCentralWidget(self.dep, self.container, self.container_wordList)

    def getWordList(self):
        self.getWordListFilePath()
        self.wordList = self.dep.readJSONfile(self.dep.json, self.filePath)  
    
    def getWordListFilePath(self):    
        base_dir = self.dep.getBaseDir(self.dep.sys, self.dep.os)
        dir_accessoryFiles = self.dep.os.path.join(base_dir, '..', 'accessoryFiles')
        self.filePath = self.dep.os.path.join(dir_accessoryFiles, 'WordsDefsCodes.json')

    def getWordsWithDefinitons(self):
        for ind in range(len(self.wordList)):
            wordAndDef = self.wordList[ind]["word"] + ": " + self.wordList[ind]["definition"]
            hyphenatedText = self.dep.softHyphenateLongWords(wordAndDef)
            self.wordList[ind]["wordAndDef"] = hyphenatedText

    def getHeightOfEachWordDef(self):
        fontMetrics = self.getFontMetrics(self.wordListFontSize)
        for ind in range(len(self.wordList)):
            text = self.wordList[ind]["wordAndDef"]
            boundingRect = fontMetrics.boundingRect(0,0,int(self.width_wordDef),0, self.dep.Qt.AlignLeft | self.dep.Qt.TextWordWrap, text) 
            self.wordList[ind]["wordHeight"] = boundingRect.height()

    def sortWordListAlphabetically(self):
        # Add new fields to each item in wordList giving the first, second and third letters of the sentence
        for item in self.wordList:
            strippedSentence = item["wordAndDef"].lstrip()
            item["firstLetter"] = strippedSentence[0].lower() if len(strippedSentence) > 0 else ''
            item["secondLetter"] = strippedSentence[1].lower() if len(strippedSentence) > 1 else ''
            item["thirdLetter"] = strippedSentence[2].lower() if len(strippedSentence) > 2 else ''
        # Alphabetically sort wordList based on these first three letters (new fields)
        self.wordList_sorted = sorted(self.wordList, key=lambda x: (x["firstLetter"], x["secondLetter"], x["thirdLetter"])) # tuple input required to sort based on multiple lists, with priority going left to right
          