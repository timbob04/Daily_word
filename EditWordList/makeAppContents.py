from EditWordList.utils import addNewWordTextBoxes
from EditWordList.makeWordList import MakeWordList

def makeAppContents(dep, container, fonts, UIsizes, appSizeOb):

    # App sizing variables
    appBoundaries = dep.AppBoundaries()
    appWidth = min(appSizeOb.sentenceWidth,appSizeOb.screenWidth)

    # Title - "Add new word"
    text = 'Add new word'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["large"]
    position = [UIsizes.pad_medium,UIsizes.pad_medium,0,0]
    t_addNewWordTitle = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position, bold=True)     
    t_addNewWordTitle.makeTextObject()
    t_addNewWordTitle.showTextObject()

    # Update app boundaries
    lowestPoint = t_addNewWordTitle.positionAdjust[1] + t_addNewWordTitle.positionAdjust[3]
    rightMostPoint = t_addNewWordTitle.positionAdjust[0] + t_addNewWordTitle.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    # Title - "Word" (small)
    text = 'Word'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["small"]
    position = [UIsizes.pad_medium,appBoundaries.bottom+UIsizes.pad_medium,0,0]
    t_wordTitle = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position)     
    t_wordTitle.makeTextObject()
    t_wordTitle.showTextObject()
    
    # Update app boundaries
    lowestPoint = t_wordTitle.positionAdjust[1] + t_wordTitle.positionAdjust[3]
    rightMostPoint = t_wordTitle.positionAdjust[0] + t_wordTitle.positionAdjust[2]
    wordTitle_top = t_wordTitle.positionAdjust[1]
    appBoundaries.setNewBoundaries(bottom=lowestPoint, right=rightMostPoint, store={'wordTitle_top': wordTitle_top})

    # Make edit text boxes for adding new words (with their definitions)
    editTextBoxes = addNewWordTextBoxes(dep, container, fonts)
    width_editTextBox_word = appWidth * 0.2
    editTextBoxes.makeEditTextBox_word(UIsizes.pad_medium, lowestPoint+UIsizes.pad_xsmall, width_editTextBox_word)
    rightEdgeOfBox_addWord = editTextBoxes.pos_word[0] + editTextBoxes.pos_word[2]
    width_editTextBox_definition = appWidth * 0.6
    editTextBoxes.makeEditTextBox_definition(rightEdgeOfBox_addWord+UIsizes.pad_medium, lowestPoint+UIsizes.pad_xsmall, width_editTextBox_definition)

    # Update app boundaries
    lowestPoint = editTextBoxes.pos_word[1] + editTextBoxes.pos_word[3]
    rightMostPoint = editTextBoxes.pos_definition[0] + editTextBoxes.pos_definition[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    # Title - "Definition" (small)
    text = 'Definition'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["small"]
    startingPos_x = editTextBoxes.pos_definition[0]
    position = [startingPos_x,appBoundaries.wordTitle_top,0,0]
    t_definitionTitle = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position)     
    t_definitionTitle.makeTextObject()
    t_definitionTitle.showTextObject()

    # Button - "Add"
    text = "Add"
    fontScaler = fonts.fontScalers["default"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_medium
    position = [UIsizes.pad_medium,startingYPosition,0,0]
    pb_add = dep.PushButton(dep, container, fonts.defaultFontSize*fontScaler, text, position)
    pb_add.makeButton()
    pb_add.showButton()
    # Run the functions required to add the new word and definition to the word list (json and GUI)
    pb_add.button.clicked.connect(lambda: editTextBoxes.AddButtonPressed()) # add to json
    pb_add.button.clicked.connect(lambda: wordList.wordAdded()) # add to GUI

    # Update app boundaries
    lowestPoint = pb_add.positionAdjust[1] + pb_add.positionAdjust[3]
    appBoundaries.setNewBoundaries(bottom=lowestPoint)

    # Draw a line to separate the 'Add words' and 'Edit words' main sections
    # Define the function to implement in the window's paintEvent attribute
    def drawLine(event, xStart, xEnd, yPoint, window, dep, lineThickness=10):
        painter = dep.QPainter(window)
        pen = dep.QPen(dep.Qt.gray, lineThickness)  # Set the color and thickness of the line
        painter.setPen(pen)
        painter.drawLine(int(xStart),int(yPoint),int(xEnd),int(yPoint))  # Draw the line
    # Run the function
    xStart = UIsizes.pad_medium
    xEnd = appBoundaries.right
    yPoint = appBoundaries.bottom + UIsizes.pad_medium
    lineThickness = 5
    container.paintEvent = lambda event: drawLine(event, xStart, xEnd, yPoint, container, dep, lineThickness)

    # Update app boundaries
    lowestPoint = yPoint + lineThickness
    appBoundaries.setNewBoundaries(right=appBoundaries.right + UIsizes.pad_medium,bottom=lowestPoint)

    # Title - "Edit word list"
    text = 'Edit word list'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["large"]
    startPos_y = appBoundaries.bottom + UIsizes.pad_medium
    position = [UIsizes.pad_medium,startPos_y,0,0]
    t_editWordListTitle = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position, bold=True)     
    t_editWordListTitle.makeTextObject()
    t_editWordListTitle.showTextObject()

    # Update app boundaries
    lowestPoint = t_editWordListTitle.positionAdjust[1] + t_editWordListTitle.positionAdjust[3]
    rightMostPoint = t_editWordListTitle.positionAdjust[0] + t_editWordListTitle.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    wordList = MakeWordList(dep, container, fonts, UIsizes, appSizeOb, appBoundaries, editTextBoxes)
    appBoundaries = wordList.appBoundaries

    container.resize(int(appBoundaries.right), int(appBoundaries.bottom+UIsizes.pad_medium))

    # Return the app boundaries
    return appBoundaries
    