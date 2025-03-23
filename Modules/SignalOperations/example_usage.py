#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example of how to use the SignalManager class in the signal_manager_app.py file
"""

# This is just an example and not meant to be executed directly

# Original imports in signal_manager_app.py
import os
import json
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QStackedWidget, QFrame, 
                           QSplitter, QLineEdit, QComboBox, QFormLayout)
from PyQt5.QtCore import Qt, QSize, QDateTime, QSettings

# Add import for SignalManager
from Modules.SignalOperations.SignalManager import SignalManager

# Other imports from original file
from Modules.FileOperation.FileOperations import FileOperations
from Modules.MenuOperation.menu_operations import MenuOperations
from Modules.Dialogs.SignalDialogs.SignalDetailsDialog import SignalDetailsDialog
from Modules.Dialogs.CoreConfigurationManager.CoreConfig import CoreConfigManager


class SignalManagerApp(QMainWindow):
    """Main application window for Signal Manager with SignalManager integration"""
    
    def __init__(self, parent=None):
        """Initialize the main window"""
        super(SignalManagerApp, self).__init__(parent)
        
        # Initialize properties
        self.current_project_name = "Untitled"
        self.current_file_path = ""
        self.has_unsaved_changes = False
        self.project_data = {}
        self.recent_files = []
        self.max_recent_files = 5
        self.current_file = None
        self.username = "Guest"  # Default username
        
        # Create SignalManager instance
        self.signal_manager = SignalManager(self)
        
        # Load UI from file
        self.setup_ui()
        
        # Set project data in the signal manager
        self.signal_manager.set_project_data(self.project_data)
        
        # Rest of initialization...
    
    # Modified methods that use SignalManager
    
    def find_signal_by_id(self, signal_id):
        """Find a signal by its ID using SignalManager"""
        return self.signal_manager.find_signal_by_id(signal_id)
    
    def generate_signal_id(self):
        """Generate a unique signal ID using SignalManager"""
        return self.signal_manager.generate_signal_id()
    
    def add_signal_to_database(self, signal_data):
        """Add a signal to the database using SignalManager"""
        return self.signal_manager.add_signal_to_database(signal_data)
    
    def update_signal_in_database(self, signal_id, updated_data):
        """Update a signal in the database using SignalManager"""
        return self.signal_manager.update_signal_in_database(signal_id, updated_data)
    
    def delete_signal_from_database(self, signal_id):
        """Delete a signal from the database using SignalManager"""
        return self.signal_manager.delete_signal_from_database(signal_id)
    
    def update_signal_tree(self):
        """Update the signal tree using SignalManager"""
        # Assuming the tree widget is named signal_tree_widget
        tree_widget = self.findChild(QTreeWidget, "signal_tree_widget")
        if tree_widget:
            self.signal_manager.update_signal_tree(tree_widget)
    
    def populate_signal_details(self, signal_data):
        """Populate signal details using SignalManager"""
        # Assuming the form layout is named signal_details_layout
        form_layout = self.findChild(QFormLayout, "signal_details_layout")
        if form_layout:
            self.signal_manager.populate_signal_details(self, signal_data, form_layout)
    
    def collect_signal_form_data(self):
        """Collect signal form data using SignalManager"""
        return self.signal_manager.collect_signal_form_data(self)
    
    def validate_signal_data(self, signal_data):
        """Validate signal data using SignalManager"""
        return self.signal_manager.validate_signal_data(signal_data)
    
    def load_project(self, file_path):
        """Load a project and update SignalManager"""
        # Load project data
        try:
            with open(file_path, 'r') as f:
                self.project_data = json.load(f)
            
            # Set project data in the signal manager
            self.signal_manager.set_project_data(self.project_data)
            
            # Update UI with project data
            self.update_ui_from_data()
            
            # Update file path and project name
            self.current_file_path = file_path
            self.current_project_name = os.path.basename(file_path)
            
            # Update window title
            self.update_window_title()
            
            # Add to recent files
            self.add_recent_file(file_path)
            
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load project: {str(e)}")
            return False 