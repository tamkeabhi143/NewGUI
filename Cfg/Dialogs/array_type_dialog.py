#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Array Type Dialog
Modern implementation of the ArrayTypeDialog.ui
"""

import os
import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLabel, 
                           QComboBox, QSpinBox, QDialogButtonBox)
from PyQt5.QtCore import Qt

class ArrayTypeDialog(QDialog):
    """Dialog for configuring array types"""
    
    def __init__(self, parent=None, array_config=None):
        """
        Initialize the dialog
        
        Args:
            parent: Parent widget
            array_config (dict, optional): Array configuration data
        """
        super(ArrayTypeDialog, self).__init__(parent)
        
        self.array_config = array_config or {}
        
        self.setup_ui()
        self.load_array_config()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Set window properties
        self.setWindowTitle("Array Type Definition")
        self.resize(400, 200)
        
        # Create main layout
        self.verticalLayout = QVBoxLayout(self)
        
        # Create form layout
        self.formLayout = QFormLayout()
        
        # Element Type
        self.element_type_label = QLabel("Element Type:")
        self.type_combo = QComboBox()
        
        data_types = ["bool_t", "uint8", "uint16", "uint32", "uint64", 
                     "sint8", "sint16", "sint32", "sint64", 
                     "char_t", "float32", "float64"]
        
        for data_type in data_types:
            self.type_combo.addItem(data_type)
        
        self.formLayout.addRow(self.element_type_label, self.type_combo)
        
        # Array Size
        self.array_size_label = QLabel("Array Size:")
        self.size_spin = QSpinBox()
        self.size_spin.setMinimum(1)
        self.size_spin.setMaximum(10000)
        self.size_spin.setValue(1)
        
        self.formLayout.addRow(self.array_size_label, self.size_spin)
        
        # Add form layout to main layout
        self.verticalLayout.addLayout(self.formLayout)
        
        # Create button box
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        
        # Connect button box signals
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        # Add button box to main layout
        self.verticalLayout.addWidget(self.buttonBox)
    
    def load_array_config(self):
        """Load array configuration data into UI"""
        if not self.array_config:
            return
        
        # Set element type
        element_type = self.array_config.get("element_type", "")
        index = self.type_combo.findText(element_type)
        if index >= 0:
            self.type_combo.setCurrentIndex(index)
        
        # Set array size
        self.size_spin.setValue(self.array_config.get("size", 1))
    
    def get_array_config(self):
        """
        Get array configuration data from UI
        
        Returns:
            dict: Array configuration data
        """
        array_config = {}
        
        # Get element type
        array_config["element_type"] = self.type_combo.currentText()
        
        # Get array size
        array_config["size"] = self.size_spin.value()
        
        return array_config