def makeAppContents(dep,window,fonts,UIsizes):

    # Input parameters
    wordBoxMaxWidth = 600
    wordBoxMaxHeight = 300

    layout = dep.QVBoxLayout(window)
    
    layout.addSpacing(UIsizes.pad_small)

    # Title - "Word:"
    text = 'There once was a man who lived in a boat, who then died'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["small"]
    t = dep.StaticText(dep,fonts.defaultFontSize*fontScaler,text,textAlignment)     
    t_wordTitle = t.makeTextObject()
    layout.addWidget(t_wordTitle)
    
    layout.addSpacing(UIsizes.pad_small)
    
    # Word
    text = "WordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWordWord"
    ts = dep.MakeTextWithMaxHeight(dep,fonts,"default",text,wordBoxMaxWidth,wordBoxMaxHeight)
    ts_wordOfDay = ts.makeScrollableText()
    layout.addWidget(ts_wordOfDay)

    layout.addSpacing(UIsizes.pad_medium)

    # Title - "Definition:"
    text = 'Definition:'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["small"]
    t = dep.StaticText(dep,fonts.defaultFontSize*fontScaler,text,textAlignment)     
    t_DefTitle = t.makeTextObject()
    layout.addWidget(t_DefTitle)

    layout.addSpacing(UIsizes.pad_small)

    # Definition
    text = "DefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDefDef"
    ts = dep.MakeTextWithMaxHeight(dep,fonts,"default",text,wordBoxMaxWidth,wordBoxMaxHeight)
    ts_defintion = ts.makeScrollableText()
    layout.addWidget(ts_defintion)

            





