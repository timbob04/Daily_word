def makeAppContents(dep,window,UIsizes,fonts,boundaries):

    # Title - "word:"
    text = 'Word:'
    textAlignment = dep.Qt.AlignLeft | dep.Qt.AlignTop    
    textPos = (UIsizes["padding_large"], UIsizes["padding_large"], 0, 0)
    ST_wordTitle = dep.StaticText(dep,window,fonts["7"],text,textPos,textAlignment)     
    ST_wordTitle.makeTextObject()

    boundaries.storeBoundaries(ST_wordTitle.positionAdjust[1] + ST_wordTitle.positionAdjust[3],
                               ST_wordTitle.positionAdjust[0] + ST_wordTitle.positionAdjust[1])
