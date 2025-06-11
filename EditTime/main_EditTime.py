from EditTime.makeAppContents import makeAppContents

def makeEditTimeApp(app, dep):

    window = dep.QMainWindow()
    window.setWindowTitle("Edit time")

    fonts = dep.DefineFontSizes(app,dep)
    
    # Define size of app using sentence width and number of lines
    sentence = "0000000000000000000000000000000000"
    numLines = 15
    appSizeOb = dep.AppSize(app,dep,fonts,sentence,numLines)

    UIsizes = dep.DefineUIsizes(appSizeOb)

    container = dep.QWidget()
    
    appBoundaries = makeAppContents(dep, container, fonts, UIsizes, appSizeOb) 
    
    dep.makeScrollAreaForCentralWidget(dep, window, container)

    # Resize window to app contents, or the screen width/height with scroll bars if the contents are bigger than the screen
    dep.resizeWindow(window, appBoundaries.right, appSizeOb.appHeight, appSizeOb)

    window.show()

    return window