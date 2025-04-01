def runDailyWordApp(app, dep):
   
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

    appBoundaries = dep.makeAppContents(dep, window, fonts, UIsizes, appSizeOb, dailyWord, dailyPriorityWord)   

    # To do:
    # This is now in a function, that either 1) resizes smaller to the app's content boundaries,
    # or 2) resizes to the size of the screen and adds a scroll area if the content is too large,
    # separately for horizontal and vertical axes (only apply if actually needed)
    window.resize(int(appBoundaries.right + UIsizes.pad_medium),int(appBoundaries.bottom + UIsizes.pad_medium))

    window.show()

    dep.centerWindowOnScreen(window, app)

    return window
    
    # print("Window geometry:", window.geometry())
    # print("Is visible?", window.isVisible())
    # window.raise_()
    # window.activateWindow()
