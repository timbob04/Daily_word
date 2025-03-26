def buttonStyle(padding):
    return """
        QPushButton { 
            text-align: center;
            padding: %dpx;
            margin: 0px;
            border: 2px solid #b0b0b0;
            background-color: #ffffff;
            border-radius: 10px;
        }
        QPushButton:hover { 
            background-color: #f5f5f5;
            border: 2px solid #808080;
        }
        QPushButton:pressed {
            background-color: #e6e6e6;
            border: 2px solid #606060;
        }
    """ % padding 

def toggleStyle(toggleWidth):
    return (f"""
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
        """)