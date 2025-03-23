#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
StructFieldDialog module for editing struct fields
"""

import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLabel, 
                            QLineEdit, QComboBox, QRadioButton, QPushButton,
                            QDialogButtonBox, QMessageBox, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5 import uic

class StructFieldDialog(QDialog):
    """Dialog for editing struct fields"""
    
    def __init__(self, parent=None, field_data=None):
        """Initialize the dialog
        
        Args:
            parent: The parent widget
            field_data: Optional dictionary with field data to populate the form
        """
        super(StructFieldDialog, self).__init__(parent)
        
        # Set up member variables
        self.field_data = field_data or {}
        self.result_data = None
        
        # Load UI from file
        self.setup_ui()
        
        # Connect signals and slots
        self.connect_signals_slots()
        
        # Populate data if provided
        if field_data:
            self.populate_form(field_data)
    
    def setup_ui(self):
        """Set up the user interface"""
        # Load UI file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        module_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        ui_file_path = os.path.join(module_dir, "Cfg", "LayoutFiles", "Dialogs", "StructFieldDialog.ui")
        uic.loadUi(ui_file_path, self)
        
        # Initialize UI elements based on selections
        self.initialize_dynamic_ui()
    
    def initialize_dynamic_ui(self):
        """Initialize dynamic UI elements based on selections"""
        # Get references to radio buttons
        basic_radio = self.findChild(QRadioButton, "basic_radio")
        array_radio = self.findChild(QRadioButton, "array_radio")
        
        # Get array-specific widgets
        array_type_label = self.findChild(QLabel, "array_type_label")
        array_display = self.findChild(QLineEdit, "array_display")
        configure_array_button = self.findChild(QPushButton, "configure_array_button")
        
        # Set initial visibility
        if basic_radio and array_radio and array_type_label and array_display and configure_array_button:
            array_type_label.setVisible(array_radio.isChecked())
            array_display.setVisible(array_radio.isChecked())
            configure_array_button.setVisible(array_radio.isChecked())
    
    def connect_signals_slots(self):
        """Connect signals and slots for dialog interactions"""
        # Connect radio buttons
        basic_radio = self.findChild(QRadioButton, "basic_radio")
        array_radio = self.findChild(QRadioButton, "array_radio")
        
        if basic_radio and array_radio:
            basic_radio.toggled.connect(self.on_radio_toggled)
            array_radio.toggled.connect(self.on_radio_toggled)
        
        # Connect configure array button
        configure_array_button = self.findChild(QPushButton, "configure_array_button")
        if configure_array_button:
            configure_array_button.clicked.connect(self.on_configure_array)
        
        # Connect dialog buttons
        button_box = self.findChild(QDialogButtonBox, "buttonBox")
        if button_box:
            button_box.accepted.connect(self.on_ok)
            button_box.rejected.connect(self.reject)
    
    def on_radio_toggled(self, checked):
        """Handle radio button toggling
        
        Args:
            checked: Whether the radio button is checked
        """
        # Get the sender
        sender = self.sender()
        
        # Get array-specific widgets
        array_type_label = self.findChild(QLabel, "array_type_label")
        array_display = self.findChild(QLineEdit, "array_display")
        configure_array_button = self.findChild(QPushButton, "configure_array_button")
        
        # Set visibility based on radio button
        if sender.objectName() == "array_radio":
            if array_type_label and array_display and configure_array_button:
                array_type_label.setVisible(checked)
                array_display.setVisible(checked)
                configure_array_button.setVisible(checked)
    
    def on_configure_array(self):
        """Handle configure array button click"""
        # Create dialog for array configuration
        from .ArrayTypeDialog import ArrayTypeDialog
        
        # Get current array type and size
        array_display = self.findChild(QLineEdit, "array_display")
        current_text = array_display.text() if array_display else ""
        
        # Parse current text to get type and size
        current_size = 0
        current_type = ""
        
        if current_text:
            parts = current_text.split()
            if len(parts) >= 3 and parts[1] == "of":
                try:
                    current_size = int(parts[0])
                    current_type = parts[2]
                except (ValueError, IndexError):
                    pass
        
        # Show the array type dialog
        dialog = ArrayTypeDialog(self, current_type, current_size)
        if dialog.exec_() == QDialog.Accepted:
            # Update the array display
            if array_display:
                array_display.setText(f"{dialog.size_spin.value()} of {dialog.type_combo.currentText()}")
    
    def populate_form(self, field_data):
        """Populate the form with field data
        
        Args:
            field_data: Dictionary with field data to populate the form
        """
        # Get form fields
        name_edit = self.findChild(QLineEdit, "name_edit")
        description_edit = self.findChild(QLineEdit, "description_edit")
        basic_radio = self.findChild(QRadioButton, "basic_radio")
        array_radio = self.findChild(QRadioButton, "array_radio")
        type_combo = self.findChild(QComboBox, "type_combo")
        array_display = self.findChild(QLineEdit, "array_display")
        
        # Populate fields
        if name_edit and "field_name" in field_data:
            name_edit.setText(field_data["field_name"])
        
        if description_edit and "description" in field_data:
            description_edit.setText(field_data["description"])
        
        # Handle data type
        if basic_radio and array_radio and type_combo:
            if "data_type" in field_data:
                if field_data["data_type"] == "ARRAY":
                    array_radio.setChecked(True)
                    
                    # Populate array display
                    if array_display and "array_size" in field_data and "element_type" in field_data:
                        array_display.setText(f"{field_data['array_size']} of {field_data['element_type']}")
                else:
                    basic_radio.setChecked(True)
                    
                    # Set type combo
                    index = type_combo.findText(field_data["data_type"])
                    if index >= 0:
                        type_combo.setCurrentIndex(index)
    
    def collect_form_data(self):
        """Collect data from the form and return it as a dictionary
        
        Returns:
            dict: Dictionary with the collected form data
        """
        result = {}
        
        # Get form fields
        name_edit = self.findChild(QLineEdit, "name_edit")
        description_edit = self.findChild(QLineEdit, "description_edit")
        basic_radio = self.findChild(QRadioButton, "basic_radio")
        type_combo = self.findChild(QComboBox, "type_combo")
        array_display = self.findChild(QLineEdit, "array_display")
        
        # Collect field name
        if name_edit:
            result["field_name"] = name_edit.text().strip()
        
        # Collect description
        if description_edit:
            result["description"] = description_edit.text().strip()
        
        # Collect data type
        if basic_radio and type_combo:
            if basic_radio.isChecked():
                result["data_type"] = type_combo.currentText()
            else:
                result["data_type"] = "ARRAY"
                
                # Parse array display to get type and size
                if array_display:
                    current_text = array_display.text()
                    parts = current_text.split()
                    if len(parts) >= 3 and parts[1] == "of":
                        try:
                            result["array_size"] = int(parts[0])
                            result["element_type"] = parts[2]
                        except (ValueError, IndexError):
                            # Default values if parsing fails
                            result["array_size"] = 0
                            result["element_type"] = ""
        
        return result
    
    def validate_form(self):
        """Validate the form data
        
        Returns:
            bool: True if the form is valid, False otherwise
        """
        # Get form fields
        name_edit = self.findChild(QLineEdit, "name_edit")
        basic_radio = self.findChild(QRadioButton, "basic_radio")
        array_display = self.findChild(QLineEdit, "array_display")
        
        # Check field name
        if name_edit and not name_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Field name is required.")
            name_edit.setFocus()
            return False
        
        # Check array configuration if array is selected
        if basic_radio and not basic_radio.isChecked():
            if array_display:
                current_text = array_display.text().strip()
                if not current_text:
                    QMessageBox.warning(self, "Validation Error", "Array configuration is required.")
                    return False
                
                # Validate array format
                parts = current_text.split()
                if len(parts) < 3 or parts[1] != "of":
                    QMessageBox.warning(self, "Validation Error", "Invalid array format. Expected: <size> of <type>")
                    return False
                
                try:
                    size = int(parts[0])
                    if size <= 0:
                        QMessageBox.warning(self, "Validation Error", "Array size must be a positive integer.")
                        return False
                except ValueError:
                    QMessageBox.warning(self, "Validation Error", "Array size must be a number.")
                    return False
        
        return True
    
    def on_ok(self):
        """Handle OK button click"""
        if self.validate_form():
            self.result_data = self.collect_form_data()
            self.accept()
    
    @staticmethod
    def get_field_details(parent=None, field_data=None):
        """Static method to show the dialog and return the field details
        
        Args:
            parent: The parent widget
            field_data: Optional dictionary with field data to populate the form
            
        Returns:
            dict: Dictionary with the collected field details, or None if canceled
        """
        dialog = StructFieldDialog(parent, field_data)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            return dialog.result_data
        
        return None 