#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ArrayTypeDialog module for configuring array types
"""

import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLabel, 
                            QLineEdit, QComboBox, QSpinBox, 
                            QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5 import uic

class ArrayTypeDialog(QDialog):
    """Dialog for configuring array types"""
    
    def __init__(self, parent=None, current_type="", current_size=0):
        """Initialize the dialog
        
        Args:
            parent: The parent widget
            current_type: The current array element type
            current_size: The current array size
        """
        super(ArrayTypeDialog, self).__init__(parent)
        self.setWindowTitle("Configure Array")
        
        # Create layout
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        layout.addLayout(form_layout)
        
        # Create widgets
        self.type_combo = QComboBox(self)
        self.type_combo.addItems(["INTEGER", "FLOAT", "BOOLEAN", "STRING", "ENUM"])
        
        self.size_spin = QSpinBox(self)
        self.size_spin.setRange(1, 1000)
        self.size_spin.setValue(current_size if current_size > 0 else 1)
        
        # Add widgets to form
        form_layout.addRow("Element Type:", self.type_combo)
        form_layout.addRow("Array Size:", self.size_spin)
        
        # Create buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Set current type if provided
        if current_type:
            index = self.type_combo.findText(current_type)
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
        
        # Set dialog size
        self.resize(300, 150) 