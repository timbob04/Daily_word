from EditTime.makeAppContents import makeAppContents

def runEditTimeApp(app, dep, worker_editTimeApp):

    # Set the app to not quit when the last window is closed
    app.setQuitOnLastWindowClosed(False)

    window = dep.QMainWindow()
    window.setWindowTitle("Edit time")

    fonts = dep.DefineFontSizes(app,dep)
    
    # Define size of app using sentence width and number of lines
    sentence = "00000000000000000000000000000000000000000"
    numLines = 30
    appSizeOb = dep.AppSize(app,dep,fonts,sentence,numLines)

    UIsizes = dep.DefineUIsizes(appSizeOb)

    container = dep.QWidget()
    
    width, height = makeAppContents(dep, container, fonts, UIsizes, worker_editTimeApp) 
    
    dep.makeScrollAreaForCentralWidget(dep, window, container)

    # Resize window to app contents, or the screen width/height with scroll bars if the contents are bigger than the screen
    dep.resizeWindow(window, width, height, appSizeOb)

    window.show()

    window.EditTimeOb = container.checkTimeEntered

    return window