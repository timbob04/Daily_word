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
    QVBoxLayout, QWidget, QScrollArea
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
    GetAppSizeUsingSentence
)
from DailyWordApp.getDailyWords import DailyWord, DailyPriorityWord
from DailyWordApp.makeAppContents import makeAppContents
from DailyWordApp.utils import SetWindowTitle

dep = StoreDependencies(globals())

def runDailyWordApp():
    
    # Make application
    app = QApplication(sys.argv)
    window = QMainWindow()
    SetWindowTitle(window, datetime)

    fonts = DefineFontSizes(QApplication,dep)
    UIsizes = DefineUIsizes()

    # Define size of app using sentence
    sentence = "There once was a man who lived in a boat, who then died"
    appSizeOb = GetAppSizeUsingSentence(dep,fonts,sentence)

    # Get daily word and daily priority word
    dailyWord = DailyWord(dep)
    dailyPriorityWord = DailyPriorityWord(dep)

    # makeAppContents(dep, central_widget, fonts, UIsizes)   

    window.resize(appSizeOb.appWidth,appSizeOb.appWidth)

    window.show()
    centerWindowOnScreen(window, QApplication)

    # Run application's event loop
    exit_code = app.exec_()
    sys.exit(exit_code)

if __name__ == "__main__":
    runDailyWordApp()