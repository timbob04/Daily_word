def getBaseDir(sys, os):
    # Check if the program is running as an executable
    if getattr(sys, 'frozen', False):                
        baseDir = os.path.dirname(sys.executable)
        if sys.platform == 'darwin':
            # macOS: .../YourApp.app/Contents/MacOS → go up 3 (.app), then 1 (bin)
            rootDir = os.path.abspath(os.path.join(baseDir, "../../../.."))
        else:
            # Windows or other: .../bin/exe_folder → go up 2
            rootDir = os.path.abspath(os.path.join(baseDir, "../.."))
    else:
        # If not, find where this python function is being called from, not where this function actually is
        caller_file = sys._getframe(1).f_globals.get("__file__", "")
        if caller_file:  
            baseDir = os.path.dirname(os.path.abspath(caller_file))  # Use the caller script's location
        else:
            baseDir = os.getcwd()  # Default to current working directory if __file__ is missing
        rootDir = os.path.abspath(os.path.join(baseDir, ".."))    

    return rootDir, baseDir
    
def readJSONfile(json, filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data
    except (json.JSONDecodeError, FileNotFoundError, IOError):
        return None
    
def softHyphenateLongWords(text, max_word_length=15):
    # Add soft hyphens to long words, which are only used if the word needs to be wrapped
    words = text.split()  # Split text by spaces
    wrapped_words = []
    for word in words:
        if len(word) > max_word_length:
            # Insert soft hyphens at every max_word_length characters for long words
            wrapped_word = '\u00AD'.join([word[i:i+max_word_length] for i in range(0, len(word), max_word_length)]) # list comprehensions for storing each part of the long word, and then using join to join them all with soft hyphens in between
            wrapped_words.append(wrapped_word)
        else:
            wrapped_words.append(word)
    # Join words back with spaces
    return ' '.join(wrapped_words)

class StoreDependencies:
    def __init__(self,globalScope):
        self.globalScope = globalScope
        self.getImportedModules()
        self.setImportsAsClassAttributes()
        
    def getImportedModules(self):    
        # Finds imported modules where this class is instantiated
        self.imported_modules = {name: obj for name, obj in self.globalScope.items() if not name.startswith("__")}
    
    def setImportsAsClassAttributes(self):
        for name, obj in self.imported_modules.items():
            setattr(self, name, obj)

def setupLogging(dep, app_name="MyApp"):
    """
    Sets up logging to a file in the folder the script or executable is being called from,
    and also prints to terminal if available.
    """
    # Get base_dir based on caller's location, not where getBaseDir lives
    caller_file = dep.sys._getframe(1).f_globals.get("__file__", "")
    if caller_file:
        base_dir = dep.os.path.dirname(dep.os.path.abspath(caller_file))
    else:
        base_dir = dep.os.getcwd()

    log_path = dep.os.path.join(base_dir, f"{app_name}_log.txt")

    # File handler with timestamped entries
    file_handler = dep.logging.FileHandler(log_path)
    file_handler.setFormatter(dep.logging.Formatter(
        "%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S"))

    # Console handler (for terminals, VS Code, etc.)
    console_handler = dep.logging.StreamHandler(dep.sys.stdout)
    console_handler.setFormatter(dep.logging.Formatter("%(message)s"))

    dep.logging.basicConfig(
        level=dep.logging.INFO,
        handlers=[file_handler, console_handler]
    )

    dep.logging.info(f"{app_name} started")

class PortListener:
    def __init__(self, dep, fileWithPortNumber, fileWithPortNumberToAvoid):
        # Parameters
        self.portNum = None
        self.portNumFileName = fileWithPortNumber
        self.portNumFileNameToAvoid = fileWithPortNumberToAvoid
        self.dep = dep
        # Default variables
        self.responseReceived = False

    def listenIndefinitely(self, functionToCallWhenResponseReceived):
        self.closeSocket()   
        self.portNum = self.findOpenPort()
        self.savePortNumberToFile(self.portNum)
        self.portListener()
        if self.portNum is not None:
            try:
                while True:
                    conn, addr = self.socket.accept()
                    data = conn.recv(1024)
                    if data:
                        functionToCallWhenResponseReceived()
                    conn.close()
            except OSError:
                pass 
        
    def listenForCertainTime(self, timeout=5):
        self.closeSocket()   
        self.portNum = self.findOpenPort()
        self.savePortNumberToFile(self.portNum)
        self.portListener()
        # Check for message for certain time
        self.socket.settimeout(timeout)
        try:
            conn, addr = self.socket.accept()  # Blocks until ping received or timeout
            data = conn.recv(1024)
            if data:
                self.responseReceived = True
            else:
                self.responseReceived = False
            conn.close()
        except self.dep.socket.timeout:
            self.responseReceived = False
        finally:
            self.socket.close()

    def closeSocket(self):
        self.portNum = None
        if hasattr(self, 'socket'):
            try:
                self.socket.close()
            except OSError:
                pass  # Socket was already closed

    def findOpenPort(self, startingPort=5000, maxTries=5000):
        # First read self.portNumFileNameToAvoid's port number to avoid it
        portToAvoid = readPortNumber(self.dep, self.portNumFileNameToAvoid)
        # Then get an open port
        for port in range(startingPort, startingPort + maxTries):
            # Skip if this is the Controller's port
            if port == portToAvoid:
                continue
            with self.dep.socket.socket(self.dep.socket.AF_INET, self.dep.socket.SOCK_STREAM) as s:
                try:
                    s.bind(("127.0.0.1", port))
                    return port
                except OSError:
                    continue              

    def savePortNumberToFile(self, portNum):
        # Get path to text file in accessoryFiles folder to save port number
        root_dir, _ = getBaseDir(self.dep.sys, self.dep.os)
        accessoryFiles_dir = self.dep.os.path.join(root_dir, 'accessoryFiles')
        curFilePath = self.dep.os.path.join(accessoryFiles_dir, self.portNumFileName)
        with open(curFilePath, "w") as f:
            f.write(str(portNum))     

    def portListener(self):
        if self.portNum is not None:
            print(f"Listening on port {self.portNum}")
            self.socket = self.dep.socket.socket(self.dep.socket.AF_INET, self.dep.socket.SOCK_STREAM)
            self.socket.bind(('127.0.0.1', self.portNum))
            self.socket.listen(1)
            print(f"Listening on port {self.portNum}")
        else:
            print('Port number not found')

    def clearPortNumber(self):
        root_dir, _ = getBaseDir(self.dep.sys, self.dep.os)
        accessoryFiles_dir = self.dep.os.path.join(root_dir, 'accessoryFiles')
        curFilePath = self.dep.os.path.join(accessoryFiles_dir, self.portNumFileName)
        with open(curFilePath, "w") as f:
            f.write('')     

class PortSender:
    def __init__(self, dep, fileWithPortNumToSendPings):
        # Parameters
        self.messageSent = False  
        self.fileWithPortNumToSendPings = fileWithPortNumToSendPings     
        self.dep = dep
        # Constructor methods    

    def sendPing(self, delay=0):
        self.portNum = readPortNumber(self.dep, self.fileWithPortNumToSendPings)
        if self.portNum is None:
            return
        
        self.socket = self.dep.socket.socket(self.dep.socket.AF_INET, self.dep.socket.SOCK_STREAM)
        try:    
            # print("Trying to send ping...")
            self.socket.connect(('127.0.0.1', self.portNum))
            self.dep.time.sleep(delay)
            self.socket.sendall(b'ping')
            self.messageSent = True
            # print("Message sent!")
        except Exception:
            pass
        finally:
            self.socket.close()

def readPortNumber(dep, fileWithPortNumToSendPings):
    # Get path to text file in accessoryFiles folder to save port number
    root_dir, _ = getBaseDir(dep.sys, dep.os)
    accessoryFiles_dir = dep.os.path.join(root_dir, 'accessoryFiles')
    curFilePath = dep.os.path.join(accessoryFiles_dir, fileWithPortNumToSendPings)
    # Return if file does not exist
    if not dep.os.path.exists(curFilePath):
        return None
    # Read port number from file
    with open(curFilePath, "r") as f:
        content = f.read().strip()
    try:
        port = int(content)
        if 1024 <= port <= 65535:  # Valid port range
            return port
    except (ValueError, OSError):
        return None
