def makeAppContents(dep,window,fonts,UIsizes,appSizeOb):

    appBoundaries = dep.AppBoundaries()

    # Title - "Word:"
    text = 'Word:'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["default"]
    position = [UIsizes.pad_medium,UIsizes.pad_medium,0,0]
    t_wordTitle = dep.StaticText(dep, window, fonts.defaultFontSize*fontScaler, text, textAlignment, position)     
    t_wordTitle.makeTextObject()
    t_wordTitle.showTextObject()

    # Update app boundaries
    lowestPoint = t_wordTitle.positionAdjust[1] + t_wordTitle.positionAdjust[3]
    rightMostPoint = t_wordTitle.positionAdjust[0] + t_wordTitle.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)
    
    # Word (of the day)
    text = "WordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWord"
    fontScaler = fonts.fontScalers["default"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_small
    widthOfText = appSizeOb.sentenceWidth * 0.6
    position = [UIsizes.pad_medium,startingYPosition,widthOfText,0]
    maxHeight = appSizeOb.appHeight * 0.2
    ts_wordOfDay = dep.MakeTextWithMaxHeight(dep, window, fonts.defaultFontSize*fontScaler, text, position, maxHeight)
    ts_wordOfDay.makeScrollableText()
    ts_wordOfDay.showTextObject()

    # Update app boundaries
    lowestPoint = ts_wordOfDay.position[1] + ts_wordOfDay.position[3]
    rightMostPoint = ts_wordOfDay.position[0] + ts_wordOfDay.position[2]
    wordOfDayMiddle = ts_wordOfDay.position[1] + ts_wordOfDay.position[3]/2
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint,store={'wordOfDayMiddle': wordOfDayMiddle})

    # Title - "Definition:"
    text = 'Definition:'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["default"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_medium
    position = [UIsizes.pad_medium,startingYPosition,0,0]
    t_defTitle = dep.StaticText(dep, window, fonts.defaultFontSize*fontScaler, text, textAlignment, position)     
    t_defTitle.makeTextObject()
    t_defTitle.showTextObject()

    # Update app boundaries
    lowestPoint = t_defTitle.positionAdjust[1] + t_defTitle.positionAdjust[3]
    rightMostPoint = t_defTitle.positionAdjust[0] + t_defTitle.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    # Definition (of the day)
    text = "DefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDef"
    fontScaler = fonts.fontScalers["default"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_small
    widthOfText = appSizeOb.sentenceWidth * 0.6
    position = [UIsizes.pad_medium,startingYPosition,widthOfText,0]
    maxHeight = appSizeOb.appHeight * 0.2
    ts_definition = dep.MakeTextWithMaxHeight(dep, window, fonts.defaultFontSize*fontScaler, text, position, maxHeight)
    ts_definition.makeScrollableText()
    ts_definition.showTextObject()   

    # Update app boundaries
    lowestPoint = ts_definition.position[1] + ts_definition.position[3]
    rightMostPoint = ts_definition.position[0] + ts_definition.position[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    # Title - "Priority word of the day"
    text = 'Priority word of the day:'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["small"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_large*1.5
    position = [UIsizes.pad_medium,startingYPosition,0,0]
    t_priorityWordTitle = dep.StaticText(dep, window, fonts.defaultFontSize*fontScaler, text, textAlignment, position, italic=True)     
    t_priorityWordTitle.makeTextObject()
    t_priorityWordTitle.showTextObject()

    # Update app boundaries
    lowestPoint = t_priorityWordTitle.positionAdjust[1] + t_priorityWordTitle.positionAdjust[3]
    rightMostPoint = t_priorityWordTitle.positionAdjust[0] + t_priorityWordTitle.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    # Priority word of the day
    text = "DefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDef"
    fontScaler = fonts.fontScalers["small"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_small
    widthOfText = appSizeOb.sentenceWidth * 0.6
    position = [UIsizes.pad_medium,startingYPosition,widthOfText,0]
    maxHeight = appSizeOb.appHeight * 0.12
    ts_definition = dep.MakeTextWithMaxHeight(dep, window, fonts.defaultFontSize*fontScaler, text, position, maxHeight, italic=True)
    ts_definition.makeScrollableText()
    ts_definition.showTextObject()  

    # Update app boundaries
    lowestPoint = ts_definition.position[1] + ts_definition.position[3]
    rightMostPoint = ts_definition.position[0] + ts_definition.position[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)
    
    # Reveal button
    text = "Reveal definition"
    fontScaler = fonts.fontScalers["default"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_large
    position = [UIsizes.pad_medium,startingYPosition,0,0]
    pb_reveal = dep.PushButton(dep, window, fonts.defaultFontSize*fontScaler, text, position)
    pb_reveal.makeButton()
    pb_reveal.showButton()

    # Priority word toggle
    toggleStatus = False
    startingXposition = appBoundaries.right + UIsizes.pad_large
    startingYposition = appBoundaries.wordOfDayMiddle
    toggle_priorityWord = Toggle(dep,window,UIsizes,startingXposition,startingYposition,toggleStatus)
    toggle_priorityWord.showToggle()


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
        self.applyToggleStyle()

    def getXandYPoints(self):
        self.xPoint = self.center - self.sizes.toggleWidth/2
        self.yPoint = self.middle - self.sizes.toggleWidth/2

    def setTogglePosition(self):
        textPos = [self.xPoint,self.yPoint,self.sizes.toggleWidth,self.sizes.toggleWidth]
        self.toggle.setGeometry(*(int(x) for x in textPos))
        self.applyToggleStyle()

    def applyToggleStyle(self):
        self.toggle.setStyleSheet(f"""
            QCheckBox::indicator {{
                width: {self.sizes.toggleWidth}px;
                height: {self.sizes.toggleWidth}px;
                background-color: white;
                border: 0px solid #b0b0b0;
                border-radius: {self.sizes.toggleWidth/10}px;
            }}
            QCheckBox::indicator:checked {{
                background-color: #4CAF50;
                border: 0px solid #45a049;
            }}
            QCheckBox::indicator:hover {{
                border: 3px solid #808080;
            }}
        """)

    def showToggle(self):
        self.toggle.show()

    def hideToggle(self):
        self.toggle.hide()


        
        