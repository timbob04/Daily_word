from StartProgramGUI.utils import CheckIfTimeEnteredCorrectly

def makeAppContents(dep, container, fonts, UIsizes, worker_startProgramApp):

    # App sizing variables
    appBoundaries = dep.AppBoundaries()

    # For launching the main app when the start button is pressed, and the time is entered correctly
    def launchMainApp():
        worker_startProgramApp.shutdown()  

    # Text - "Choose time for daily word to appear"
    text = 'Choose time for daily word to appear'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["default"]
    position = [UIsizes.pad_medium,UIsizes.pad_medium,0,0]
    t_chooseTimeTitle = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position)     
    t_chooseTimeTitle.makeTextObject()
    t_chooseTimeTitle.showTextObject()

    # Update app boundaries
    lowestPoint = t_chooseTimeTitle.positionAdjust[1] + t_chooseTimeTitle.positionAdjust[3]
    rightMostPoint = t_chooseTimeTitle.positionAdjust[0] + t_chooseTimeTitle.positionAdjust[2]
    centerTopText = t_chooseTimeTitle.positionAdjust[0] + t_chooseTimeTitle.positionAdjust[2]/2
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint,store={'centerTopText': centerTopText})

    # Width of one digit
    bounding_rect = t_chooseTimeTitle.fontMetrics.boundingRect(0,0,0,0, dep.Qt.AlignCenter, "0") 
    widthOneDigit = bounding_rect.width()    

    # Edit text box - hours field
    editTextBox_hours = dep.EditTextBox(dep, container, fonts)
    editTextBox_hours.numDigits = 3 # define width of box by number of digits
    startingPoint_x = appBoundaries.centerTopText - (widthOneDigit/2)
    startingPoint_y = appBoundaries.bottom + UIsizes.pad_medium
    editTextBox_hours.makeEditTextBox(startingPoint_x, startingPoint_y, 0)
    editTextBox_hours.rightAlign()
    editTextBox_hours.tb.show()

    # Update app boundaries
    textBoxGeometry = editTextBox_hours.tb.geometry()
    lowestPoint = textBoxGeometry.bottom()
    middleRow_textBoxes = textBoxGeometry.top() + textBoxGeometry.height() / 2
    topRow_textBoxes = textBoxGeometry.top()
    centerText_hours = textBoxGeometry.left() + textBoxGeometry.width() / 2
    appBoundaries.setNewBoundaries(bottom=lowestPoint,store={'middleRow_textBoxes': middleRow_textBoxes, 
                                                             'topRow_textBoxes': topRow_textBoxes,
                                                             'centerText_hours': centerText_hours})

    # Text: Colon in between hours and minutes field
    text = ':'
    textAlignment = dep.Qt.AlignCenter
    fontScaler = fonts.fontScalers["default"]
    position = [appBoundaries.centerTopText, appBoundaries.middleRow_textBoxes, 0, 0]
    t_colon = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position)
    t_colon.centerAlign_H()
    t_colon.centerAlign_V()
    t_colon.makeTextObject()
    t_colon.showTextObject()

    # Edit text box - minutes field
    editTextBox_minutes = dep.EditTextBox(dep, container, fonts)
    editTextBox_minutes.numDigits = 3 # define width of box by number of digits
    startingPoint_x = appBoundaries.centerTopText + (widthOneDigit/2)
    startingPoint_y = appBoundaries.topRow_textBoxes
    editTextBox_minutes.makeEditTextBox(startingPoint_x, startingPoint_y, 0)

    # Update app boundaries
    textBoxGeometry = editTextBox_minutes.tb.geometry()
    rightOfMinutesBox = textBoxGeometry.right()
    centerText_minutes = textBoxGeometry.left() + textBoxGeometry.width() / 2
    appBoundaries.setNewBoundaries(right=rightOfMinutesBox,store={'centerText_minutes': centerText_minutes,
                                                                  'rightOfMinutesBox': rightOfMinutesBox})

    # Text - 24 hour format text
    text = '(24 hr format)'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["small"]
    position = [appBoundaries.rightOfMinutesBox+UIsizes.pad_medium, appBoundaries.middleRow_textBoxes, 0, 0]
    t_24hourFormat = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position)
    t_24hourFormat.centerAlign_V()
    t_24hourFormat.makeTextObject()
    t_24hourFormat.showTextObject()

    # Update app boundaries
    rightMostPoint = t_24hourFormat.positionAdjust[0] + t_24hourFormat.positionAdjust[2]
    appBoundaries.setNewBoundaries(right=rightMostPoint)

    # Text - HH
    text = 'HH'
    textAlignment = dep.Qt.AlignCenter
    fontScaler = fonts.fontScalers["small"]
    position = [appBoundaries.centerText_hours, appBoundaries.bottom+UIsizes.pad_xsmall, 0, 0]
    t_HH = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position)
    t_HH.centerAlign_H()
    t_HH.makeTextObject()
    t_HH.showTextObject()

    # Text - MM
    text = 'MM'
    textAlignment = dep.Qt.AlignCenter
    fontScaler = fonts.fontScalers["small"]
    position = [appBoundaries.centerText_minutes, appBoundaries.bottom+UIsizes.pad_xsmall, 0, 0]
    t_MM = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position)
    t_MM.centerAlign_H()
    t_MM.makeTextObject()
    t_MM.showTextObject()

    # Update app boundaries
    lowestPoint = t_HH.positionAdjust[1] + t_HH.positionAdjust[3]
    appBoundaries.setNewBoundaries(bottom=lowestPoint)

    # Text - 'Time entered incorrectly'
    text = 'Time entered\nincorrectly'
    textAlignment = dep.Qt.AlignCenter
    fontScaler = fonts.fontScalers["small"]
    position = [appBoundaries.centerTopText, appBoundaries.bottom+UIsizes.pad_small, 0, 0]
    t_timeEnteredIncorrectly = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position)
    t_timeEnteredIncorrectly.color = 'red'
    t_timeEnteredIncorrectly.centerAlign_H()
    t_timeEnteredIncorrectly.makeTextObject()

    # Update app boundaries
    lowestPoint = t_timeEnteredIncorrectly.positionAdjust[1] + t_timeEnteredIncorrectly.positionAdjust[3]
    appBoundaries.setNewBoundaries(bottom=lowestPoint)

    # Push button - 'Start'
    text = "Start"
    fontScaler = fonts.fontScalers["default"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_large
    position = [appBoundaries.right,startingYPosition,0,0]
    pb_start = dep.PushButton(dep, container, fonts.defaultFontSize*fontScaler, text, position)
    pb_start.rightAlign()
    pb_start.makeButton()
    pb_start.showButton()

    # Update app boundaries
    rightMostPoint = pb_start.positionAdjust[0] + pb_start.positionAdjust[2]
    lowestPoint = pb_start.positionAdjust[1] + pb_start.positionAdjust[3]
    appBoundaries.setNewBoundaries(right=rightMostPoint,bottom=lowestPoint)

    # Object to check if time is entered correctly, and lanch main app, if the start time is entered correctly
    container.checkTimeEntered = CheckIfTimeEnteredCorrectly(dep, editTextBox_hours, 
                editTextBox_minutes, t_timeEnteredIncorrectly, launchMainApp)
    editTextBox_hours.tb.textChanged.connect(container.checkTimeEntered.checkTime_HH)
    editTextBox_minutes.tb.textChanged.connect(container.checkTimeEntered.checkTime_MM)
    pb_start.button.clicked.connect(container.checkTimeEntered.buttonPressed)

    appContentsWidth = appBoundaries.right + UIsizes.pad_medium
    appContentsHeight = appBoundaries.bottom + UIsizes.pad_medium

    container.resize(int(appContentsWidth),int(appContentsHeight))

    # Return the app boundaries
    return appContentsWidth, appContentsHeight

        



