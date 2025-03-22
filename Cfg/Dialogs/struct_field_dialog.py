#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Structure Field Dialog
Modern implementation of the StructFieldDialog.ui
"""

import os
import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QComboBox, QRadioButton, QPushButton, 
                            QGroupBox, QDialogButtonBox, QFormLayout)
from PyQt5.QtCore import Qt

class StructFieldDialog(QDialog):
    """Dialog for editing structure fields"""
    
    def __init__(self, parent=None, field_data=None):
        """
        Initialize the dialog
        
        Args:
            parent: Parent widget
            field_data (dict, optional): Field data to edit
        """
        super(StructFieldDialog, self).__init__(parent)
        
        self.field_data = field_data or {}
        self.array_config = self.field_data.get("array_config", {})
        
        self.setup_ui()
        self.load_field_data()
        self.connect_signals_slots()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Set window properties
        self.setWindowTitle("Structure Field")
        self.resize(400, 250)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self)
        
        # Create form layout for field name
        self.form_layout = QFormLayout()
        
        # Field Name
        self.name_label = QLabel("Field Name:")
        self.name_edit = QLineEdit()
        self.form_layout.addRow(self.name_label, self.name_edit)
        
        # Add form layout to main layout
        self.main_layout.addLayout(self.form_layout)
        
        # Create field type group box
        self.type_group = QGroupBox("Field Type")
        self.type_layout = QVBoxLayout(self.type_group)
        
        # Radio button layout
        self.radio_layout = QHBoxLayout()
        
        # Basic type radio button
        self.basic_radio = QRadioButton("Basic Type")
        self.basic_radio.setChecked(True)
        
        # Array type radio button
        self.array_radio = QRadioButton("Array Type")
        
        # Add radio buttons to layout
        self.radio_layout.addWidget(self.basic_radio)
        self.radio_layout.addWidget(self.array_radio)
        
        # Type selection layout
        self.type_selection_layout = QHBoxLayout()
        
        # Type combo box for basic types
        self.type_combo = QComboBox()
        data_types = ["bool_t", "uint8", "uint16", "uint32", "uint64", 
                     "sint8", "sint16", "sint32", "sint64", 
                     "char_t", "float32", "float64"]
        
        for data_type in data_types:
            self.type_combo.addItem(data_type)
        
        self.type_selection_layout.addWidget(self.type_combo)
        
        # Array configuration layout
        self.array_layout = QHBoxLayout()
        
        # Array type label
        self.array_type_label = QLabel("Array of:")
        self.array_type_label.setVisible(False)
        
        # Array display field
        self.array_display = QLineEdit()
        self.array_display.setReadOnly(True)
        self.array_display.setVisible(False)
        
        # Configure array button
        self.configure_array_button = QPushButton("Configure...")
        self.configure_array_button.setVisible(False)
        
        # Add widgets to array layout
        self.array_layout.addWidget(self.array_type_label)
        self.array_layout.addWidget(self.array_display)
        self.array_layout.addWidget(self.configure_array_button)
        
        # Add layouts to type group layout
        self.type_layout.addLayout(self.radio_layout)
        self.type_layout.addLayout(self.type_selection_layout)
        self.type_layout.addLayout(self.array_layout)
        
        # Add type group to main layout
        self.main_layout.addWidget(self.type_group)
        
        # Create description layout
        self.description_layout = QFormLayout()
        
        # Description label and edit
        self.description_label = QLabel("Description:")
        self.description_edit = QLineEdit()
        self.description_layout.addRow(self.description_label, self.description_edit)
        
        # Add description layout to main layout
        self.main_layout.addLayout(self.description_layout)
        
        # Create button box
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        
        # Add button box to main layout
        self.main_layout.addWidget(self.buttonBox)
    
    def load_field_data(self):
        """Load field data into UI"""
        if not self.field_data:
            return
        
        # Load field name
        self.name_edit.setText(self.field_data.get("name", ""))
        
        # Load field type
        field_type = self.field_data.get("type", "")
        
        if "array" in self.field_data and self.field_data["array"]:
            # Set array radio button
            self.array_radio.setChecked(True)
            
            # Update array display
            self.update_array_display()
        else:
            # Set basic type radio button
            self.basic_radio.setChecked(True)
            
            # Set type combo index
            index = self.type_combo.findText(field_type)
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
        
        # Load description
        self.description_edit.setText(self.field_data.get("description", ""))
    
    def connect_signals_slots(self):
        """Connect signals and slots"""
        # Connect button box signals
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        # Connect array radio button toggled signal
        self.array_radio.toggled.connect(self.on_array_radio_toggled)
        
        # Connect configure array button clicked signal
        self.configure_array_button.clicked.connect(self.on_configure_array_clicked)
    
    def on_array_radio_toggled(self, checked):
        """Handle array radio button toggled"""
        # Show/hide array config widgets
        self.array_type_label.setVisible(checked)
        self.array_display.setVisible(checked)
        self.configure_array_button.setVisible(checked)
        
        # Show/hide type combo
        self.type_combo.setVisible(not checked)
    
    def on_configure_array_clicked(self):
        """Handle configure array button clicked"""
        # Open array type dialog
        from array_type_dialog import ArrayTypeDialog
        dialog = ArrayTypeDialog(self, self.array_config)
        
        if dialog.exec_() == QDialog.Accepted:
            # Get array configuration
            self.array_config = dialog.get_array_config()
            
            # Update array display
            self.update_array_display()
    
    def update_array_display(self):
        """Update array display field"""
        if not self.array_config:
            self.array_display.setText("")
            return
        
        element_type = self.array_config.get("element_type", "")
        size = self.array_config.get("size", 0)
        
        self.array_display.setText(f"{element_type}[{size}]")
    
    def get_field_data(self):
        """
        Get field data from UI
        
        Returns:
            dict: Field data
        """
        field_data = {}
        
        # Get field name
        field_data["name"] = self.name_edit.text()
        
        # Get field type
        if self.basic_radio.isChecked():
            # Basic type
            field_data["type"] = self.type_combo.currentText()
            field_data["array"] = False
        else:
            # Array type
            field_data["array"] = True
            field_data["array_config"] = self.array_config
            field_data["type"] = self.array_config.get("element_type", "") + "[]"
        
        # Get description
        field_data["description"] = self.description_edit.text()
        
        return field_data