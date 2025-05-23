import ast
import importlib
import os
import shutil
import subprocess
import sys

from utils.utils import StoreDependencies, getBaseDir
from Installation.makeExecutables import makeExecutables, makeLauncherFile

dep = StoreDependencies(globals())

# Inputs
fileNames = ["consoleMessages.programStarting", "UserInput.main_UserInput", "Controller.main_Controller"]

def makeAndOrganizeExecutables(fileNames):
    deleteBinAndBuildFolders() # to start afresh
    for i in range(len(fileNames)):
        print(f"Making executable for {fileNames[i]}")
        makeExecutables(dep, fileNames[i])
    makeLauncherFile(dep)    

def deleteBinAndBuildFolders():
    for folder in ["bin", "build"]:
        if os.path.exists(folder) and os.path.isdir(folder):
            shutil.rmtree(folder)  

if __name__ == "__main__":
    makeAndOrganizeExecutables(fileNames)
