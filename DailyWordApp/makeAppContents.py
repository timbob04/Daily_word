def makeAppContents(dep,window,fonts,UIsizes,appSizeOb):

    # Title - "Word:"
    text = 'Word:'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["default"]
    position = [UIsizes.pad_medium,UIsizes.pad_medium,0,0]
    t_wordTitle = dep.StaticText(dep,window, fonts.defaultFontSize*fontScaler,text,textAlignment,position)     
    t_wordTitle.showTextObject()

    lowestPoint = t_wordTitle.positionAdjust[1] + t_wordTitle.positionAdjust[3]

    # Word
    text = "WordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWord"
    startingYPosition = lowestPoint + UIsizes.pad_small
    widthOfText = appSizeOb.sentenceWidth * 0.6
    position = [UIsizes.pad_medium,startingYPosition,widthOfText,0]
    maxHeight = appSizeOb.appHeight * 0.2
    ts_wordOfDay = dep.MakeTextWithMaxHeight(dep,window,fonts,"default",text,position,maxHeight)
    ts_wordOfDay.showTextObject()

    


    # layout.addSpacing(UIsizes.pad_medium)

    # # Title - "Definition:"
    # text = 'Definition:'
    # textAlignment = dep.Qt.AlignLeft
    # fontScaler = fonts.fontScalers["small"]
    # t = dep.StaticText(dep,fonts.defaultFontSize*fontScaler,text,textAlignment)     
    # t_DefTitle = t.makeTextObject()
    # layout.addWidget(t_DefTitle)

    # layout.addSpacing(UIsizes.pad_small)

    # # Definition
    # text = "DefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDef"
    # ts = dep.MakeTextWithMaxHeight(dep,fonts,"default",text,wordBoxMaxWidth,wordBoxMaxHeight)
    # ts_defintion = ts.makeScrollableText()
    # layout.addWidget(ts_defintion)

            





