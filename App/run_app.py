#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Signal Manager Run Script
"""

import sys
import os
import argparse

def main():
    """Main application entry point"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Signal Manager')
    parser.add_argument('--demo', action='store_true', help='Run dialog integration demo')
    parser.add_argument('--core-config', action='store_true', help='Run Core Configuration Manager')
    args = parser.parse_args()
    
    # Import PyQt5 here to avoid the need for the module when just checking version
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
    from PyQt5.QtCore import Qt
    from PyQt5 import uic
    
    # Enable High DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a consistent look across platforms
    
    # Set application properties
    app.setApplicationName("Signal Manager")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Your Organization")
    app.setOrganizationDomain("yourorganization.com")
    
    # Add resource directories to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    resources_dir = os.path.join(parent_dir, "Cfg", "Resources")
    dialogs_dir = os.path.join(parent_dir, "Cfg", "LayoutFiles", "Dialogs")
    
    # Load and apply stylesheet if available
    style_path = os.path.join(resources_dir, "styles", "dark_theme.qss")
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: Dark theme stylesheet not found at {style_path}")
    
    # Determine which UI to show
    if args.demo:
        # Run dialog integration demo
        dialog_integration_ui = os.path.join(dialogs_dir, "DialogIntegration.ui")
        main_window = QWidget()
        uic.loadUi(dialog_integration_ui, main_window)
        
        # Set the window title
        main_window.setWindowTitle("Signal Manager - Dialog Integration Demo")
        
    elif args.core_config:
        # Run Core Configuration Manager
        core_config_ui = os.path.join(dialogs_dir, "CoreConfigManager.ui")
        main_window = QMainWindow()
        
        # Set window properties
        main_window.setWindowTitle("Signal Manager - Core Configuration")
        main_window.setMinimumSize(900, 650)
        
        # Load the UI into a central widget
        core_config = QWidget()
        uic.loadUi(core_config_ui, core_config)
        main_window.setCentralWidget(core_config)
        
    else:
        # Run main Signal Manager application
        signal_manager_ui = os.path.join(parent_dir, "Cfg", "LayoutFiles", "signal_manager_app.ui")
        main_window = QMainWindow()
        uic.loadUi(signal_manager_ui, main_window)
        
        # Connect navigation buttons to switch between pages
        content_stack = main_window.findChild(QWidget, "content_stack")
        nav_button0 = main_window.findChild(QWidget, "navButton0")
        nav_button1 = main_window.findChild(QWidget, "navButton1")
        nav_button2 = main_window.findChild(QWidget, "navButton2")
        
        # Connect navigation buttons to switch pages
        if content_stack and nav_button0 and nav_button1 and nav_button2:
            nav_button0.clicked.connect(lambda: content_stack.setCurrentIndex(0))
            nav_button1.clicked.connect(lambda: content_stack.setCurrentIndex(1))
            nav_button2.clicked.connect(lambda: content_stack.setCurrentIndex(2))
            
            # Ensure button states update correctly when clicked
            nav_button0.clicked.connect(lambda: nav_button0.setChecked(True))
            nav_button0.clicked.connect(lambda: nav_button1.setChecked(False))
            nav_button0.clicked.connect(lambda: nav_button2.setChecked(False))
            
            nav_button1.clicked.connect(lambda: nav_button0.setChecked(False))
            nav_button1.clicked.connect(lambda: nav_button1.setChecked(True))
            nav_button1.clicked.connect(lambda: nav_button2.setChecked(False))
            
            nav_button2.clicked.connect(lambda: nav_button0.setChecked(False))
            nav_button2.clicked.connect(lambda: nav_button1.setChecked(False))
            nav_button2.clicked.connect(lambda: nav_button2.setChecked(True))
    
    # Show the window
    main_window.show()
    
    # Run the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()