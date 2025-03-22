#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Core Properties Dialog
Modern implementation of the CorePropertiesDialog.ui
"""

import os
import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QComboBox, QCheckBox, QPushButton, 
                           QFormLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt

class CorePropertiesDialog(QDialog):
    """Dialog for editing core properties"""
    
    def __init__(self, parent=None, core_data=None):
        """
        Initialize the dialog
        
        Args:
            parent: Parent widget
            core_data (dict, optional): Core properties data
        """
        super(CorePropertiesDialog, self).__init__(parent)
        
        self.core_data = core_data or {}
        
        self.setup_ui()
        self.load_core_data()
        self.connect_signals_slots()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Set window properties
        self.setWindowTitle("Core Properties")
        self.resize(400, 400)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self)
        
        # Create form layout
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)
        
        # Core Name
        self.name_label = QLabel("Core Name:")
        self.name_edit = QLineEdit()
        self.form_layout.addRow(self.name_label, self.name_edit)
        
        # Description
        self.description_label = QLabel("Description:")
        self.description_edit = QLineEdit()
        self.form_layout.addRow(self.description_label, self.description_edit)
        
        # Empty label for spacing
        self.empty_label_1 = QLabel("")
        
        # Is Master Core checkbox
        self.master_checkbox = QCheckBox("Is Master Core")
        self.form_layout.addRow(self.empty_label_1, self.master_checkbox)
        
        # OS Type
        self.os_label = QLabel("OS Type:")
        self.os_combo = QComboBox()
        
        os_types = ["Unknown", "Linux", "QNX", "AUTOSAR", "FreeRTOS", "Windows", "Other"]
        for os_type in os_types:
            self.os_combo.addItem(os_type)
        
        self.form_layout.addRow(self.os_label, self.os_combo)
        
        # Empty label for custom OS
        self.empty_label_2 = QLabel("")
        
        # Custom OS field
        self.custom_os_edit = QLineEdit()
        self.custom_os_edit.setPlaceholderText("Enter custom OS type")
        self.custom_os_edit.setVisible(False)
        self.form_layout.addRow(self.empty_label_2, self.custom_os_edit)
        
        # SOC Family
        self.soc_family_label = QLabel("SOC Family:")
        self.soc_family_combo = QComboBox()
        
        soc_families = ["Unknown", "TI", "Tricore", "NXP", "Intel", "AMD", "Raspberry Pi", "Other"]
        for soc_family in soc_families:
            self.soc_family_combo.addItem(soc_family)
        
        self.form_layout.addRow(self.soc_family_label, self.soc_family_combo)
        
        # Empty label for custom SOC family
        self.empty_label_3 = QLabel("")
        
        # Custom SOC family field
        self.custom_soc_family_edit = QLineEdit()
        self.custom_soc_family_edit.setPlaceholderText("Enter custom SOC family")
        self.custom_soc_family_edit.setVisible(False)
        self.form_layout.addRow(self.empty_label_3, self.custom_soc_family_edit)
        
        # Empty label for QNX checkbox
        self.empty_label_4 = QLabel("")
        
        # Is QNX Core checkbox
        self.qnx_checkbox = QCheckBox("Is QNX Core")
        self.form_layout.addRow(self.empty_label_4, self.qnx_checkbox)
        
        # Empty label for Autosar checkbox
        self.empty_label_5 = QLabel("")
        
        # Is Autosar Compliant checkbox
        self.autosar_checkbox = QCheckBox("Is Autosar Compliant")
        self.form_layout.addRow(self.empty_label_5, self.autosar_checkbox)
        
        # Empty label for Simulation checkbox
        self.empty_label_6 = QLabel("")
        
        # Is Simulation Core checkbox
        self.sim_checkbox = QCheckBox("Is Simulation Core")
        self.form_layout.addRow(self.empty_label_6, self.sim_checkbox)
        
        # Add form layout to main layout
        self.main_layout.addLayout(self.form_layout)
        
        # Add vertical spacer
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
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
    
    def load_core_data(self):
        """Load core data into UI"""
        if not self.core_data:
            return
        
        # Load core name
        self.name_edit.setText(self.core_data.get("name", ""))
        
        # Load description
        self.description_edit.setText(self.core_data.get("description", ""))
        
        # Load is master core
        self.master_checkbox.setChecked(self.core_data.get("is_master", False))
        
        # Load OS type
        os_type = self.core_data.get("os_type", "Unknown")
        if os_type in ["Unknown", "Linux", "QNX", "AUTOSAR", "FreeRTOS", "Windows"]:
            index = self.os_combo.findText(os_type)
            if index >= 0:
                self.os_combo.setCurrentIndex(index)
        else:
            index = self.os_combo.findText("Other")
            if index >= 0:
                self.os_combo.setCurrentIndex(index)
            self.custom_os_edit.setText(os_type)
            self.custom_os_edit.setVisible(True)
        
        # Load SOC family
        soc_family = self.core_data.get("soc_family", "Unknown")
        if soc_family in ["Unknown", "TI", "Tricore", "NXP", "Intel", "AMD", "Raspberry Pi"]:
            index = self.soc_family_combo.findText(soc_family)
            if index >= 0:
                self.soc_family_combo.setCurrentIndex(index)
        else:
            index = self.soc_family_combo.findText("Other")
            if index >= 0:
                self.soc_family_combo.setCurrentIndex(index)
            self.custom_soc_family_edit.setText(soc_family)
            self.custom_soc_family_edit.setVisible(True)
        
        # Load additional flags
        self.qnx_checkbox.setChecked(self.core_data.get("is_qnx", False))
        self.autosar_checkbox.setChecked(self.core_data.get("is_autosar", False))
        self.sim_checkbox.setChecked(self.core_data.get("is_simulation", False))
    
    def connect_signals_slots(self):
        """Connect signals and slots"""
        # Connect combo box changed signals
        self.os_combo.currentTextChanged.connect(self.on_os_combo_changed)
        self.soc_family_combo.currentTextChanged.connect(self.on_soc_family_combo_changed)
    
    def on_os_combo_changed(self, text):
        """Handle OS combo box changed"""
        # Show/hide custom OS field
        self.custom_os_edit.setVisible(text == "Other")
    
    def on_soc_family_combo_changed(self, text):
        """Handle SOC family combo box changed"""
        # Show/hide custom SOC family field
        self.custom_soc_family_edit.setVisible(text == "Other")
    
    def get_core_data(self):
        """
        Get core data from UI
        
        Returns:
            dict: Core data
        """
        core_data = {}
        
        # Get core name
        core_data["name"] = self.name_edit.text()
        
        # Get description
        core_data["description"] = self.description_edit.text()
        
        # Get is master core
        core_data["is_master"] = self.master_checkbox.isChecked()
        
        # Get OS type
        os_type = self.os_combo.currentText()
        if os_type == "Other":
            os_type = self.custom_os_edit.text()
        core_data["os_type"] = os_type
        
        # Get SOC family
        soc_family = self.soc_family_combo.currentText()
        if soc_family == "Other":
            soc_family = self.custom_soc_family_edit.text()
        core_data["soc_family"] = soc_family
        
        # Get additional flags
        core_data["is_qnx"] = self.qnx_checkbox.isChecked()
        core_data["is_autosar"] = self.autosar_checkbox.isChecked()
        core_data["is_simulation"] = self.sim_checkbox.isChecked()
        
        return core_data