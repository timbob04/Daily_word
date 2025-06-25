from DailyWordApp.makeAppContents import makeAppContents
from PyQt5.QtCore import QObject, QEvent

def runDailyWordApp(app, dep):

    # Set the app to not quit when the last window is closed
    app.setQuitOnLastWindowClosed(False)
   
    # Make main window
    window = dep.QMainWindow()
    window.titleBar = dep.SetWindowTitle(window, dep.datetime, dep)

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
    width, height = makeAppContents(dep, app, container, fonts, UIsizes, appSizeOb, dailyWord, dailyPriorityWord) 
    dep.makeScrollAreaForCentralWidget(dep, window, container)
    
    # Resize window to app contents, or the screen width/height with scroll bars if the contents are bigger than the screen
    dep.resizeWindow(window, width, height, appSizeOb)

    window.show()

    dep.centerWindowOnScreen(window, app)

    # Make tray icon
    app.icon.changeIconToActiveState()

    watcher = InteractionWatcher(window, app.icon.changeIconToInactiveState)
    window.installEventFilter(watcher)
    window.watcher = watcher

    return window

# This class is used to watch for interactions with the app (any click, focus, or close) and call the callback function
class InteractionWatcher(QObject):
    def __init__(self, window, callbackFunction):
        super().__init__()
        self.window = window        # the window you care about
        self.callbackFunction  = callbackFunction

    def eventFilter(self, obj, event):
        t = event.type()

        # any mouse click, key press, focus, close, minimise/maximise
        eventsToWatchFor = {
            QEvent.MouseButtonPress,
            QEvent.MouseButtonRelease,
            QEvent.KeyPress,
            QEvent.FocusIn,
            QEvent.Close,
            QEvent.WindowStateChange,   # minimise / maximise / restore
        }

        # If the event is in the list of events to watch for and the object is the window or a child of the window, run the callback function
        if t in eventsToWatchFor and (obj is self.window or self.window.isAncestorOf(obj)):
            self.callbackFunction() 
        return False
