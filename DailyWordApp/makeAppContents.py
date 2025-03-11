def makeAppContents(dep,window,fonts):
    
    layout = dep.QVBoxLayout(window)
    
    layout.addSpacing(10)

    # Title - "word:"
    text = 'Word:'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["small"]
    t = dep.StaticText(dep,fonts.defaultFontSize*fontScaler,text,textAlignment)     
    t_wordTitle = t.makeTextObject()
    layout.addWidget(t_wordTitle)
    
    layout.addSpacing(10)
    
    text = "HelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHello"
    ts = dep.MakeTextWithMaxHeight(dep,fonts,"default",text,100,300)
    ts_wordOfDay = ts.makeScrollableText()
    layout.addWidget(ts_wordOfDay)
    


            

