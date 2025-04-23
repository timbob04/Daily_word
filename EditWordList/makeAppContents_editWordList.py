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

    container.resize(appBoundaries.right, appBoundaries.bottom)

    return appBoundaries

class makeWordList():
    def __init__(self, dep, container, fonts, UIsizes, appSizeOb, appBoundaries):
        self.dep = dep
        self.container = container
        self.fonts = fonts
        self.UIsizes = UIsizes
        self.appSizeOb = appSizeOb
        # Constructor functions
        self.makeScrollableArea()
        self.getWordList()

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

          