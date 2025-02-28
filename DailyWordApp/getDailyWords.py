class WordAndDefinition():
    def __init__(self,dep):
        # Inputs
        self.WordList = None
        self.filePath = None
        self.dep = dep
        # Parameters
        self.allWordsPrevShown = None
        self.positionOfWord = None
        self.word = "No words added"
        self.definition = ""
        self.dataExists = False
        self.wordPresent = False
        self.wordPriorityStatus = False
        # Initializiation methods
        self.getWordListFilePath()
        self.getWordList()
        self.doesDataExist()
        if self.dataExists:
            self.areWordsPresent()
        if self.wordPresent:   
            self.areAllWordsPrevShown() # if yes, go back to start of list
            self.getDailyWordPosInWordList()
            self.getWordAndDefintion()
            self.getWordPriorityWordStatus()

    def getWordListFilePath(self):    
        base_dir = self.dep.getBaseDir(self.dep.sys,self.dep.os)
        dir_accessoryFiles = self.dep.os.path.join(base_dir, '..', 'accessoryFiles')
        self.filePath = self.dep.os.path.join(dir_accessoryFiles, 'WordsDefsCodes.json')

    def getWordList(self):    
        self.WordList = self.dep.readJSONfile(self.dep.json, self.filePath)     

    def doesDataExist(self):    
        self.dataExists = not (self.WordList is None) and len(self.WordList) > 0

    def areWordsPresent(self):
        wordPresent = any(word['word'] for word in self.WordList)
        defPresent = any(word['definition'] for word in self.WordList)        
        self.wordPresent = wordPresent and defPresent

    def areAllWordsPrevShown(self):
        # Check to see if the entire list of words has been presented before
        self.allWordsPrevShown = all(word['wordShown'] for word in self.WordList)

    def getDailyWordPosInWordList(self):    
        if (self.allWordsPrevShown):
            self.positionOfWord = 0
        else:
            self.positionOfWord = self.firstFalse_wordShown()

    def firstFalse_wordShown(self):
        for index, curItem in enumerate(self.WordList):
            if not curItem['wordShown']:
                return index
        return None  
    
    def getWordAndDefintion(self): 
        if self.wordPresent:            
            self.word = self.WordList[self.positionOfWord]['word']
            self.definition = self.WordList[self.positionOfWord]['definition']

    def returnWordAndDefinition(self):
        return self.word, self.definition

    def updateWordList(self):       
        if (self.allWordsPrevShown):
            for word in self.WordList[1:]: # change all 'wordShown' to false, except for the first
                word['wordShown'] = False
        else:
            self.WordList[self.positionOfWord]['wordShown'] = True
        self.updateJSONfile()

    def updateJSONfile(self):
        with open(self.fileName, 'w') as file:
            self.dep.json.dump(self.WordList, file, indent=4)  

    def getWordPriorityWordStatus(self):
        if self.wordPresent:
            self.wordPriorityStatus = self.WordList[self.positionOfWord]['isPriorityWord']