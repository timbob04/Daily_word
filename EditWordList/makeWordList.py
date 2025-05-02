class MakeWordList():
    def __init__(self, dep, container, fonts, UIsizes, appSizeOb, appBoundaries, editTextBoxes):
        self.dep = dep
        self.container = container
        self.fonts = fonts
        self.UIsizes = UIsizes
        self.appSizeOb = appSizeOb
        self.appBoundaries = appBoundaries
        self.editTextBoxes = editTextBoxes
        # Default values
        self.wordListFontSize = "small"
        self.delButonFontSize = "small"
        self.hSpacer = self.UIsizes.pad_small # horizontal spacer between elements in word list
        self.vSpacer = self.UIsizes.pad_large # vertical spacer between rows in word list
        # Constructor functions - make initial word list
        self.makeTitles()
        self.findListElementPositionsAndSizes()
        self.getWordList()
        self.getWordsWithDefinitons()
        self.sortWordListAlphabetically()
        self.getHeightOfEachWordDef()
        self.getStartPositions_y()
        self.makeWordList()

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
        self.appBoundaries.setNewBoundaries(bottom=lowestPoint)

    def findListElementPositionsAndSizes(self):   
        # Priority word toggle title width and center point
        self.width_priorityWord = self.t_priorityWord.textOb.width()
        self.centerPoint_priorityWord = self.t_priorityWord.positionAdjust[0] + self.width_priorityWord / 2
        # List starting position - y-axis
        self.listStartingPos_y = self.appBoundaries.bottom
        # Delete button width
        curText = "Delete"
        b_deleteButton = self.dep.PushButton(self.dep, self.container, self.fonts.defaultFontSize*self.fonts.fontScalers[self.delButonFontSize], curText, [0, 0, 0, 0])
        b_deleteButton.makeButton()
        self.width_deleteButton = b_deleteButton.button.width()
        # Button height
        self.height_button = b_deleteButton.button.height()
        # Width of everything apart from word and definition
        width_excludeWordDef = self.UIsizes.pad_medium + self.width_priorityWord + \
            self.hSpacer + self.width_deleteButton + \
            self.hSpacer + self.UIsizes.pad_medium                       
        # Width of the word and definition area
        self.width_wordDef = self.appBoundaries.right - width_excludeWordDef
        # Toggle height
        toggle = self.dep.Toggle(self.dep,self.container,self.UIsizes,100,100,False)
        self.height_toggle = toggle.toggle.height()
        print(f"height_toggle: {self.height_toggle}")
        # Text height
        fontMetrics = self.getFontMetrics(self.wordListFontSize)
        boundingRect = fontMetrics.boundingRect(0,0,0,0,self.dep.Qt.AlignLeft,"0") 
        self.height_text = boundingRect.height()
        # Get starting x-axis positions for each element
        self.findStartPositions_x()
        # Get starting y-axis positions for each element
        self.findIncrements_y()
        # Delete things not needed anymore
        b_deleteButton.button.deleteLater()
        toggle.toggle.deleteLater()

    def getFontMetrics(self, fontSize):
        font = self.dep.QFont()
        font.setPointSizeF(self.fonts.defaultFontSize * self.fonts.fontScalers[fontSize])    
        fontMetrics = self.dep.QFontMetrics(font)
        return fontMetrics       

    def findStartPositions_x(self):
        self.xPos_toggle_center = self.UIsizes.pad_medium + self.width_priorityWord / 2
        self.xPos_deleteButton_start = self.UIsizes.pad_medium + self.width_priorityWord + self.hSpacer
        self.xPos_text_start = self.xPos_deleteButton_start + self.width_deleteButton + self.hSpacer
   
    def findIncrements_y(self): 
        # Finds the distance needed to push down each list element (text, buttonm toggle) to get them all centered on the same line/row
        self.maxHeight = max(self.height_button, self.height_toggle, self.height_text)
        self.increment_toggle = int( (self.maxHeight - self.height_toggle) / 2 )
        self.increment_button = int( (self.maxHeight - self.height_button) / 2 )
        self.increment_text = int( (self.maxHeight - self.height_text) / 2 )

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

    def sortWordListAlphabetically(self):
        # Add new fields to each item in wordList giving the first, second and third letters of the sentence
        for item in self.wordList:
            strippedSentence = item["wordAndDef"].lstrip()
            item["firstLetter"] = strippedSentence[0].lower() if len(strippedSentence) > 0 else ''
            item["secondLetter"] = strippedSentence[1].lower() if len(strippedSentence) > 1 else ''
            item["thirdLetter"] = strippedSentence[2].lower() if len(strippedSentence) > 2 else ''
        # Alphabetically sort wordList based on these first three letters (new fields)
        self.wordList = sorted(self.wordList, key=lambda x: (x["firstLetter"], x["secondLetter"], x["thirdLetter"])) # tuple input required to sort based on multiple lists, with priority going left to right

    def getHeightOfEachWordDef(self):
        fontMetrics = self.getFontMetrics(self.wordListFontSize)
        for ind in range(len(self.wordList)):
            text = self.wordList[ind]["wordAndDef"]
            boundingRect = fontMetrics.boundingRect(0,0,int(self.width_wordDef),0, self.dep.Qt.AlignLeft | self.dep.Qt.TextWordWrap, text) 
            self.wordList[ind]["wordHeight"] = boundingRect.height() + self.increment_text

    def getStartPositions_y(self):
        for ind in range(len(self.wordList)):
            if ind == 0:
                self.wordList[ind]["startPos_y"] = self.listStartingPos_y + self.UIsizes.pad_small
            else:
                self.wordList[ind]["startPos_y"] = self.wordList[ind-1]["startPos_y"] + rowWidth + self.vSpacer
            curWordHeight = self.wordList[ind]["wordHeight"]
            rowWidth = max(curWordHeight, self.maxHeight)
            
            lowestPoint = self.wordList[ind]["startPos_y"] + rowWidth
            self.appBoundaries.setNewBoundaries(bottom=lowestPoint)

    def makeWordList(self):
        # First delete any existing widgets in the word list - to do        
        # Also reset the app boundaries (bottom) to self.listStartingPos_y - to do
        for ind in range(len(self.wordList)):
            self.makeToggle(ind)
            self.makeDeleteButton(ind)            
            self.printWord(ind)
        # After making list elements (above), update the scroll area - to do
            
    def makeToggle(self, ind):
        toggleMiddle = self.wordList[ind]["startPos_y"] + self.increment_toggle + self.height_toggle/2
        toggle = self.dep.Toggle(self.dep, self.container, self.UIsizes, self.centerPoint_priorityWord, toggleMiddle, False)
        toggle.showToggle()
        # Set toggle's initial state
        if self.wordList[ind]["isPriorityWord"]:
            toggle.toggle.setChecked(True)
        # Connect toggle to function storing the toggle choice in wordList
        def _storeToggleState(toggleState, i=ind): # ind=i is 'Default-value capture'
            self.wordList[i]['isPriorityWord'] = toggleState
            self.saveWordListToJson() # save the json to save the new toggle state           
        toggle.toggle.clicked.connect(_storeToggleState) # clicked.connect sends one input (the toggle state) to the function (slot) in the parentheses
        # Store toggle object in wordList
        self.wordList[ind]["toggle"] = toggle

    def makeDeleteButton(self, ind):
        buttonTop = self.wordList[ind]["startPos_y"] + self.increment_button
        deleteButton = self.dep.PushButton( self.dep, self.container, \
            self.fonts.defaultFontSize*self.fonts.fontScalers[self.delButonFontSize], \
            'Delete', [self.xPos_deleteButton_start, buttonTop, 0, 0] )
        deleteButton.makeButton()
        deleteButton.showButton()
        # Connect button to function dealing with the delete button being pressed
        def _deleteButtonPressed(_unusedSlotArgument, i=ind):
            self.deleteWord(i)
        deleteButton.button.clicked.connect(_deleteButtonPressed) # clicked.connect sends one input (which for a button, is always 'False') to the function (slot) in the parentheses
        # Store delete button object in wordList
        self.wordList[ind]["deleteButton"] = deleteButton

    def printWord(self, ind):
        textTop = self.wordList[ind]["startPos_y"] + self.increment_text
        text = self.wordList[ind]["wordAndDef"]
        pos = [self.xPos_text_start, textTop, self.width_wordDef, self.wordList[ind]["wordHeight"]]
        text = self.dep.StaticText(self.dep, self.container, \
            self.fonts.defaultFontSize*self.fonts.fontScalers[self.wordListFontSize], \
            text, self.dep.Qt.AlignLeft, pos)
        text.makeTextObject()
        text.showTextObject()
        self.wordList[ind]["text"] = text

    def saveWordListToJson(self):
        # Get elements of wordList to save
        wordListToSave = []  
        for ind in range(len(self.wordList)):
            wordListToSave.append({
                "word": self.wordList[ind]["word"],
                "definition": self.wordList[ind]["definition"],
                "wordShown": self.wordList[ind]["wordShown"],
                "isPriorityWord": self.wordList[ind]["isPriorityWord"],
                "priorityWordShown": self.wordList[ind]["priorityWordShown"]
            })
        # Get save file path
        base_dir = self.dep.getBaseDir(self.dep.sys, self.dep.os)
        dir_accessoryFiles = self.dep.os.path.join(base_dir, '..', 'accessoryFiles')
        self.filePath = self.dep.os.path.join(dir_accessoryFiles, 'WordsDefsCodes.json')
        # Save wordListToSave to json file
        with open(self.filePath, 'w') as file:
            self.dep.json.dump(wordListToSave, file, indent=4)  

    def deleteListElements(self):
        # Delete all the widgets in the word list
        for ind in range(len(self.wordList)):
            self.wordList[ind]["toggle"].toggle.deleteLater()
            self.wordList[ind]["deleteButton"].button.deleteLater()
            self.wordList[ind]["text"].textOb.deleteLater()

    def wordAdded(self):
        if self.editTextBoxes.newWord != "" or self.editTextBoxes.newDefinition != "":
            # Delete the widgets (to completely remake the list)
            self.deleteListElements()
            # Append new word and definition to wordList
            self.wordList.append({
                "word": self.editTextBoxes.newWord,
                "definition": self.editTextBoxes.newDefinition,
                "wordShown": False,
                "isPriorityWord": False,
                "priorityWordShown": False
            })
            # Reset the app boundaries
            self.appBoundaries.setNewBoundaries(bottom=self.listStartingPos_y)
            # Re-make word list
            self.getWordsWithDefinitons()
            self.sortWordListAlphabetically()
            self.getHeightOfEachWordDef()
            self.getStartPositions_y()
            self.makeWordList()
            # Re-adjust the size of the container
            self.container.resize(int(self.appBoundaries.right), int(self.appBoundaries.bottom)+self.UIsizes.pad_medium)
            self.container.update()
            # No need to save the wordList to json file, as this is done in the addNewWordTextBoxes class

    def deleteWord(self, ind):
        # Confirm delete dialog
        reply = self.dep.QMessageBox.question(self.container, 'Delete Word',
            f"Are you sure you want to delete '{self.wordList[ind]['word']}'?",
            self.dep.QMessageBox.Yes | self.dep.QMessageBox.No, self.dep.QMessageBox.Yes)
        # If user clicks 'Yes'
        if reply == self.dep.QMessageBox.Yes:
            # Delete the widgets
            self.deleteListElements()
            # Delete the word from wordList
            print(f"deleting word at ind: {ind}")
            self.wordList.pop(ind)
            # Reset the app boundaries
            self.appBoundaries.setNewBoundaries(bottom=self.listStartingPos_y)
            # Re-make word list
            self.getWordsWithDefinitons()
            self.sortWordListAlphabetically()
            self.getHeightOfEachWordDef()
            self.getStartPositions_y()
            self.makeWordList()
            # Re-adjust the size of the container
            self.container.resize(int(self.appBoundaries.right), int(self.appBoundaries.bottom)+self.UIsizes.pad_medium)
            self.container.update()
            # Save the edited wordList to json file
            self.saveWordListToJson()