import subprocess

# Cache the dark mode result per GUI session
_dark_mode_cache = None

def checkForDarkMode():
    global _dark_mode_cache
    if _dark_mode_cache is None:
        try:
            result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], 
                                  capture_output=True, text=True)
            _dark_mode_cache = result.stdout.strip() == "Dark"
        except:
            _dark_mode_cache = False
    return _dark_mode_cache

# 
def checkForDarkMode_reset():
    """Reset the theme cache - call this when opening a new GUI"""
    global _dark_mode_cache
    _dark_mode_cache = None

def buttonStyle(padding):
    if checkForDarkMode():
        return f"""
            QPushButton {{ 
                text-align: center;
                padding: {padding}px;
                margin: 0px;
                border: 2px solid #666666;
                background-color: #3d3d3d;
                color: #ffffff;
                border-radius: 10px;
            }}
            QPushButton:hover {{ 
                background-color: #4d4d4d;
                border: 2px solid #888888;
            }}
            QPushButton:pressed {{
                background-color: #5d5d5d;
                border: 2px solid #aaaaaa;
            }}
        """
    else:
        return f"""
            QPushButton {{ 
                text-align: center;
                padding: {padding}px;
                margin: 0px;
                border: 2px solid #b0b0b0;
                background-color: #ffffff;
                color: #000000;
                border-radius: 10px;
            }}
            QPushButton:hover {{ 
                background-color: #f5f5f5;
                border: 2px solid #808080;
            }}
            QPushButton:pressed {{
                background-color: #e6e6e6;
                border: 2px solid #606060;
            }}
        """

def textStyle():
    if checkForDarkMode():
        return "QLabel { color: #ffffff; }"
    else:
        return "QLabel { color: #000000; }"

def toggleStyle(toggleWidth):
    if checkForDarkMode():
        return f"""
            QCheckBox::indicator {{
                width: {toggleWidth}px;
                height: {toggleWidth}px;
                background-color: #5d5d5d;
                border: 0px solid #666666;
                border-radius: {toggleWidth/10}px;
            }}
            QCheckBox::indicator:checked {{
                background-color: #4CAF50;
            }}
            QCheckBox::indicator:hover {{
                border: 3px solid #888888;
            }}
        """
    else:
        return f"""
            QCheckBox::indicator {{
                width: {toggleWidth}px;
                height: {toggleWidth}px;
                background-color: white;
                border: 0px solid #b0b0b0;
                border-radius: {toggleWidth/10}px;
            }}
            QCheckBox::indicator:checked {{
                background-color: #4CAF50;
            }}
            QCheckBox::indicator:hover {{
                border: 3px solid #808080;
            }}
        """