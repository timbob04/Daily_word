def makeAppContents(dep, container, fonts, UIsizes, appSizeOb, dailyWord, dailyPriorityWord, worker_dailyWordApp):

    # App sizing variables
    appBoundaries = dep.AppBoundaries()
    appWidth = min(appSizeOb.sentenceWidth,appSizeOb.screenWidth)

    # Title - "Word:"
    text = 'Word:'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["default"]
    position = [UIsizes.pad_medium,UIsizes.pad_medium,0,0]
    t_wordTitle = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position, bold=True)     
    t_wordTitle.makeTextObject()
    t_wordTitle.showTextObject()

    # Update app boundaries
    lowestPoint = t_wordTitle.positionAdjust[1] + t_wordTitle.positionAdjust[3]
    rightMostPoint = t_wordTitle.positionAdjust[0] + t_wordTitle.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)
    
    # Word (of the day)
    text = dailyWord.word
    fontScaler = fonts.fontScalers["default"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_small
    widthOfText = appWidth * 0.6
    position = [UIsizes.pad_medium,startingYPosition,widthOfText,0]
    maxHeight = appSizeOb.appHeight * 0.2
    ts_wordOfDay = dep.MakeTextWithMaxHeight(dep, container, fonts.defaultFontSize*fontScaler, text, position, maxHeight)
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
    t_defTitle = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position, bold=True)     
    t_defTitle.makeTextObject()
    t_defTitle.showTextObject()

    # Update app boundaries
    lowestPoint = t_defTitle.positionAdjust[1] + t_defTitle.positionAdjust[3]
    rightMostPoint = t_defTitle.positionAdjust[0] + t_defTitle.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    # Definition (of the day)
    text = dailyWord.definition
    fontScaler = fonts.fontScalers["default"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_small
    widthOfText = appWidth * 0.6
    position = [UIsizes.pad_medium,startingYPosition,widthOfText,0]
    maxHeight = appSizeOb.appHeight * 0.2
    ts_definition = dep.MakeTextWithMaxHeight(dep, container, fonts.defaultFontSize*fontScaler, text, position, maxHeight)
    ts_definition.makeScrollableText() 

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
    t_priorityWordTitle = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position, italic=True)     
    t_priorityWordTitle.makeTextObject()

    # Update app boundaries
    lowestPoint = t_priorityWordTitle.positionAdjust[1] + t_priorityWordTitle.positionAdjust[3]
    rightMostPoint = t_priorityWordTitle.positionAdjust[0] + t_priorityWordTitle.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    # Priority word of the day
    text = dailyPriorityWord.priorityWordAndDef
    fontScaler = fonts.fontScalers["small"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_small
    widthOfText = appWidth * 0.6
    position = [UIsizes.pad_medium,startingYPosition,widthOfText,0]
    maxHeight = appSizeOb.appHeight * 0.12
    ts_priorityWordAndDef = dep.MakeTextWithMaxHeight(dep, container, fonts.defaultFontSize*fontScaler, text, position, maxHeight, italic=True)
    ts_priorityWordAndDef.makeScrollableText()

    # Update app boundaries
    lowestPoint = ts_priorityWordAndDef.position[1] + ts_priorityWordAndDef.position[3]
    rightMostPoint = ts_priorityWordAndDef.position[0] + ts_priorityWordAndDef.position[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)
    
    # Button - "Reveal"
    text = "Reveal definition"
    fontScaler = fonts.fontScalers["default"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_large
    position = [UIsizes.pad_medium,startingYPosition,0,0]
    pb_reveal = dep.PushButton(dep, container, fonts.defaultFontSize*fontScaler, text, position)
    pb_reveal.makeButton()
    pb_reveal.showButton()
    # Define button's actions
    pb_reveal.button.clicked.connect(lambda: ts_definition.showTextObject())
    pb_reveal.button.clicked.connect(lambda: t_priorityWordTitle.showTextObject())
    pb_reveal.button.clicked.connect(lambda: ts_priorityWordAndDef.showTextObject())
    pb_reveal.button.clicked.connect(lambda: t_priorityWord.showTextObject())
    pb_reveal.button.clicked.connect(lambda: toggle_priorityWord.showToggle())
    
    # Update app boundaries
    lowestPoint = pb_reveal.positionAdjust[1] + pb_reveal.positionAdjust[3]
    rightMostPoint = pb_reveal.positionAdjust[0] + pb_reveal.positionAdjust[2]
    revealButtonStartingYPos = startingYPosition
    revealButtonRightmostPoint = rightMostPoint
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint,
                                   store={'revealButtonStartingYPos': revealButtonStartingYPos,
                                          'revealButtonRightmostPoint': revealButtonRightmostPoint})

    # Text - "Priority word"
    text = "Priority\nword"
    fontScaler = fonts.fontScalers["small"]
    textAlignment = dep.Qt.AlignCenter
    position = [appBoundaries.right + UIsizes.pad_medium,0,0,0]
    t_priorityWord = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position)

    # Toggle = "Priority word"
    toggleStatus = dailyWord.wordPriorityStatus
    toggleCenterPos = t_priorityWord.positionAdjust[0] + t_priorityWord.positionAdjust[2]/2
    toggleMiddlePos = appBoundaries.wordOfDayMiddle
    toggle_priorityWord = dep.Toggle(dep,container,UIsizes,toggleCenterPos,toggleMiddlePos,toggleStatus)
    toggle_priorityWord.toggle.clicked.connect(lambda: saveToggleChoice(dep,toggle_priorityWord,dailyWord.word,dailyWord.definition))

    # Readjust toggle text position and show
    t_priorityWord.positionAdjust[1] = toggle_priorityWord.position[1] + UIsizes.toggleWidth * 1.2
    t_priorityWord.makeTextObject()

    # Update app boundaries
    lowestPoint = t_priorityWord.positionAdjust[1] + t_priorityWord.positionAdjust[3]
    rightMostPoint = t_priorityWord.positionAdjust[0] + t_priorityWord.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    # Button - "Edit word list"
    text = "Edit word list"
    fontScaler = fonts.fontScalers["default"]
    startingXPosition = appBoundaries.revealButtonRightmostPoint + UIsizes.pad_large
    startingYPosition = appBoundaries.revealButtonStartingYPos
    position = [startingXPosition,startingYPosition,0,0]
    pb_editWordList = dep.PushButton(dep, container, fonts.defaultFontSize*fontScaler, text, position)

    # Update app boundaries
    lowestPoint = pb_editWordList.positionAdjust[1] + pb_editWordList.positionAdjust[3]
    rightMostPoint = pb_editWordList.positionAdjust[0] + pb_editWordList.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    # Reposition and make Edit word list button
    pb_editWordList.positionAdjust[0] = appBoundaries.right
    pb_editWordList.rightAlign()
    pb_editWordList.makeButton()
    pb_editWordList.showButton()

    # Connect to the Controller's button_clicked signal in the dailyWordApp worker
    pb_editWordList.button.clicked.connect(lambda: worker_dailyWordApp.button_clicked.emit('editWordList')) # Connect to the Controller's button_clicked signal in the dailyWordApp worker

    appContentsWidth = appBoundaries.right + UIsizes.pad_medium
    appContentsHeight = appBoundaries.bottom + UIsizes.pad_medium

    container.resize(int(appContentsWidth),int(appContentsHeight))

    # Return the app boundaries
    return appContentsWidth, appContentsHeight


def saveToggleChoice(dep, h_toggle, word, definition): 

    # Get Json file path
    baseDir = dep.getBaseDir(dep.sys, dep.os)
    accessoryFiles_dir = dep.os.path.join(baseDir, '..', 'accessoryFiles')
    jsonFilePath = dep.os.path.join(accessoryFiles_dir, 'WordsDefsCodes.json')

    # Read json file
    wordList = dep.readJSONfile(dep.json, jsonFilePath)

    # Get position of word
    pos = None
    for i, curWord in enumerate(wordList):
        if curWord['word'] == word and curWord['definition'] == definition:
            pos = i
            break

    # Update priority word toggle status in word list (isPriorityWord)
    if pos is not None:
        wordList[pos]['isPriorityWord'] = h_toggle.toggle.isChecked()

    # Save data
    with open(jsonFilePath, 'w') as file:
        dep.json.dump(wordList, file, indent=4)    

        
        