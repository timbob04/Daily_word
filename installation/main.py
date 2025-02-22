from installation.makeExecutables import makeExecutables
from utils.utils import storeDependencies, getBaseDir
import ast
import importlib
import os
import shutil
import subprocess
import sys

# Make executables
# Reorder folder (one _internal, etc)
# Run installer (inno or package)

print("Starting program")

# Convert these files into executables
fileNames = ["consoleMessages.programStarting"]
consoleNeeded = [True]

dep = storeDependencies(ast, importlib, os, shutil, getBaseDir, subprocess, sys)

# Make the executables
for i in range(len(fileNames)):
    makeExecutables(dep, fileNames[i], consoleNeeded[i])