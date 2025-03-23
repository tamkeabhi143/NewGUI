#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run script for the Signal Manager application
"""

import sys
import os
from App.signal_manager_app import SignalManagerApp
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

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
    
    # Create and show the main window
    main_window = SignalManagerApp()
    main_window.show()
    
    # Run the application event loop
    sys.exit(app.exec_()) 