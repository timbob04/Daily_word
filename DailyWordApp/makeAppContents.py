def makeAppContents(dep,window,fonts,UIsizes):
    
    layout = dep.QVBoxLayout(window)
    
    layout.addSpacing(UIsizes.pad_large)

    # Title - "word:"
    text = 'Word:'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["small"]
    t = dep.StaticText(dep,fonts.defaultFontSize*fontScaler,text,textAlignment)     
    t_wordTitle = t.makeTextObject()
    layout.addWidget(t_wordTitle)
    
    layout.addSpacing(UIsizes.pad_small)
    
    text = "HelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHello"
    ts = dep.MakeTextWithMaxHeight(dep,fonts,"default",text,400,300)
    ts_wordOfDay = ts.makeScrollableText()
    layout.addWidget(ts_wordOfDay)
    


            

