#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data Type Selection Dialog
Modern implementation of the UserDataTypeDialog.ui
"""

import os
import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QComboBox, QRadioButton, QPushButton, 
                           QGroupBox, QTreeWidget, QTreeWidgetItem, 
                           QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt

class DataTypeSelectionDialog(QDialog):
    """Dialog for selecting data types"""
    
    def __init__(self, parent=None, data_type=None):
        """
        Initialize the dialog
        
        Args:
            parent: Parent widget
            data_type (dict, optional): Data type information
        """
        super(DataTypeSelectionDialog, self).__init__(parent)
        
        self.data_type = data_type or {}
        self.struct_fields = self.data_type.get("struct_fields", [])
        self.array_config = self.data_type.get("array_config", {})
        
        self.setup_ui()
        self.load_data_type()
        self.connect_signals_slots()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Set window properties
        self.setWindowTitle("Select Data Type")
        self.resize(600, 500)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self)
        
        # Create type group box
        self.type_group = QGroupBox("Data Type")
        self.type_layout = QVBoxLayout(self.type_group)
        
        # Radio button layout
        self.radio_layout = QHBoxLayout()
        
        # Primitive type radio button
        self.primitive_radio = QRadioButton("Primitive Type")
        self.primitive_radio.setChecked(True)
        
        # Structure type radio button
        self.struct_radio = QRadioButton("Structure Type")
        
        # Array type radio button
        self.array_radio = QRadioButton("Array Type")
        
        # Add radio buttons to layout
        self.radio_layout.addWidget(self.primitive_radio)
        self.radio_layout.addWidget(self.struct_radio)
        self.radio_layout.addWidget(self.array_radio)
        
        # Add radio layout to type layout
        self.type_layout.addLayout(self.radio_layout)
        
        # Form layout for type selection
        self.form_layout = QFormLayout()
        
        # Type label and combo
        self.type_label = QLabel("Data Type:")
        self.type_combo = QComboBox()
        
        data_types = ["bool_t", "uint8", "uint16", "uint32", "uint64", 
                     "sint8", "sint16", "sint32", "sint64", 
                     "char_t", "float32", "float64"]
        
        for data_type in data_types:
            self.type_combo.addItem(data_type)
        
        self.form_layout.addRow(self.type_label, self.type_combo)
        
        # Add form layout to type layout
        self.type_layout.addLayout(self.form_layout)
        
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
        
        # Add array layout to type layout
        self.type_layout.addLayout(self.array_layout)
        
        # Add type group to main layout
        self.main_layout.addWidget(self.type_group)
        
        # Create structure definition group
        self.struct_group = QGroupBox("Structure Definition")
        self.struct_group.setVisible(False)
        self.struct_layout = QVBoxLayout(self.struct_group)
        
        # Structure fields label
        self.struct_fields_label = QLabel("Structure Fields:")
        
        # Structure fields tree
        self.struct_fields_tree = QTreeWidget()
        self.struct_fields_tree.setColumnCount(3)
        self.struct_fields_tree.setHeaderLabels(["Field Name", "Data Type", "Description"])
        self.struct_fields_tree.setAlternatingRowColors(True)
        
        # Field buttons layout
        self.field_buttons_layout = QHBoxLayout()
        
        # Add field button
        self.add_field_button = QPushButton("Add Field")
        
        # Edit field button
        self.edit_field_button = QPushButton("Edit Field")
        
        # Remove field button
        self.remove_field_button = QPushButton("Remove Field")
        
        # Add buttons to layout
        self.field_buttons_layout.addWidget(self.add_field_button)
        self.field_buttons_layout.addWidget(self.edit_field_button)
        self.field_buttons_layout.addWidget(self.remove_field_button)
        
        # Add widgets to struct layout
        self.struct_layout.addWidget(self.struct_fields_label)
        self.struct_layout.addWidget(self.struct_fields_tree)
        self.struct_layout.addLayout(self.field_buttons_layout)
        
        # Add struct group to main layout
        self.main_layout.addWidget(self.struct_group)
        
        # Create button layout
        self.button_layout = QHBoxLayout()
        
        # Add spacer to push buttons to the right
        self.button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # OK button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        # Add buttons to layout
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        
        # Add button layout to main layout
        self.main_layout.addLayout(self.button_layout)
    
    def load_data_type(self):
        """Load data type information into UI"""
        if not self.data_type:
            return
        
        # Get type information
        type_info = self.data_type.get("type", "")
        is_struct = self.data_type.get("is_struct", False)
        is_array = self.data_type.get("is_array", False)
        
        if is_struct:
            # Set structure radio button
            self.struct_radio.setChecked(True)
            
            # Load structure fields
            self.load_struct_fields()
        elif is_array:
            # Set array radio button
            self.array_radio.setChecked(True)
            
            # Update array display
            self.update_array_display()
        else:
            # Set primitive radio button
            self.primitive_radio.setChecked(True)
            
            # Set type combo index
            index = self.type_combo.findText(type_info)
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
    
    def load_struct_fields(self):
        """Load structure fields into tree widget"""
        # Clear tree widget
        self.struct_fields_tree.clear()
        
        # Add fields to tree widget
        for field in self.struct_fields:
            item = QTreeWidgetItem(self.struct_fields_tree)
            item.setText(0, field.get("name", ""))
            item.setText(1, field.get("type", ""))
            item.setText(2, field.get("description", ""))
    
    def update_array_display(self):
        """Update array display field"""
        if not self.array_config:
            self.array_display.setText("")
            return
        
        element_type = self.array_config.get("element_type", "")
        size = self.array_config.get("size", 0)
        
        self.array_display.setText(f"{element_type}[{size}]")
    
    def connect_signals_slots(self):
        """Connect signals and slots"""
        # Connect radio button toggled signals
        self.struct_radio.toggled.connect(self.on_struct_radio_toggled)
        self.array_radio.toggled.connect(self.on_array_radio_toggled)
        
        # Connect field buttons clicked signals
        self.add_field_button.clicked.connect(self.on_add_field_clicked)
        self.edit_field_button.clicked.connect(self.on_edit_field_clicked)
        self.remove_field_button.clicked.connect(self.on_remove_field_clicked)
        
        # Connect configure array button clicked signal
        self.configure_array_button.clicked.connect(self.on_configure_array_clicked)
    
    def on_struct_radio_toggled(self, checked):
        """Handle structure radio button toggled"""
        # Show/hide structure definition group
        self.struct_group.setVisible(checked)
        
        # Show/hide type combo
        self.type_combo.setVisible(not checked)
    
    def on_array_radio_toggled(self, checked):
        """Handle array radio button toggled"""
        # Show/hide array config widgets
        self.array_type_label.setVisible(checked)
        self.array_display.setVisible(checked)
        self.configure_array_button.setVisible(checked)
        
        # Show/hide type combo
        self.type_combo.setVisible(not checked)
    
    def on_add_field_clicked(self):
        """Handle add field button clicked"""
        # Open structure field dialog
        from struct_field_dialog import StructFieldDialog
        dialog = StructFieldDialog(self)
        
        if dialog.exec_() == QDialog.Accepted:
            # Get field data
            field_data = dialog.get_field_data()
            
            # Add field to struct fields
            self.struct_fields.append(field_data)
            
            # Add field to tree widget
            item = QTreeWidgetItem(self.struct_fields_tree)
            item.setText(0, field_data.get("name", ""))
            item.setText(1, field_data.get("type", ""))
            item.setText(2, field_data.get("description", ""))
    
    def on_edit_field_clicked(self):
        """Handle edit field button clicked"""
        # Get selected item
        selected_items = self.struct_fields_tree.selectedItems()
        if not selected_items:
            return
        
        selected_item = selected_items[0]
        selected_index = self.struct_fields_tree.indexOfTopLevelItem(selected_item)
        
        # Get field data
        field_data = self.struct_fields[selected_index]
        
        # Open structure field dialog
        from struct_field_dialog import StructFieldDialog
        dialog = StructFieldDialog(self, field_data)
        
        if dialog.exec_() == QDialog.Accepted:
            # Get updated field data
            updated_field_data = dialog.get_field_data()
            
            # Update field in struct fields
            self.struct_fields[selected_index] = updated_field_data
            
            # Update field in tree widget
            selected_item.setText(0, updated_field_data.get("name", ""))
            selected_item.setText(1, updated_field_data.get("type", ""))
            selected_item.setText(2, updated_field_data.get("description", ""))
    
    def on_remove_field_clicked(self):
        """Handle remove field button clicked"""
        # Get selected item
        selected_items = self.struct_fields_tree.selectedItems()
        if not selected_items:
            return
        
        selected_item = selected_items[0]
        selected_index = self.struct_fields_tree.indexOfTopLevelItem(selected_item)
        
        # Remove field from struct fields
        del self.struct_fields[selected_index]
        
        # Remove field from tree widget
        self.struct_fields_tree.takeTopLevelItem(selected_index)
    
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
    
    def get_data_type(self):
        """
        Get data type information from UI
        
        Returns:
            dict: Data type information
        """
        data_type = {}
        
        # Get type information based on selected radio button
        if self.primitive_radio.isChecked():
            # Primitive type
            data_type["type"] = self.type_combo.currentText()
            data_type["is_struct"] = False
            data_type["is_array"] = False
        elif self.struct_radio.isChecked():
            # Structure type
            data_type["type"] = "struct"
            data_type["is_struct"] = True
            data_type["is_array"] = False
            data_type["struct_fields"] = self.struct_fields
        else:
            # Array type
            data_type["type"] = "array"
            data_type["is_struct"] = False
            data_type["is_array"] = True
            data_type["array_config"] = self.array_config
        
        return data_type