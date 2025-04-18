#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Signal Manager - Main Application
A modern PyQt5-based application for signal data management with dark theme
"""

import sys
import os

# Add the parent directory to Python path so we can import Modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QFile, QTextStream, Qt
from PyQt5 import uic

# Import the compiled resources module
import Cfg.Resources.resources_rc

def load_stylesheet(resource_path):
    """Load the stylesheet from the given resource path"""
    try:
        stylesheet_file = QFile(resource_path)
        if (stylesheet_file.open(QFile.ReadOnly | QFile.Text)):
            stream = QTextStream(stylesheet_file)
            stylesheet = stream.readAll()
            return stylesheet
        else:
            print(f"Could not open stylesheet file: {resource_path}")
    except Exception as e:
        print(f"Error loading stylesheet: {str(e)}")
    return ""

def main():
    """Main application entry point"""
    # Enable High DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName("Signal Manager")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Your Organization")
    app.setOrganizationDomain("yourorganization.com")
    
    # Load and apply the dark theme stylesheet
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    style_path = os.path.join(base_dir, 'Cfg', 'Resources', 'styles', 'dark_theme.qss')
    
    if os.path.exists(style_path):
        with open(style_path, 'r') as f:
            stylesheet = f.read()
            app.setStyleSheet(stylesheet)
    else:
        print(f"Warning: Stylesheet file not found at {style_path}")
    
    # Create and show the main window by loading the UI file directly
    main_window = QMainWindow()
    ui_path = os.path.join(base_dir, 'Cfg', 'LayoutFiles', 'signal_manager_app.ui')
    try:
        uic.loadUi(ui_path, main_window)
        
        # Get the stacked widget and its pages
        stack_widget = main_window.findChild(QWidget, "content_stack")
        
        # Connect navigation buttons
        nav_button0 = main_window.findChild(QWidget, "navButton0")
        nav_button1 = main_window.findChild(QWidget, "navButton1")
        nav_button2 = main_window.findChild(QWidget, "navButton2")
        
        # Connect signals to switch stacked widget pages
        nav_button0.clicked.connect(lambda: stack_widget.setCurrentIndex(0))
        nav_button1.clicked.connect(lambda: stack_widget.setCurrentIndex(1))
        nav_button2.clicked.connect(lambda: stack_widget.setCurrentIndex(2))
        
    except Exception as e:
        print(f"Error loading UI file: {str(e)}")
        return 1
    
    main_window.show()
    
    # Run the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()