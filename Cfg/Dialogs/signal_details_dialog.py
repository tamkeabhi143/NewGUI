#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Signal Details Dialog
Modern implementation of the SignalDetailsDialog.ui
"""

import os
import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
                           QLabel, QLineEdit, QComboBox, QGroupBox, QTreeWidget, 
                           QTreeWidgetItem, QPushButton, QSpinBox, QFormLayout,
                           QScrollArea, QWidget, QCheckBox, QDateTimeEdit, QFrame,
                           QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

class SignalDetailsDialog(QDialog):
    """Dialog for editing signal details"""
    
    def __init__(self, parent=None, signal_name="SignalName"):
        super(SignalDetailsDialog, self).__init__(parent)
        
        self.signal_name = signal_name
        self.struct_fields = []
        
        self.setup_ui()
        self.connect_signals_slots()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Set window properties
        self.setWindowTitle("Signal Details")
        self.resize(600, 600)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create basic properties tab
        self.create_basic_tab()
        
        # Create advanced properties tab
        self.create_advanced_tab()
        
        # Create core routing tab
        self.create_routing_tab()
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.basic_tab, "Basic Properties")
        self.tab_widget.addTab(self.advanced_tab, "Advanced Properties")
        self.tab_widget.addTab(self.routing_tab, "Core Routing")
        
        # Set the default tab
        self.tab_widget.setCurrentIndex(0)
        
        # Create button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        
        # Create OK button
        self.ok_button = QPushButton("OK")
        self.ok_button.setDefault(True)
        self.ok_button.clicked.connect(self.accept)
        
        # Create Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        # Add buttons to layout
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        
        # Add tab widget and button layout to main layout
        self.main_layout.addWidget(self.tab_widget)
        self.main_layout.addLayout(self.button_layout)
    
    def create_basic_tab(self):
        """Create the basic properties tab"""
        self.basic_tab = QWidget()
        self.basic_tab_layout = QVBoxLayout(self.basic_tab)
        
        # Form layout for basic properties
        self.basic_form_layout = QFormLayout()
        self.basic_form_layout.setSpacing(15)
        
        # Signal Name
        self.signal_name_label_text = QLabel("Signal Name:")
        self.signal_name_label = QLabel(self.signal_name)
        bold_font = QFont()
        bold_font.setBold(True)
        self.signal_name_label.setFont(bold_font)
        self.basic_form_layout.addRow(self.signal_name_label_text, self.signal_name_label)
        
        # Variable Port Name
        self.var_port_name_label = QLabel("Variable Port Name:")
        self.variable_port_name_edit = QLineEdit()
        self.basic_form_layout.addRow(self.var_port_name_label, self.variable_port_name_edit)
        
        # Data Type
        self.data_type_label = QLabel("Data Type:")
        self.data_type_combo = QComboBox()
        self.data_type_combo.setEditable(True)
        
        data_types = ["INT8", "UINT8", "INT16", "UINT16", "INT32", "UINT32", 
                      "INT64", "UINT64", "FLOAT32", "FLOAT64", "BOOLEAN", 
                      "CHAR", "STRING", "STRUCT"]
        
        for data_type in data_types:
            self.data_type_combo.addItem(data_type)
        
        self.basic_form_layout.addRow(self.data_type_label, self.data_type_combo)
        
        # Structure Definition Group (hidden by default)
        self.struct_group = QGroupBox("Structure Definition")
        self.struct_group.setVisible(False)
        self.struct_layout = QVBoxLayout(self.struct_group)
        
        self.struct_fields_label = QLabel("Structure Fields:")
        self.struct_fields_tree = QTreeWidget()
        self.struct_fields_tree.setColumnCount(3)
        self.struct_fields_tree.setHeaderLabels(["Field Name", "Data Type", "Description"])
        self.struct_fields_tree.setAlternatingRowColors(True)
        
        self.field_buttons_layout = QHBoxLayout()
        self.add_field_button = QPushButton("Add Field")
        self.edit_field_button = QPushButton("Edit Field")
        self.remove_field_button = QPushButton("Remove Field")
        
        self.field_buttons_layout.addWidget(self.add_field_button)
        self.field_buttons_layout.addWidget(self.edit_field_button)
        self.field_buttons_layout.addWidget(self.remove_field_button)
        
        self.struct_layout.addWidget(self.struct_fields_label)
        self.struct_layout.addWidget(self.struct_fields_tree)
        self.struct_layout.addLayout(self.field_buttons_layout)
        
        # Description
        self.description_label = QLabel("Description:")
        self.description_edit = QLineEdit()
        self.basic_form_layout.addRow(self.description_label, self.description_edit)
        
        # Memory Region
        self.memory_region_label = QLabel("Memory Region:")
        self.memory_region_combo = QComboBox()
        memory_regions = ["DDR", "Cached", "NonCached"]
        for memory_region in memory_regions:
            self.memory_region_combo.addItem(memory_region)
        self.basic_form_layout.addRow(self.memory_region_label, self.memory_region_combo)
        
        # Type
        self.type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        types = ["Concurrent", "Sequential"]
        for type_item in types:
            self.type_combo.addItem(type_item)
        self.basic_form_layout.addRow(self.type_label, self.type_combo)
        
        # Init Value
        self.init_value_label = QLabel("Init Value:")
        self.init_value_combo = QComboBox()
        init_values = ["ZeroMemory", "Custom"]
        for init_value in init_values:
            self.init_value_combo.addItem(init_value)
        self.basic_form_layout.addRow(self.init_value_label, self.init_value_combo)
        
        # Custom Value Button (hidden by default)
        self.custom_value_button = QPushButton("Enter Custom Value...")
        self.custom_value_button.setVisible(False)
        self.basic_form_layout.addRow("", self.custom_value_button)
        
        # ASIL
        self.asil_label = QLabel("ASIL:")
        self.asil_combo = QComboBox()
        asil_values = ["QM", "A", "B", "C", "D"]
        for asil_value in asil_values:
            self.asil_combo.addItem(asil_value)
        self.basic_form_layout.addRow(self.asil_label, self.asil_combo)
        
        # Add form layout and struct group to tab layout
        self.basic_tab_layout.addLayout(self.basic_form_layout)
        self.basic_tab_layout.addWidget(self.struct_group)
        self.basic_tab_layout.addStretch()
    
    def create_advanced_tab(self):
        """Create the advanced properties tab"""
        self.advanced_tab = QWidget()
        self.advanced_tab_layout = QVBoxLayout(self.advanced_tab)
        
        # Card for advanced properties
        self.advanced_card = QFrame()
        self.advanced_card.setObjectName("card")
        self.advanced_card_layout = QVBoxLayout(self.advanced_card)
        
        # Form layout for advanced properties
        self.advanced_form_layout = QFormLayout()
        self.advanced_form_layout.setSpacing(15)
        
        # Buffer Count IPC
        self.buffer_count_ipc_label = QLabel("Buffer Count IPC:")
        self.buffer_count_ipc_spin = QSpinBox()
        self.buffer_count_ipc_spin.setMinimum(1)
        self.buffer_count_ipc_spin.setMaximum(10)
        self.advanced_form_layout.addRow(self.buffer_count_ipc_label, self.buffer_count_ipc_spin)
        
        # Implementation Approach
        self.impl_approach_label = QLabel("Implementation Approach:")
        self.impl_approach_combo = QComboBox()
        impl_approaches = ["SharedMemory", "VRING", "IpcOvEth"]
        for approach in impl_approaches:
            self.impl_approach_combo.addItem(approach)
        self.advanced_form_layout.addRow(self.impl_approach_label, self.impl_approach_combo)
        
        # Get Object Reference
        self.get_obj_ref_label = QLabel("Get Object Reference:")
        self.get_obj_ref_combo = QComboBox()
        self.get_obj_ref_combo.addItems(["False", "True"])
        self.advanced_form_layout.addRow(self.get_obj_ref_label, self.get_obj_ref_combo)
        
        # Notifiers
        self.notifiers_label = QLabel("Notifiers:")
        self.notifiers_combo = QComboBox()
        self.notifiers_combo.addItems(["False", "True"])
        self.advanced_form_layout.addRow(self.notifiers_label, self.notifiers_combo)
        
        # SM Buffer Count
        self.sm_buff_count_label = QLabel("SM Buffer Count:")
        self.sm_buff_count_spin = QSpinBox()
        self.sm_buff_count_spin.setMinimum(1)
        self.sm_buff_count_spin.setMaximum(10)
        self.advanced_form_layout.addRow(self.sm_buff_count_label, self.sm_buff_count_spin)
        
        # Timeout
        self.timeout_label = QLabel("Timeout:")
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setMinimum(10)
        self.timeout_spin.setMaximum(200)
        self.timeout_spin.setSingleStep(10)
        self.timeout_spin.setSuffix(" ms")
        self.advanced_form_layout.addRow(self.timeout_label, self.timeout_spin)
        
        # Periodicity
        self.periodicity_label = QLabel("Periodicity:")
        self.periodicity_spin = QSpinBox()
        self.periodicity_spin.setMinimum(10)
        self.periodicity_spin.setMaximum(200)
        self.periodicity_spin.setSingleStep(10)
        self.periodicity_spin.setSuffix(" ms")
        self.advanced_form_layout.addRow(self.periodicity_label, self.periodicity_spin)
        
        # Checksum
        self.checksum_label = QLabel("Checksum:")
        self.checksum_combo = QComboBox()
        checksum_types = ["None", "Additive", "CustomChecksum"]
        for checksum_type in checksum_types:
            self.checksum_combo.addItem(checksum_type)
        self.advanced_form_layout.addRow(self.checksum_label, self.checksum_combo)
        
        # Add form layout to card layout
        self.advanced_card_layout.addLayout(self.advanced_form_layout)
        
        # Add card to tab layout
        self.advanced_tab_layout.addWidget(self.advanced_card)
        self.advanced_tab_layout.addStretch()
    
    def create_routing_tab(self):
        """Create the core routing tab"""
        self.routing_tab = QWidget()
        self.routing_tab_layout = QVBoxLayout(self.routing_tab)
        
        # Create scroll area for core routing
        self.core_scroll_area = QScrollArea()
        self.core_scroll_area.setWidgetResizable(True)
        
        # Create scroll content widget
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        
        # Source Core Group
        self.source_group = QGroupBox("Source Core")
        self.source_layout = QVBoxLayout(self.source_group)
        
        # Source Core Combo
        self.source_combo = QComboBox()
        self.source_combo.addItem("<None>")
        
        self.source_layout.addWidget(self.source_combo)
        
        # Destination Cores Group
        self.dest_group = QGroupBox("Destination Cores")
        self.dest_layout = QVBoxLayout(self.dest_group)
        
        # Add groups to scroll layout
        self.scroll_layout.addWidget(self.source_group)
        self.scroll_layout.addWidget(self.dest_group)
        
        # Set scroll content widget
        self.core_scroll_area.setWidget(self.scroll_content)
        
        # Add scroll area to tab layout
        self.routing_tab_layout.addWidget(self.core_scroll_area)
    
    def connect_signals_slots(self):
        """Connect signals and slots"""
        # Connect data type change to handle struct visibility
        self.data_type_combo.currentTextChanged.connect(self.on_data_type_changed)
        
        # Connect init value change to handle custom value button visibility
        self.init_value_combo.currentTextChanged.connect(self.on_init_value_changed)
    
    def on_data_type_changed(self, text):
        """Handle data type change"""
        # Show structure definition group if STRUCT is selected
        self.struct_group.setVisible(text == "STRUCT")
    
    def on_init_value_changed(self, text):
        """Handle init value change"""
        # Show custom value button if Custom is selected
        self.custom_value_button.setVisible(text == "Custom")