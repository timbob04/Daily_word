from EditWordList.utils import makeEditTextBox

def EditWordListApp(app, dep, mainWindow, currentWord="", currentDefinition=""):

    app.setQuitOnLastWindowClosed(False)

    dep.checkForDarkMode_reset()

    window = dep.QMainWindow() # Make a window
    window.setWindowTitle("Edit word") # set its title
    window.setWindowModality(dep.Qt.ApplicationModal)  # Make it modal - blocks entire app
    window.setParent(mainWindow, dep.Qt.Window)  # set window as a child of the Edit Word List window
    
    window.editButtonPressed = False  # turns true when the user presses the 'Edit' button

    fonts = dep.DefineFontSizes(app,dep)
    
    # Define size of app using sentence width and number of lines
    sentence = "000000000000000000000000000000000000000000000000000000"
    numLines = 20
    appSizeOb = dep.AppSize(app,dep,fonts,sentence,numLines)

    UIsizes = dep.DefineUIsizes(appSizeOb)

    container = dep.QWidget()
    
    appBoundaries = makeAppContents_EditWord(dep, container, fonts, UIsizes, appSizeOb, currentWord, currentDefinition) 
    
    dep.makeScrollAreaForCentralWidget(dep, window, container)

    # Resize window to app contents, or the screen width/height with scroll bars if the contents are bigger than the screen
    dep.resizeWindow(window, appBoundaries.right + UIsizes.pad_medium, appBoundaries.bottom + UIsizes.pad_medium, appSizeOb)

    window.show()

    # Add methods to the window object
    def getNewText():
        return container.tb_word.text(), container.tb_def.text()
    
    def exec_():
        # Create a local event loop for the modal window
        loop = dep.QEventLoop()
        
        def checkWindowClosed():
            if not window.isVisible():
                loop.quit()
        
        # Check every 100ms if window is still visible
        timer = dep.QTimer()
        timer.timeout.connect(checkWindowClosed)
        timer.start(100)
        
        loop.exec_()
        return window.editButtonPressed  # Return True if Edit button was pressed, False otherwise
    
    window.getNewText = getNewText
    window.exec_ = exec_

    return window

def makeAppContents_EditWord(dep, container, fonts, UIsizes, appSizeOb, currentWord="", currentDefinition=""):
    
    # App sizing variables
    appBoundaries = dep.AppBoundaries()
    appWidth = min(appSizeOb.sentenceWidth,appSizeOb.screenWidth)

    # Title - "Edit word"
    text = 'Edit word'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["default"]
    position = [UIsizes.pad_medium,UIsizes.pad_medium,0,0]
    t_editWord = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position, bold=True)     
    t_editWord.makeTextObject()
    t_editWord.showTextObject()

    # Update app boundaries
    lowestPoint = t_editWord.positionAdjust[1] + t_editWord.positionAdjust[3]
    rightMostPoint = t_editWord.positionAdjust[0] + t_editWord.positionAdjust[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    # Make edit text box for adding new word
    width_editWord = appWidth - (UIsizes.pad_medium*2)
    start_y = lowestPoint+UIsizes.pad_xsmall
    tb_word, tb_word_pos = makeEditTextBox(dep, container, fonts, UIsizes.pad_medium, start_y, width_editWord, "default", currentWord)
    # Store text boxes as container attributes for access in getNewText()
    container.tb_word = tb_word

    # Update app boundaries
    lowestPoint = tb_word_pos[1] + tb_word_pos[3]
    rightMostPoint = tb_word_pos[0] + tb_word_pos[2]
    appBoundaries.setNewBoundaries(bottom=lowestPoint,right=rightMostPoint)

    # Title - "Edit definition"
    text = 'Edit definition'
    textAlignment = dep.Qt.AlignLeft
    fontScaler = fonts.fontScalers["default"]
    position = [UIsizes.pad_medium,appBoundaries.bottom + UIsizes.pad_large,0,0]
    t_editDef = dep.StaticText(dep, container, fonts.defaultFontSize*fontScaler, text, textAlignment, position, bold=True)     
    t_editDef.makeTextObject()
    t_editDef.showTextObject()

    # Update app boundaries
    lowestPoint = t_editDef.positionAdjust[1] + t_editDef.positionAdjust[3]    
    appBoundaries.setNewBoundaries(bottom=lowestPoint)

    # Make edit text box for adding new definitions
    start_y = lowestPoint+UIsizes.pad_xsmall
    tb_def, tb_def_pos = makeEditTextBox(dep, container, fonts, UIsizes.pad_medium, start_y, width_editWord, "default", currentDefinition)
    # Store text boxes as container attributes for access in getNewText()
    container.tb_def = tb_def

    # Update app boundaries
    lowestPoint = tb_def_pos[1] + tb_def_pos[3]
    appBoundaries.setNewBoundaries(bottom=lowestPoint)

    # Button - "Edit"
    text = "Edit"
    fontScaler = fonts.fontScalers["default"]
    startingYPosition = appBoundaries.bottom + UIsizes.pad_large*2
    position = [UIsizes.pad_medium + width_editWord,startingYPosition,0,0]
    pb_Edit = dep.PushButton(dep, container, fonts.defaultFontSize*fontScaler, text, position)
    pb_Edit.rightAlign()
    pb_Edit.makeButton()
    pb_Edit.showButton()
    # Connect to set the flag when Edit is pressed
    def onEditButtonClicked():
        print("Edit button clicked!")
        container.window().editButtonPressed = True
        print("About to close window...")
        container.window().close()
        print("Window.close() called")
    
    pb_Edit.button.clicked.connect(onEditButtonClicked)

    # Update app boundaries
    lowestPoint = pb_Edit.positionAdjust[1] + pb_Edit.positionAdjust[3]
    appBoundaries.setNewBoundaries(bottom=lowestPoint)

    container.resize(int(appBoundaries.right), int(appBoundaries.bottom))

    # Return the app boundaries
    return appBoundaries