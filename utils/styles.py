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