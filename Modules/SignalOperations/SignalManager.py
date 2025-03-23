#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SignalManager module for handling signal operations
"""

import os
import json
import uuid
from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem, QFormLayout, QLabel, 
                           QLineEdit, QMessageBox, QVBoxLayout, QWidget, QComboBox)
from PyQt5.QtCore import Qt

class SignalManager:
    """Class for managing signal operations"""
    
    def __init__(self, parent=None):
        """Initialize the SignalManager
        
        Args:
            parent: The parent widget (usually the main application)
        """
        self.parent = parent
        self.project_data = {}
        self.current_signal = None
        self.current_signal_id = None
        
    def set_project_data(self, project_data):
        """Set the project data
        
        Args:
            project_data: The project data dictionary
        """
        self.project_data = project_data
        
    def find_signal_by_id(self, signal_id):
        """Find a signal by its ID
        
        Args:
            signal_id: The ID of the signal to find
            
        Returns:
            dict: The signal data dictionary, or None if not found
        """
        if not self.project_data or "signals" not in self.project_data:
            return None
            
        for signal in self.project_data["signals"]:
            if signal.get("id") == signal_id:
                return signal
                
        return None
    
    def generate_signal_id(self):
        """Generate a unique signal ID
        
        Returns:
            str: A unique signal ID
        """
        # Start with a simple UUID4-based ID
        new_id = str(uuid.uuid4())[:8]
        
        # Check if this ID already exists in the project
        if "signals" in self.project_data:
            existing_ids = [signal.get("id") for signal in self.project_data["signals"] if "id" in signal]
            while new_id in existing_ids:
                new_id = str(uuid.uuid4())[:8]
                
        return new_id
    
    def add_signal_to_database(self, signal_data):
        """Add a signal to the database
        
        Args:
            signal_data: The signal data dictionary
            
        Returns:
            str: The ID of the added signal
        """
        # If signals key doesn't exist, create it
        if "signals" not in self.project_data:
            self.project_data["signals"] = []
            
        # Generate a unique ID if not provided
        if "id" not in signal_data or not signal_data["id"]:
            signal_data["id"] = self.generate_signal_id()
            
        # Add to signals list
        self.project_data["signals"].append(signal_data)
        
        # Mark project as modified
        if self.parent and hasattr(self.parent, "set_project_modified"):
            self.parent.set_project_modified(True)
            
        return signal_data["id"]
    
    def update_signal_in_database(self, signal_id, updated_data):
        """Update a signal in the database
        
        Args:
            signal_id: The ID of the signal to update
            updated_data: The updated signal data
            
        Returns:
            bool: True if the signal was updated, False otherwise
        """
        if not self.project_data or "signals" not in self.project_data:
            return False
            
        # Find the signal by ID
        for i, signal in enumerate(self.project_data["signals"]):
            if signal.get("id") == signal_id:
                # Ensure the ID is preserved
                updated_data["id"] = signal_id
                # Update the signal
                self.project_data["signals"][i] = updated_data
                
                # Mark project as modified
                if self.parent and hasattr(self.parent, "set_project_modified"):
                    self.parent.set_project_modified(True)
                    
                return True
                
        return False
    
    def delete_signal_from_database(self, signal_id):
        """Delete a signal from the database
        
        Args:
            signal_id: The ID of the signal to delete
            
        Returns:
            bool: True if the signal was deleted, False otherwise
        """
        if not self.project_data or "signals" not in self.project_data:
            return False
            
        # Find the signal by ID
        for i, signal in enumerate(self.project_data["signals"]):
            if signal.get("id") == signal_id:
                # Save the current state for potential undo
                signal_data = signal.copy()
                
                # Remove the signal
                del self.project_data["signals"][i]
                
                # Mark project as modified
                if self.parent and hasattr(self.parent, "set_project_modified"):
                    self.parent.set_project_modified(True)
                    
                return True
                
        return False
    
    def update_signal_tree(self, tree_widget):
        """Update the signal tree with current data
        
        Args:
            tree_widget: The QTreeWidget to update
        """
        # Clear the tree
        tree_widget.clear()
        
        # If no signals, return
        if not self.project_data or "signals" not in self.project_data:
            return
            
        # Add signals to the tree
        for signal in self.project_data["signals"]:
            # Create a tree item for the signal
            item = QTreeWidgetItem(tree_widget)
            
            # Set signal name in first column
            item.setText(0, signal.get("name", "Unknown"))
            
            # Set additional info in other columns if desired
            item.setText(1, signal.get("data_type", ""))
            
            # Store the signal ID in the item's data
            item.setData(0, Qt.UserRole, signal.get("id"))
    
    def populate_signal_details(self, parent, signal_data, form_layout=None):
        """Populate signal details in a form layout
        
        Args:
            parent: The parent widget
            signal_data: The signal data dictionary
            form_layout: Optional form layout to populate
            
        Returns:
            QFormLayout: The populated form layout
        """
        # If no form layout provided, create one
        if not form_layout:
            form_layout = QFormLayout()
            
        # Clear the existing layout
        while form_layout.count() > 0:
            item = form_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Add signal details to the form
        for key, value in signal_data.items():
            # Skip internal fields like ID
            if key in ["id", "struct_fields"]:
                continue
                
            # Create a label and value widget
            label = QLabel(f"{key.replace('_', ' ').title()}:")
            
            # For different types of values, create appropriate widgets
            if isinstance(value, bool):
                value_widget = QLabel("Yes" if value else "No")
            elif isinstance(value, (list, dict)):
                value_widget = QLabel(str(value))
            else:
                value_widget = QLabel(str(value))
                
            # Add to the form layout
            form_layout.addRow(label, value_widget)
            
        # Handle struct fields separately if present
        if "struct_fields" in signal_data and signal_data.get("data_type") == "STRUCT":
            # Create a container for struct fields
            struct_container = QWidget()
            struct_layout = QVBoxLayout(struct_container)
            
            # Add a header
            struct_layout.addWidget(QLabel("<b>Struct Fields:</b>"))
            
            # Create a sub-form for each field
            for field in signal_data["struct_fields"]:
                field_form = QFormLayout()
                
                # Add field details
                for key, value in field.items():
                    label = QLabel(f"{key.replace('_', ' ').title()}:")
                    value_widget = QLabel(str(value))
                    field_form.addRow(label, value_widget)
                    
                # Add a separator
                struct_layout.addLayout(field_form)
                struct_layout.addWidget(QLabel("----------"))
                
            # Add the struct container to the main form
            form_layout.addRow(QLabel(""), struct_container)
            
        return form_layout
    
    def collect_signal_form_data(self, parent):
        """Collect data from a signal form
        
        Args:
            parent: The parent widget containing the form elements
            
        Returns:
            dict: The collected signal data
        """
        result = {}
        
        # Get basic signal properties
        name_edit = parent.findChild(QLineEdit, "signal_name_edit")
        if name_edit:
            result["name"] = name_edit.text()
            
        # Get other signal properties based on your form structure
        data_type_combo = parent.findChild(QComboBox, "data_type_combo")
        if data_type_combo:
            result["data_type"] = data_type_combo.currentText()
            
        # Add more fields based on your form structure
        
        return result
    
    def validate_signal_data(self, signal_data):
        """Validate signal data
        
        Args:
            signal_data: The signal data to validate
            
        Returns:
            tuple: (bool, str) - (is_valid, error_message)
        """
        # Check for required fields
        if "name" not in signal_data or not signal_data["name"]:
            return False, "Signal name is required"
            
        if "data_type" not in signal_data or not signal_data["data_type"]:
            return False, "Data type is required"
            
        # Check for duplicate names
        if "signals" in self.project_data:
            for signal in self.project_data["signals"]:
                if (signal.get("name") == signal_data["name"] and 
                    (signal.get("id") != signal_data.get("id"))):
                    return False, f"Signal with name '{signal_data['name']}' already exists"
                    
        # Add more validation rules as needed
        
        return True, "" 