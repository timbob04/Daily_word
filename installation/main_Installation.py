import ast
import importlib
import os
import shutil
import subprocess
import sys
import plistlib

from utils.utils import StoreDependencies, getBaseDir
from Installation.makeExecutables import makeExecutables

dep = StoreDependencies(globals())

# Inputs
fileNames = [ "PingController.main_PingController", "Controller.main_Controller"]
appName = ["Daily word", "Controller"]
backgroundApp = [False, True]

def makeAndOrganizeExecutables(fileNames):
    deleteBinAndBuildFolders() # to start afresh
    for i in range(len(fileNames)):
        print(f"Making executable for {fileNames[i]}")
        makeExecutables(dep, fileNames[i], appName[i], backgroundApp[i])

def deleteBinAndBuildFolders():
    for folder in ["bin", "build"]:
        if os.path.exists(folder) and os.path.isdir(folder):
            shutil.rmtree(folder)  

if __name__ == "__main__":
    makeAndOrganizeExecutables(fileNames)
