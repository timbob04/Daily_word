def getBaseDir(sys,os):
    # Check if the program is running as an executable
    if getattr(sys, 'frozen', False):                
        return os.path.dirname(sys.executable)
    
    # If not, find where this python function is being called from, not where this function actually is
    caller_file = sys._getframe(1).f_globals.get("__file__", "")
    if caller_file:  
        return os.path.dirname(os.path.abspath(caller_file))  # Use the caller script's location
    else:
        return os.getcwd()  # Default to current working directory if __file__ is missing
    

def readJSONfile(json,filepath):
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

class StoreDependencies():
    def __init__(self,inspect,os):
        self.inspect = inspect
        self.os = inspect
        self.findFileNameAndLineNumber
    
    def findFileNameAndLineNumber(self):
        here = self.os.path.abspath(__file__)
        for frame in self.inspect.stack():
            if self.os.path.abspath(frame.filename) != here:
                self.callerFileName = frame.filename
                self.callerLineNumber = frame.lineno
                break
    
    def retrieveLinesOfCodeBeforeCall(self):          
        with open(self.callerFileName, 'r') as f:
            lines = f.readlines()
            self.lines = lines[:self.callerLineNumber - 1]
            
    # Get the words after instances of 'import', ignoring spaces and commas

    def __init__(self, *args):
        for idx, value in enumerate(args):            
            attr_name = getattr(value, "__name__", f"arg_{idx}")
            setattr(self, attr_name, value) 
