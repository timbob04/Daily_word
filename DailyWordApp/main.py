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
    centerWindowOnScreen, MakeTextWithMaxHeight
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
    
    # Create a central widget for the application
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    fonts = DefineFontSizes(QApplication)
    UIsizes = DefineUIsizes()

    # Get daily word and daily priority word
    dailyWord = DailyWord(dep)
    dailyPriorityWord = DailyPriorityWord(dep)

    makeAppContents(dep, central_widget, fonts, UIsizes)    

    window.show()
    centerWindowOnScreen(window, QApplication)

    # Run application's event loop
    exit_code = app.exec_()
    sys.exit(exit_code)

if __name__ == "__main__":
    runDailyWordApp()