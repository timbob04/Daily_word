class makeMenuIcon():
    def __init__(self, dep, app, controller):
        self.dep = dep
        self.app = app
        self.controller = controller
        # Constructor methods
        self.getIconPaths()
        self.createTrayIcon()
        self.makeTrayActions()
        self.storeTrayIcon()

    def getIconPaths(self):
        # Get icon for the mac's toolbar
        root_dir, _ = self.dep.getBaseDir(self.dep.sys, self.dep.os)
        dir_accessoryFiles = self.dep.os.path.join(root_dir, 'accessoryFiles')
        self.icon_path = self.dep.os.path.join(dir_accessoryFiles, 'iconTemplate.png')
        self.icon_path_active = self.dep.os.path.join(dir_accessoryFiles, 'iconTemplate_dot.png')

    def createTrayIcon(self):    
        # Create the system tray icon
        self.tray = self.dep.QSystemTrayIcon(self.dep.QIcon(self.icon_path), parent=self.app)
        self.tray.setToolTip("Daily Word Definition")
        # Define action on icon click
        self.tray.activated.connect(self.defineActionOnIconClick)
        # Create the menu
        self.menu = self.dep.QMenu()

    def makeTrayActions(self):  
        # Add the Edit time action
        edit_time_action = self.dep.QAction("Edit time", self.menu)
        edit_time_action.triggered.connect(self.controller.workers['editTime'].start)
        self.menu.addAction(edit_time_action)  
        # Add a separator
        self.menu.addSeparator()

        # Add the Edit word list action
        edit_word_list_action = self.dep.QAction("Edit word list", self.menu)
        edit_word_list_action.triggered.connect(self.controller.workers['editWordList'].start)
        self.menu.addAction(edit_word_list_action)
        # Add separator
        self.menu.addSeparator()

        # Add the Quit action
        quit_action = self.dep.QAction("Quit", self.menu)
        quit_action.triggered.connect(self.controller.userInitiatedQuit)
        self.menu.addAction(quit_action)
                
        # Set the menu as the tray icon's context menu
        self.tray.setContextMenu(self.menu)
        # Make sure the icon is visible
        self.tray.show()

    def defineActionOnIconClick(self, reason):
        if reason == self.dep.QSystemTrayIcon.Trigger: # when the icon is clicked
            wins = [w for w in self.app.topLevelWidgets() if w.isVisible()] # get all visible windows

            # Sort the windows from largest to smallest so larger ones end up behind
            wins.sort(key=lambda w: w.width() * w.height(),reverse=True)
            
            # Raise the windows from largest to smallest so larger ones end up behind
            for w in wins:
                w.raise_()
                w.activateWindow()

    def storeTrayIcon(self):
        # Store the tray icon in the app for later reference
        self.app.icon = self

    def changeIconToActiveState(self):
        self.app.icon.tray.setIcon(self.dep.QIcon(self.icon_path_active))

    def changeIconToInactiveState(self):
        print("Changing icon to inactive state")
        self.app.icon.tray.setIcon(self.dep.QIcon(self.icon_path))