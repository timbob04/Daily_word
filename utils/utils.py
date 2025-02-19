
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
    
class storeDependencies:
    def __init__(self, *args):
        for idx, value in enumerate(args):            
            attr_name = getattr(value, "__name__", f"arg_{idx}")
            setattr(self, attr_name, value)    