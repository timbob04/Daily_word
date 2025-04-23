from EditWordList.makeAppContents_addNewWord import makeAppContents_AddNewWord
from EditWordList.makeAppContents_editWordList import makeAppContents_EditWordList

def makeEditWordListApp(app, dep):

    window = dep.QMainWindow()
    window.setWindowTitle("Edit word list")

    fonts = dep.DefineFontSizes(app,dep)
    
    # Define size of app using sentence width and number of lines
    sentence = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    numLines = 35
    appSizeOb = dep.AppSize(app,dep,fonts,sentence,numLines)

    UIsizes = dep.DefineUIsizes(appSizeOb)

    container = dep.QWidget()
    
    appBoundaries = makeAppContents_AddNewWord(dep, container, fonts, UIsizes, appSizeOb) 
    appBoundaries = makeAppContents_EditWordList(dep, container, fonts, UIsizes, appSizeOb, appBoundaries)
    
    dep.makeScrollAreaForCentralWidget(dep, window, container)

    # Resize window to app contents, or the screen width/height with scroll bars if the contents are bigger than the screen
    dep.resizeWindow(window, appBoundaries.right, appSizeOb.appHeight, appSizeOb)

    window.show()

    return window


# Something to do with updating the list efficiently (at a specified time):
# listWidget.setUpdatesEnabled(False)   # suppress repaints
# listWidget.clear()
# rebuild_rows()
# listWidget.setUpdatesEnabled(True)    # one repaint here