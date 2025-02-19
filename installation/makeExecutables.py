import os
import shutil

class makeExecutables():
    def __init__(self,dep,fileNames):
        # Parameters
        self.dep = dep
        self.fileNames = fileNames
        # Initializer methods
        self.deleteBinAndBuildFolders()

    # To start afresh
    def deleteBinAndBuildFolders(self):
        for folder in ["bin", "build"]:
            if os.path.exists(folder) and os.path.isdir(folder):
                shutil.rmtree(folder)   

    def getDependencies(self,curModule):  
        getModuleImports = GetModuleImports(curModule)
        return getModuleImports.imports



class GetModuleImports():
    def __init__(self, dep, moduleName):
        self.dep = dep
        self.moduleName = moduleName
        self.imports = []
        # Initializer methods
        self.getFilePathForModule()
        self.openFile()
        self.findAndStoreImports()

    def getFilePathForModule(self):
        module_spec = self.dep.importlib.util.find_spec(self.moduleName)
        self.file_path = module_spec.origin

    def openFile(self):   
        with open(self.file_path, "r", encoding="utf-8") as file:
            self.tree = self.dep.ast.parse(file.read(), filename=self.file_path) 

    def findAndStoreImports(self):
         for node in self.dep.ast.walk(self.tree):
            if isinstance(node, self.dep.ast.Import):
                for alias in node.names:
                    self.imports.append(alias.name)
            elif isinstance(node, self.dep.ast.ImportFrom):
                if node.module:  # Ignore relative imports with None
                    self.imports.append(node.module)