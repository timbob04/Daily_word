
def organizeExecutableFiles(dep):

    # Define bin and dependencies folders
    nameOfBinFolder = "bin"
    nameOfDepFolder = "_internal" # the location where PyInstaller puts each executable's dependencies
    
    # Make paths
    curDir = dep.getBaseDir(dep.sys, dep.os)
    dir_bin = dep.os.path.join(curDir,'..', nameOfBinFolder)
    dir_targetDepFolder = dep.os.path.join(dir_bin,nameOfDepFolder)

    # Make _dependencies folder in bin
    dep.os.makedirs(dir_targetDepFolder, exist_ok=True)

    # Loop through all items in the bin folder
    for folderItem in dep.os.listdir(dir_bin):

        dir_folderItem = dep.os.path.join(dir_bin, folderItem)
        dir_curDepFolder = ""
        
        if dir_folderItem == dir_targetDepFolder:
            continue

        # Delete any .app folders
        if folderItem.endswith(".app") and dep.os.path.isdir(dir_folderItem):
            dep.shutil.rmtree(dir_folderItem)
            continue

        # Rename any folders with the same name as an executable, so the executable can be moved to the bin folder
        if dep.os.path.isdir(dir_folderItem):    
            dep.os.rename(dir_folderItem, dir_folderItem + "_temp")
            dir_folderItem += "_temp"
            dir_curDepFolder = dep.os.path.join(dir_bin, dir_folderItem , nameOfDepFolder)

        if dep.os.name == "nt": 
            exe_path = dep.os.path.join(dir_folderItem, folderItem + ".exe") 
        else:
            exe_path = dep.os.path.join(dir_folderItem, folderItem) 

        # Move any executables in the current folder to the bin folder
        if dep.os.path.exists(exe_path) and dep.os.path.isfile(exe_path):
            dep.shutil.move(exe_path, dir_bin)

        # Move any dependencies in the current folder to the _dependencies folder
        if dep.os.path.isdir(dir_curDepFolder):    
            moveDependencies(dep, dir_curDepFolder, dir_targetDepFolder)

        # Now remove the remainder of the executable folder
        if dep.os.path.isdir(dir_folderItem):
            dep.shutil.rmtree(dir_folderItem)

def moveDependencies(dep, folder_source, folder_dest):

    # Loop through all items in the source folder
    for item in dep.os.listdir(folder_source):
        curItemPath_source = dep.os.path.join(folder_source, item)
        curItemPath_dest = dep.os.path.join(folder_dest, item)

        # If item is folder
        if dep.os.path.isdir(curItemPath_source):
            if not dep.os.path.exists(curItemPath_dest):  # If folder doesn't exist in destination, copy it
                dep.shutil.copytree(curItemPath_source, curItemPath_dest)
            else:  # If folder does exist in destination, recurse inside (so can now copy new files inside)
                moveDependencies(curItemPath_source, curItemPath_dest)
        
        # If it's a file, copy over, but only if it doesn't exist in destination
        elif dep.os.path.isfile(curItemPath_source) and not dep.os.path.exists(curItemPath_dest):
            dep.shutil.copy2(curItemPath_source, curItemPath_dest)