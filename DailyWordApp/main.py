# Standard library imports
import os
import sys
from datetime import datetime
import json
import platform
import inspect
import re

# Third-party imports
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, 
    QVBoxLayout, QWidget, QScrollArea, 
    QPushButton, QStyle, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QFont, QFontMetrics, QCursor, 
    QTextDocument, QTextOption
)

# Local imports
from utils.utils import (
    readJSONfile, getBaseDir, 
    StoreDependencies, softHyphenateLongWords
)
from utils.utils_UI import (
    DefineUIsizes, DefineFontSizes, StaticText,
    centerWindowOnScreen, MakeTextWithMaxHeight,
    AppSize, AppBoundaries, PushButton
)
from utils.styles import buttonStyle
from DailyWordApp.getDailyWords import DailyWord, DailyPriorityWord
from DailyWordApp.makeAppContents import makeAppContents
from DailyWordApp.utils import SetWindowTitle

# Store a reference to each dependency above
dep = StoreDependencies(globals())

def runDailyWordApp():
    
    # Make application
    app = QApplication(sys.argv)
    window = QMainWindow()
    SetWindowTitle(window, datetime)

    fonts = DefineFontSizes(QApplication,dep)
    
    # Define size of app using sentence and number of lines
    sentence = "0000000000000000000000000000000000000000000000000000000"
    numLines = 20
    appSizeOb = AppSize(dep,fonts,sentence,numLines)

    UIsizes = DefineUIsizes(appSizeOb)

    # Get daily word and daily priority word
    dailyWord = DailyWord(dep)
    dailyPriorityWord = DailyPriorityWord(dep)

    makeAppContents(dep, window, fonts, UIsizes, appSizeOb)   

    # This is now in a function, that either 1) resizes smaller to the app's content boundaries,
    # or 2) resizes to the size of the screen and adds a scroll area if the content is too large,
    # separately for horizontal and vertical axes (only apply if actually needed)
    window.resize(appSizeOb.sentenceWidth,appSizeOb.appHeight)

    window.show()
    centerWindowOnScreen(window, QApplication)

    # Run application's event loop
    exit_code = app.exec_()
    sys.exit(exit_code)

if __name__ == "__main__":
    runDailyWordApp()