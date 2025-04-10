def runDailyWordApp(app, dep):

    # Set the app to not quit when the last window is closed
    app.setQuitOnLastWindowClosed(True)
   
    # Make main window
    window = dep.QMainWindow()
    dep.SetWindowTitle(window, dep.datetime)

    fonts = dep.DefineFontSizes(app,dep)
    
    # Define size of app using sentence and number of lines
    sentence = "0000000000000000000000000000000000000000000000000000000"
    numLines = 20
    appSizeOb = dep.AppSize(app,dep,fonts,sentence,numLines)

    UIsizes = dep.DefineUIsizes(appSizeOb)

    # Get daily word and daily priority word
    dailyWord = dep.DailyWord(dep)
    dailyPriorityWord = dep.DailyPriorityWord(dep)

    # Make app contents (in central widget)
    container = dep.QWidget()
    width, height = dep.makeAppContents(dep, container, fonts, UIsizes, appSizeOb, dailyWord, dailyPriorityWord) 
    makeScrollAreaForCentralWidget(dep, window, container)
    
    # Resize window to app contents, or the screen width/height with scroll bars if the contents are bigger than the screen
    resizeWindow(window, width, height, appSizeOb)

    window.show()

    dep.centerWindowOnScreen(window, app)

    return window

def makeScrollAreaForCentralWidget(dep, window, container):
    scrollArea = dep.QScrollArea()
    scrollArea.setWidget(container)
    scrollArea.setHorizontalScrollBarPolicy(dep.Qt.ScrollBarAsNeeded)
    scrollArea.setVerticalScrollBarPolicy(dep.Qt.ScrollBarAsNeeded)
    scrollArea.setAlignment(dep.Qt.AlignCenter)
    scrollArea.setContentsMargins(0, 0, 0, 0)
    window.setCentralWidget(scrollArea)
   
def resizeWindow(window, width, height, appSizeOb, percentage=0.03):
    # Determine desired window size, which is a litte bigger than the contents
    widthOfWindowWithContents = width + width * percentage
    heightOfWindowWithContents = height + height * percentage

    # Make sure the window is not bigger than the screen
    windowFinalWidth = min(widthOfWindowWithContents,appSizeOb.screenWidth)
    windowFinalHeight = min(heightOfWindowWithContents,appSizeOb.screenHeight)

    window.resize(int(windowFinalWidth),int(windowFinalHeight))