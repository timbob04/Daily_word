from StartProgramGUI.makeAppContents import makeAppContents

def runStartProgramApp(app, dep, worker_startProgramApp):

    # Set the app to not quit when the last window is closed
    app.setQuitOnLastWindowClosed(False)
   
    # Make main window
    window = dep.QMainWindow()
    window.setWindowTitle("Start program")
    window.startButtonClicked = False  # Initialize flag to track if Start button was clicked

    fonts = dep.DefineFontSizes(app,dep)
    
    # Define size of app using sentence width and number of lines
    sentence = "000000000000000000000000000000000000000000"
    numLines = 15
    appSizeOb = dep.AppSize(app,dep,fonts,sentence,numLines)

    UIsizes = dep.DefineUIsizes(appSizeOb)

    # Make app contents (in central widget)
    container = dep.QWidget()
    width, height = makeAppContents(dep, container, fonts, UIsizes, worker_startProgramApp) 
    dep.makeScrollAreaForCentralWidget(dep, window, container)
    
    # Resize window to app contents, or the screen width/height with scroll bars if the contents are bigger than the screen
    dep.resizeWindow(window, width, height, appSizeOb)

    window.show()

    dep.centerWindowOnScreen(window, app)

    window.startTimeOb = container.checkTimeEntered

    return window
