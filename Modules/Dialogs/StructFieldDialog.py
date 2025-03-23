#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Struct Field Dialog module for managing fields in struct data types
"""

import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QComboBox, QDialogButtonBox, 
                           QPushButton, QMessageBox, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
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
        
        # Set up UI
        self.setup_ui()
        
        # Connect signals and slots
        self.connect_signals_slots()
        
        # Populate data if provided
        if field_data:
            self.populate_form(field_data)
    
    def setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("Struct Field")
        self.setMinimumWidth(300)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Create form layout
        form_layout = QFormLayout()
        layout.addLayout(form_layout)
        
        # Field name
        self.field_name_edit = QLineEdit()
        form_layout.addRow("Field Name:", self.field_name_edit)
        
        # Data type
        self.data_type_combo = QComboBox()
        self.data_type_combo.addItems([
            "UINT8", "UINT16", "UINT32", "UINT64",
            "INT8", "INT16", "INT32", "INT64",
            "FLOAT", "DOUBLE", "BOOL", "CHAR",
            "ARRAY", "ENUM", "STRUCT"
        ])
        form_layout.addRow("Data Type:", self.data_type_combo)
        
        # Array size (only shown for array type)
        self.array_size_edit = QLineEdit()
        self.array_size_row = form_layout.addRow("Array Size:", self.array_size_edit)
        self.array_size_row_index = form_layout.rowCount() - 1
        
        # Element type (only shown for array type)
        self.element_type_combo = QComboBox()
        self.element_type_combo.addItems([
            "UINT8", "UINT16", "UINT32", "UINT64",
            "INT8", "INT16", "INT32", "INT64",
            "FLOAT", "DOUBLE", "BOOL", "CHAR"
        ])
        self.element_type_row = form_layout.addRow("Element Type:", self.element_type_combo)
        self.element_type_row_index = form_layout.rowCount() - 1
        
        # Description
        self.description_edit = QLineEdit()
        form_layout.addRow("Description:", self.description_edit)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)
        
        # Store references to buttons
        self.ok_button = button_box.button(QDialogButtonBox.Ok)
        self.cancel_button = button_box.button(QDialogButtonBox.Cancel)
        
        # Hide array specific fields initially
        self.array_size_row.setVisible(False)
        self.element_type_row.setVisible(False)
    
    def connect_signals_slots(self):
        """Connect signals and slots for dialog interactions"""
        # Connect data type combo box changes
        self.data_type_combo.currentTextChanged.connect(self.on_data_type_changed)
        
        # Connect buttons
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.reject)
    
    def on_data_type_changed(self, data_type):
        """Handle changes to the data type combo box
        
        Args:
            data_type: The selected data type
        """
        # Show array fields only if array is selected
        is_array = data_type == "ARRAY"
        self.array_size_row.setVisible(is_array)
        self.element_type_row.setVisible(is_array)
    
    def populate_form(self, field_data):
        """Populate the form with field data
        
        Args:
            field_data: Dictionary with field data to populate the form
        """
        # Populate field name
        if "field_name" in field_data:
            self.field_name_edit.setText(field_data["field_name"])
        
        # Populate data type
        if "data_type" in field_data:
            index = self.data_type_combo.findText(field_data["data_type"])
            if index >= 0:
                self.data_type_combo.setCurrentIndex(index)
        
        # Populate array size
        if "array_size" in field_data:
            self.array_size_edit.setText(str(field_data["array_size"]))
        
        # Populate element type
        if "element_type" in field_data:
            index = self.element_type_combo.findText(field_data["element_type"])
            if index >= 0:
                self.element_type_combo.setCurrentIndex(index)
        
        # Populate description
        if "description" in field_data:
            self.description_edit.setText(field_data["description"])
    
    def collect_form_data(self):
        """Collect data from the form and return it as a dictionary"""
        result = {}
        
        # Collect field name
        result["field_name"] = self.field_name_edit.text().strip()
        
        # Collect data type
        result["data_type"] = self.data_type_combo.currentText()
        
        # Collect array specific fields if applicable
        if result["data_type"] == "ARRAY":
            try:
                result["array_size"] = int(self.array_size_edit.text().strip())
            except ValueError:
                result["array_size"] = 0
            
            result["element_type"] = self.element_type_combo.currentText()
        
        # Collect description
        result["description"] = self.description_edit.text().strip()
        
        return result
    
    def validate_form(self):
        """Validate the form data
        
        Returns:
            bool: True if the form is valid, False otherwise
        """
        # Check for field name
        if not self.field_name_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Field name is required.")
            self.field_name_edit.setFocus()
            return False
        
        # Check for array size if array is selected
        if self.data_type_combo.currentText() == "ARRAY":
            try:
                array_size = int(self.array_size_edit.text().strip())
                if array_size <= 0:
                    raise ValueError()
            except ValueError:
                QMessageBox.warning(self, "Validation Error", "Array size must be a positive integer.")
                self.array_size_edit.setFocus()
                return False
        
        return True
    
    def on_ok(self):
        """Handle OK button click"""
        if self.validate_form():
            self.result_data = self.collect_form_data()
            self.accept()
    
    @staticmethod
    def get_field_data(parent=None, field_data=None):
        """Static method to show the dialog and get the result
        
        Args:
            parent: The parent widget
            field_data: Optional dictionary with field data to populate the form
            
        Returns:
            dict or None: The collected field data if OK was clicked, None otherwise
        """
        dialog = StructFieldDialog(parent, field_data)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            return dialog.result_data
        
        return None 