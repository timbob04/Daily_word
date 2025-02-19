from installation.makeExecutables import makeExecutables
from utils.utils import storeDependencies
import ast
import importlib.util
import os

# Convert these files into executables
fileNames = ["consoleMessages.programStarting"]

dep = storeDepdenencies(ast, importlib.util, os)

