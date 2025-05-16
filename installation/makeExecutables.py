class makeExecutables():
    def __init__(self,dep, fileName):
        # Input parameters
        self.dep = dep
        self.fileName = fileName    
        # Fixed parameters
        self.projectRoot, _ = dep.getBaseDir(dep.sys, dep.os)
        self.executableName = self.fileName.split(".")[-1]
        # Initializer methods
        self.getPythonFilePath()
        self.getModuleDependencies()
        self.makeCommandsToAddDependencies()
        self.makeCommandsToAddNeededFolders()
        self.createPyInstallerCommand()
        self.runPyInstallerCommand()                  

    def getPythonFilePath(self):
        self.pythonFile = self.dep.os.path.join(self.projectRoot, self.fileName.replace(".", self.dep.os.sep)) + ".py"              

    def getModuleDependencies(self):  
        getModuleImports = GetModuleImports(self.dep, self.fileName)
        self.dependencies = getModuleImports.imports
    
    def makeCommandsToAddDependencies(self):
        self.hidden_imports_cmd = [
            f'--hidden-import={dep}' 
            for dep in self.dependencies
            ]

    def makeCommandsToAddNeededFolders(self):
        folders = [ self.fileName.split(".")[0], "utils" ]
        separator = ";" if self.dep.os.name == "nt" else ":"
        self.neededFoldersCmd = [
            f'--add-data={self.dep.os.path.join(self.projectRoot, folder)}{separator}{folder}'
            for folder in folders
        ] 

    def createPyInstallerCommand(self):    
        self.pyInstallerCommand = [
            "pyinstaller", "--onedir", "--noupx", "--clean", "--windowed",
            "--name", self.executableName,
            "--distpath", "bin",
            self.pythonFile,
            *self.hidden_imports_cmd,
            *self.neededFoldersCmd
        ] 

    def runPyInstallerCommand(self):   
        self.dep.subprocess.run(self.pyInstallerCommand , capture_output=True, text=True)

# Finds all imports at the top of the main file being made into the executable
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
        self.imports = set()  # Use a set to avoid duplicates
        for node in self.dep.ast.walk(self.tree):
            if isinstance(node, self.dep.ast.Import):
                for alias in node.names:
                    self.imports.add(alias.name)
            elif isinstance(node, self.dep.ast.ImportFrom):
                if node.module:  # Ignore relative imports with None
                    self.imports.add(node.module)
        self.imports = list(self.imports)  # Convert back to a list          