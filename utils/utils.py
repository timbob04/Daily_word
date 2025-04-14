def getBaseDir(sys, os):
    # Check if the program is running as an executable
    if getattr(sys, 'frozen', False):                
        return os.path.dirname(sys.executable)
    
    # If not, find where this python function is being called from, not where this function actually is
    caller_file = sys._getframe(1).f_globals.get("__file__", "")
    if caller_file:  
        return os.path.dirname(os.path.abspath(caller_file))  # Use the caller script's location
    else:
        return os.getcwd()  # Default to current working directory if __file__ is missing
    
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