#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run script for the Signal Manager application
"""

import sys
import os

# Set up paths properly to find all modules
app_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(os.path.dirname(app_dir))  # Go up two levels

ProjectPath = os.path.abspath(os.path.join(app_dir, ".."))  # Project root path

# Add base directory to Python path
sys.path.append(ProjectPath)

# Add the NewGUI directory to Python path
newgui_dir = os.path.dirname(app_dir)
sys.path.append(newgui_dir)

# Add the App directory to Python path
sys.path.append(app_dir)

# Now import the modules after setting the path
from signal_manager_app import SignalManagerApp
from Modules.Dialogs.LoginDialog import LoginDialog
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from icecream import ic

# Import resource file to initialize resources
import Cfg.Resources.resources_rc

if __name__ == "__main__":
    # Enable High DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName("Signal Manager")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Your Organization")
    app.setOrganizationDomain("yourorganization.com")
    
    # Initialize UserManager with application directory
    userCredentials = os.path.join(ProjectPath, "Cfg", "Credentials")
    ic(ProjectPath)
    from Modules.Dialogs.UserManager import UserManager
    user_manager = UserManager(ProjectPath)
    
    # check the argument for --no-login and depend on that show login menu
    if len(sys.argv) > 1 and sys.argv[1] == "--no-login":
        # Skip login dialog if --no-login argument is provided
        login_success = True
        username = "Admin"
    else:
        # Show login dialog
        login_success, username = LoginDialog.login()
    
    # Only proceed if login was successful
    if login_success:
        # Create the main window
        main_window = SignalManagerApp()
        
        # Set resource paths - use the correct paths matching the project structure
        MainAppIconsPath = os.path.join(ProjectPath, "Cfg", "Resources", "icons")
        ToolbarIconsPath = os.path.join(ProjectPath, "Cfg", "Resources", "icons")
        
        # Pass icon paths to the main window if it has a method to set them
        if hasattr(main_window, 'set_icon_paths'):
            main_window.set_icon_paths(MainAppIconsPath, ToolbarIconsPath)
        
        # Set the application icon
        app_icon_path = os.path.join(MainAppIconsPath, "AppIcon.png")
        if os.path.exists(app_icon_path):
            main_window.setWindowIcon(QIcon(app_icon_path))
        
        # Set the logged-in username
        main_window.set_username(username)
        
        # Show the main window
        main_window.show()
        
        # Run the application event loop
        sys.exit(app.exec_())
    else:
        # Exit if login failed or was cancelled
        sys.exit(0)