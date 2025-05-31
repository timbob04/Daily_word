def makeAppContents(dep, container, fonts, UIsizes, worker_stopProgramApp):

    # App sizing variables
    appBoundaries = dep.AppBoundaries()

    # Text - "Choose time for daily word to appear"
    text = 'The program is currently running'
    textAlignment = dep.Qt.AlignCenter
    fontScaler = fonts.fontScalers["default"]
    position = [UIsizes.pad_medium,UIsizes.pad_medium,0,0]
    t_programRunning = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position)     
    t_programRunning.makeTextObject()
    t_programRunning.showTextObject()

    # Update app boundaries
    lowestPoint = t_programRunning.positionAdjust[1] + t_programRunning.positionAdjust[3]
    rightMostPoint = t_programRunning.positionAdjust[0] + t_programRunning.positionAdjust[2]
    centerTopText = t_programRunning.positionAdjust[0] + t_programRunning.positionAdjust[2]/2
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint,store={'centerTopText': centerTopText})

    # Push button - 'Stop program'
    text = "Stop program"
    fontScaler = fonts.fontScalers["default"]
    startingYPosition = lowestPoint + UIsizes.pad_large
    position = [centerTopText,startingYPosition,0,0]
    pb_stopProgram = dep.PushButton(dep, container, fonts.defaultFontSize*fontScaler, text, position)
    pb_stopProgram.centerAlign_H()
    pb_stopProgram.makeButton()
    pb_stopProgram.showButton()
    pb_stopProgram.button.clicked.connect(worker_stopProgramApp.shutdown)

    # Update app boundaries
    lowestPoint = pb_stopProgram.positionAdjust[1] + pb_stopProgram.positionAdjust[3]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    appContentsWidth = appBoundaries.right + UIsizes.pad_medium
    appContentsHeight = appBoundaries.bottom + UIsizes.pad_medium

    container.resize(int(appContentsWidth),int(appContentsHeight))

    # Return the app boundaries
    return appContentsWidth, appContentsHeight

        



