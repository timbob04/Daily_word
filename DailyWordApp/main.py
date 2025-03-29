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
    AppSize, AppBoundaries, PushButton, Toggle
)
from utils.styles import (
    buttonStyle, toggleStyle
) 
from DailyWordApp.getDailyWords import DailyWord, DailyPriorityWord
from DailyWordApp.makeAppContents import makeAppContents
from DailyWordApp.utils import SetWindowTitle

# Store a reference to each dependency above
dep = StoreDependencies(globals())

def runDailyWordApp():
    
    # Make application
    app = dep.QApplication(sys.argv)
    window = dep.QMainWindow()
    dep.SetWindowTitle(window, dep.datetime)

    fonts = dep.DefineFontSizes(dep.QApplication,dep)
    
    # Define size of app using sentence and number of lines
    sentence = "0000000000000000000000000000000000000000000000000000000"
    numLines = 20
    appSizeOb = dep.AppSize(dep,fonts,sentence,numLines)

    UIsizes = dep.DefineUIsizes(appSizeOb)

    # Get daily word and daily priority word
    dailyWord = dep.DailyWord(dep)
    dailyPriorityWord = dep.DailyPriorityWord(dep)

    appBoundaries = dep.makeAppContents(dep, window, fonts, UIsizes, appSizeOb, dailyWord, dailyPriorityWord)   

    # This is now in a function, that either 1) resizes smaller to the app's content boundaries,
    # or 2) resizes to the size of the screen and adds a scroll area if the content is too large,
    # separately for horizontal and vertical axes (only apply if actually needed)
    window.resize(int(appBoundaries.right + UIsizes.pad_medium),int(appBoundaries.bottom + UIsizes.pad_medium))

    window.show()
    dep.centerWindowOnScreen(window, QApplication)

    # Run application's event loop
    exit_code = app.exec_()
    sys.exit(exit_code)

if __name__ == "__main__":
    runDailyWordApp()