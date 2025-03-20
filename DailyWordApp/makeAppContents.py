def makeAppContents(dep,window,fonts,UIsizes,appSizeOb):

    appBoundaries = dep.AppBoundaries()

    # Title - "Word:"
    text = 'Word:'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["default"]
    position = [UIsizes.pad_medium,UIsizes.pad_medium,0,0]
    t_wordTitle = dep.StaticText(dep,window, fonts.defaultFontSize*fontScaler,text,textAlignment,position)     
    t_wordTitle.showTextObject()

    # Update app boundaries
    lowestPoint = t_wordTitle.positionAdjust[1] + t_wordTitle.positionAdjust[3]
    rightMostPoint = t_wordTitle.positionAdjust[0] + t_wordTitle.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)
    
    # Word (of the day)
    text = "WordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWord"
    startingYPosition = appBoundaries.bottom + UIsizes.pad_small
    widthOfText = appSizeOb.sentenceWidth * 0.6
    position = [UIsizes.pad_medium,startingYPosition,widthOfText,0]
    maxHeight = appSizeOb.appHeight * 0.2
    ts_wordOfDay = dep.MakeTextWithMaxHeight(dep,window,fonts,"default",text,position,maxHeight)
    ts_wordOfDay.showTextObject()

    # Update app boundaries
    lowestPoint = ts_wordOfDay.position[1] + ts_wordOfDay.position[3]
    rightMostPoint = ts_wordOfDay.position[0] + ts_wordOfDay.position[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    # Title - "Definition:"
    text = 'Definition:'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["default"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_large
    position = [UIsizes.pad_medium,startingYPosition,0,0]
    t_defTitle = dep.StaticText(dep, window, fonts.defaultFontSize*fontScaler, text, textAlignment, position)     
    t_defTitle.showTextObject()

    # Update app boundaries
    lowestPoint = t_defTitle.positionAdjust[1] + t_defTitle.positionAdjust[3]
    rightMostPoint = t_defTitle.positionAdjust[0] + t_defTitle.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    # Definition (of the day)
    text = "DefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDef"
    startingYPosition = appBoundaries.bottom + UIsizes.pad_small
    widthOfText = appSizeOb.sentenceWidth * 0.6
    position = [UIsizes.pad_medium,startingYPosition,widthOfText,0]
    maxHeight = appSizeOb.appHeight * 0.2
    ts_definition = dep.MakeTextWithMaxHeight(dep,window,fonts,"default",text,position,maxHeight)
    ts_definition.showTextObject()   


            

