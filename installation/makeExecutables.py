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
        # Get icon path for macOS
        icon_cmd = []
        if self.dep.sys.platform == 'darwin':
            root_dir, _ = self.dep.getBaseDir(self.dep.sys, self.dep.os)
            icon_path = self.dep.os.path.join(root_dir, 'accessoryFiles', 'app_icon.icns')
            if self.dep.os.path.exists(icon_path):
                icon_cmd = ['--icon', icon_path]

        self.pyInstallerCommand = [
            "pyinstaller", "--onedir", "--noupx", "--clean", "--windowed", "--noconsole",
            "--name", self.executableName,
            "--distpath", "bin",
            self.pythonFile,
            *self.hidden_imports_cmd,
            *self.neededFoldersCmd,
            *icon_cmd
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


def makeLauncher(dep, app_name="UserInput", binary_name="PingController"):

    if dep.sys.platform != 'darwin':
        return
    
    print("Making launcher for mac")

    project_dir, _ = dep.getBaseDir(dep.sys, dep.os)
    script_path = dep.os.path.join(project_dir, f"{app_name}.applescript")
    app_path = dep.os.path.join(project_dir, f"{app_name}.app")

    # Start afresh
    if dep.os.path.exists(app_path):
        dep.subprocess.run(["rm", "-rf", app_path], check=True)

    applescript = f'''\
        tell application "Terminal"
            set appPath to POSIX path of (path to me)
            set binPath to appPath & "../bin/{binary_name}.app/Contents/MacOS/{binary_name}"
            do script binPath
            delay 0.5
            repeat while busy of window 1
                delay 0.2
            end repeat
            close window 1
        end tell
        '''

    # Write the AppleScript to file
    with open(script_path, 'w') as f:
        f.write(applescript)

    # Compile into a .app
    dep.subprocess.run(["osacompile", "-o", app_path, script_path], check=True)

    # Remove temporary .applescript
    dep.os.remove(script_path)

    print(f"✅ Created .app launcher at: {app_path}")



