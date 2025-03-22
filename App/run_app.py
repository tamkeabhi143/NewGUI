#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Signal Manager Application Launcher
Runs the main Signal Manager application
"""
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from pathlib import Path
import argparse

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="Signal Manager Application")
    parser.add_argument("--demo", action="store_true", help="Run the dialog integration demo")
    parser.add_argument("--core-config", action="store_true", help="Run the Core Configuration Manager")
    
    args = parser.parse_args()
    
    # Add the project root directory to sys.path
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Import required modules
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
    except ImportError:
        print("Error: PyQt5 is not installed. Please install it with:")
        print("pip install PyQt5")
        sys.exit(1)
    
    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName("Signal Manager")
    app.setApplicationVersion("1.0.0")
    
    # Enable High DPI scaling
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Load and apply stylesheet
    style_path = os.path.join(project_root,"..\\", "Cfg", "Resources", "styles", "dark_theme.qss")
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: Style file not found at {style_path}")
    
    # Determine which UI to show
    if args.demo:
        # Run dialog integration demo
        from Cfg.Dialogs.dialog_integration import DialogIntegrationDemo
        main_window = DialogIntegrationDemo()
    elif args.core_config:
        # Run Core Configuration Manager
        from PyQt5.QtWidgets import QMainWindow
        from Cfg.Dialogs.core_config_manager import CoreConfigManager
        
        main_window = QMainWindow()
        main_window.setWindowTitle("Core Configuration Manager")
        main_window.resize(900, 650)
        
        core_config = CoreConfigManager()
        main_window.setCentralWidget(core_config)
    else:
        # Run main Signal Manager application
        from Cfg.Dialogs.signal_manager_app import SignalManagerApp
        main_window = SignalManagerApp()
    
    # Show the window
    main_window.show()
    
    # Run the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()