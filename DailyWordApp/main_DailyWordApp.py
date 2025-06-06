from DailyWordApp.makeAppContents import makeAppContents

def runDailyWordApp(app, dep, worker_dailyWordApp):

    # Set the app to not quit when the last window is closed
    app.setQuitOnLastWindowClosed(False)
   
    # Make main window
    window = dep.QMainWindow()
    dep.SetWindowTitle(window, dep.datetime)

    fonts = dep.DefineFontSizes(app,dep)
    
    # Define size of app using sentence width and number of lines
    sentence = "0000000000000000000000000000000000000000000000000000000"
    numLines = 20
    appSizeOb = dep.AppSize(app,dep,fonts,sentence,numLines)

    UIsizes = dep.DefineUIsizes(appSizeOb)

    # Get daily word and daily priority word
    dailyWord = dep.DailyWord(dep)
    dailyPriorityWord = dep.DailyPriorityWord(dep)

    # Make app contents (in central widget)
    container = dep.QWidget()
    width, height = makeAppContents(dep, container, fonts, UIsizes, appSizeOb, dailyWord, dailyPriorityWord, worker_dailyWordApp) 
    dep.makeScrollAreaForCentralWidget(dep, window, container)
    
    # Resize window to app contents, or the screen width/height with scroll bars if the contents are bigger than the screen
    dep.resizeWindow(window, width, height, appSizeOb)

    window.show()

    dep.centerWindowOnScreen(window, app)

    return window