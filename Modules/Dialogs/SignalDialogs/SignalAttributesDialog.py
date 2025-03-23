#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SignalAttributesDialog module for managing signal attributes
"""

import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QLabel, QLineEdit, QComboBox, QPushButton,
                            QDialogButtonBox, QMessageBox, QSpinBox, 
                            QGroupBox, QCheckBox, QTableWidget, QTableWidgetItem,
                            QHeaderView)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic

class SignalAttributesDialog(QDialog):
    """Dialog for managing signal attributes"""
    
    attributesChanged = pyqtSignal(dict)
    
    def __init__(self, parent=None, attributes=None):
        """Initialize the dialog
        
        Args:
            parent: The parent widget
            attributes: Optional dictionary with attributes to populate the dialog
        """
        super(SignalAttributesDialog, self).__init__(parent)
        
        # Set up member variables
        self.attributes = attributes or {}
        self.result_attributes = None
        
        # Set up UI
        self.setup_ui()
        
        # Connect signals and slots
        self.connect_signals_slots()
        
        # Populate data if provided
        if attributes:
            self.populate_form(attributes)
    
    def setup_ui(self):
        """Set up the user interface"""
        # Set window title
        self.setWindowTitle("Signal Attributes")
        
        # Create main layout
        self.main_layout = QVBoxLayout(self)
        
        # Create table for attributes
        self.attributes_table = QTableWidget(0, 3)
        self.attributes_table.setHorizontalHeaderLabels(["Name", "Value", "Actions"])
        self.attributes_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.attributes_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.attributes_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.main_layout.addWidget(self.attributes_table)
        
        # Create buttons for adding attributes
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Attribute")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addStretch()
        self.main_layout.addLayout(btn_layout)
        
        # Create standard dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.on_ok)
        button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(button_box)
        
        # Set dialog size
        self.resize(500, 400)
    
    def connect_signals_slots(self):
        """Connect signals and slots for dialog interactions"""
        self.add_btn.clicked.connect(self.on_add_attribute)
    
    def on_add_attribute(self):
        """Handle add attribute button click"""
        # Add a new row to the attributes table
        row = self.attributes_table.rowCount()
        self.attributes_table.insertRow(row)
        
        # Add name and value cells
        name_edit = QLineEdit()
        self.attributes_table.setCellWidget(row, 0, name_edit)
        
        value_edit = QLineEdit()
        self.attributes_table.setCellWidget(row, 1, value_edit)
        
        # Add delete button
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda: self.on_delete_attribute(row))
        self.attributes_table.setCellWidget(row, 2, delete_btn)
        
        # Set focus to name edit
        name_edit.setFocus()
    
    def on_delete_attribute(self, row):
        """Handle delete attribute button click
        
        Args:
            row: The row to delete
        """
        self.attributes_table.removeRow(row)
    
    def populate_form(self, attributes):
        """Populate the form with attributes
        
        Args:
            attributes: Dictionary with attributes to populate the form
        """
        # Clear existing rows
        self.attributes_table.setRowCount(0)
        
        # Add rows for each attribute
        for name, value in attributes.items():
            row = self.attributes_table.rowCount()
            self.attributes_table.insertRow(row)
            
            # Add name cell
            name_edit = QLineEdit(name)
            self.attributes_table.setCellWidget(row, 0, name_edit)
            
            # Add value cell
            value_edit = QLineEdit(str(value))
            self.attributes_table.setCellWidget(row, 1, value_edit)
            
            # Add delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, r=row: self.on_delete_attribute(r))
            self.attributes_table.setCellWidget(row, 2, delete_btn)
    
    def collect_form_data(self):
        """Collect data from the form
        
        Returns:
            dict: Dictionary with the collected attributes
        """
        result = {}
        
        # Collect attributes from table
        for row in range(self.attributes_table.rowCount()):
            name_edit = self.attributes_table.cellWidget(row, 0)
            value_edit = self.attributes_table.cellWidget(row, 1)
            
            if name_edit and value_edit:
                name = name_edit.text().strip()
                value = value_edit.text().strip()
                
                if name:
                    result[name] = value
        
        return result
    
    def validate_form(self):
        """Validate the form data
        
        Returns:
            bool: True if the form is valid, False otherwise
        """
        # Check for duplicate attribute names
        names = set()
        for row in range(self.attributes_table.rowCount()):
            name_edit = self.attributes_table.cellWidget(row, 0)
            
            if name_edit:
                name = name_edit.text().strip()
                
                if name:
                    if name in names:
                        QMessageBox.warning(self, "Validation Error", f"Duplicate attribute name: {name}")
                        return False
                    
                    names.add(name)
        
        return True
    
    def on_ok(self):
        """Handle OK button click"""
        if self.validate_form():
            self.result_attributes = self.collect_form_data()
            self.attributesChanged.emit(self.result_attributes)
            self.accept()
    
    @staticmethod
    def get_attributes(parent=None, attributes=None):
        """Static method to show the dialog and return the attributes
        
        Args:
            parent: The parent widget
            attributes: Optional dictionary with attributes to populate the dialog
            
        Returns:
            dict: Dictionary with the collected attributes, or None if canceled
        """
        dialog = SignalAttributesDialog(parent, attributes)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            return dialog.result_attributes
        
        return None 