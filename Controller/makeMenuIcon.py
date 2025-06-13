def makeMenuIcon(dep, app, controller):
    
    # Get icon for the mac's toolbar
    root_dir, _ = dep.getBaseDir(dep.sys, dep.os)
    dir_accessoryFiles = dep.os.path.join(root_dir, 'accessoryFiles')
    icon_path = dep.os.path.join(dir_accessoryFiles, 'iconTemplate.png')

    # Create the system tray icon
    tray = dep.QSystemTrayIcon(dep.QIcon(icon_path), parent=app)
    tray.setToolTip("Daily Word Definition")
    
    # Create the menu
    menu = dep.QMenu()
    
    # Add the Quit action
    quit_action = dep.QAction("Quit", menu)
    quit_action.triggered.connect(controller.userInitiatedQuit)
    menu.addAction(quit_action)

    # Add a separator
    menu.addSeparator()

    # Add the Edit word list action
    edit_word_list_action = dep.QAction("Edit word list", menu)
    edit_word_list_action.triggered.connect(controller.workers['editWordList'].start)
    menu.addAction(edit_word_list_action)

    # Add separator
    menu.addSeparator()

    # Add action to bring all windows to front
    bring_all_to_front_action = dep.QAction("Bring all windows to front", menu)
    bring_all_to_front_action.triggered.connect(lambda: [window.raise_() for window in app.topLevelWidgets() if window.isVisible()])
    menu.addAction(bring_all_to_front_action)

    # Add separator
    menu.addSeparator()

    # Add the Edit time action
    edit_time_action = dep.QAction("Edit time", menu)
    edit_time_action.triggered.connect(controller.workers['editTime'].start)
    menu.addAction(edit_time_action)
    
    # Set the menu as the tray icon's context menu
    tray.setContextMenu(menu)
    
    # Make sure the icon is visible
    tray.show()
    
    # Store the tray icon in the app for later reference
    app.tray = tray