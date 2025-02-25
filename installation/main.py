import ast
import importlib
import os
import shutil
import subprocess
import sys

from utils.utils import storeDependencies, getBaseDir
from installation.makeExecutables import makeExecutables
from installation.arrangeExecutableFiles import organizeExecutableFiles

dep = storeDependencies(ast, importlib, os, shutil, getBaseDir, subprocess, sys)

# Make the executables
fileNames = ["consoleMessages.programStarting"]
consoleNeeded = [True]
for i in range(len(fileNames)):
    makeExecutables(dep, fileNames[i], consoleNeeded[i])

# Organize the executables
organizeExecutableFiles(dep)    
