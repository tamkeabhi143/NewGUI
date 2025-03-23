#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Signal Details Dialog module for displaying and editing signal properties
"""

import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QComboBox, QCheckBox, QSpinBox, QDialogButtonBox, 
                            QTreeWidget, QTreeWidgetItem, QPushButton, QMessageBox,
                            QStackedWidget, QWidget)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from .StructFieldDialog import StructFieldDialog

class SignalDetailsDialog(QDialog):
    """Dialog for editing signal details"""
    
    def __init__(self, parent=None, signal_data=None):
        """Initialize the dialog
        
        Args:
            parent: The parent widget
            signal_data: Optional dictionary with signal data to populate the form
        """
        super(SignalDetailsDialog, self).__init__(parent)
        
        # Set up member variables
        self.signal_data = signal_data or {}
        self.result_data = None
        
        # Load UI from file
        self.setup_ui()
        
        # Connect signals and slots
        self.connect_signals_slots()
        
        # Populate data if provided
        if signal_data:
            self.populate_form(signal_data)
    
    def setup_ui(self):
        """Load and set up the user interface"""
        # Load UI file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        module_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        ui_file_path = os.path.join(module_dir, "Cfg", "LayoutFiles", "Dialogs", "SignalDetailsDialog.ui")
        uic.loadUi(ui_file_path, self)
        
        # Get references to important widgets
        self.content_stack = self.findChild(QStackedWidget, "content_stack")
        self.ok_button = self.findChild(QPushButton, "ok_button")
        self.cancel_button = self.findChild(QPushButton, "cancel_button")
        
        # Get navigation buttons
        self.nav_buttons = []
        for i in range(3):  # We have 3 navigation buttons
            button = self.findChild(QPushButton, f"navButton{i}")
            if button:
                self.nav_buttons.append(button)
        
        # Initialize UI elements based on selections
        self.initialize_dynamic_ui()
    
    def connect_signals_slots(self):
        """Connect signals and slots for dialog interactions"""
        # Connect navigation buttons
        for i, button in enumerate(self.nav_buttons):
            button.clicked.connect(lambda checked, idx=i: self.set_active_page(idx))
        
        # Connect data type combo box changes
        data_type_combo = self.findChild(QComboBox, "data_type_combo")
        if data_type_combo:
            data_type_combo.currentTextChanged.connect(self.on_data_type_changed)
        
        # Connect init value combo box changes
        init_value_combo = self.findChild(QComboBox, "init_value_combo")
        if init_value_combo:
            init_value_combo.currentTextChanged.connect(self.on_init_value_changed)
        
        # Connect struct field buttons
        add_field_button = self.findChild(QPushButton, "add_field_button")
        if add_field_button:
            add_field_button.clicked.connect(self.on_add_field)
        
        edit_field_button = self.findChild(QPushButton, "edit_field_button")
        if edit_field_button:
            edit_field_button.clicked.connect(self.on_edit_field)
        
        remove_field_button = self.findChild(QPushButton, "remove_field_button")
        if remove_field_button:
            remove_field_button.clicked.connect(self.on_remove_field)
        
        # Connect OK and Cancel buttons
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.reject)
    
    def set_active_page(self, index):
        """Set the active page in the stacked widget
        
        Args:
            index: The page index to activate
        """
        if self.content_stack:
            self.content_stack.setCurrentIndex(index)
        
        # Update button states
        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)
    
    def initialize_dynamic_ui(self):
        """Initialize dynamic UI elements based on selections"""
        # Handle struct visibility
        struct_group = self.findChild(QWidget, "struct_group")
        if struct_group:
            struct_group.setVisible(False)
    
    def on_data_type_changed(self, data_type):
        """Handle changes to the data type combo box
        
        Args:
            data_type: The selected data type
        """
        # Show struct fields if struct is selected
        struct_group = self.findChild(QWidget, "struct_group")
        if struct_group:
            struct_group.setVisible(data_type == "STRUCT")
    
    def on_init_value_changed(self, init_value):
        """Handle changes to the init value combo box
        
        Args:
            init_value: The selected init value
        """
        # Show custom value button if custom is selected
        custom_value_button = self.findChild(QPushButton, "custom_value_button")
        if custom_value_button:
            custom_value_button.setVisible(init_value == "Custom")
    
    def on_add_field(self):
        """Add a field to the struct definition"""
        dialog = StructFieldDialog(self)
        if dialog.exec_() == QDialog.Accepted and dialog.result_data:
            # Get the struct fields tree
            struct_fields_tree = self.findChild(QTreeWidget, "struct_fields_tree")
            if struct_fields_tree:
                # Create a tree item for the field
                field = dialog.result_data
                item = QTreeWidgetItem(struct_fields_tree)
                item.setText(0, field.get("field_name", ""))
                item.setText(1, field.get("data_type", ""))
                item.setText(2, field.get("description", ""))
                
                # Store the full field data in the item's data
                item.setData(0, Qt.UserRole, field)
                
                # Select the newly added item
                struct_fields_tree.setCurrentItem(item)
    
    def on_edit_field(self):
        """Edit the selected field in the struct definition"""
        # Get the struct fields tree
        struct_fields_tree = self.findChild(QTreeWidget, "struct_fields_tree")
        if struct_fields_tree:
            # Get the selected item
            item = struct_fields_tree.currentItem()
            if item:
                # Get the field data
                field = item.data(0, Qt.UserRole)
                if field:
                    dialog = StructFieldDialog(self, field)
                    if dialog.exec_() == QDialog.Accepted and dialog.result_data:
                        # Update the tree item
                        field = dialog.result_data
                        item.setText(0, field.get("field_name", ""))
                        item.setText(1, field.get("data_type", ""))
                        item.setText(2, field.get("description", ""))
                        
                        # Store the updated field data in the item's data
                        item.setData(0, Qt.UserRole, field)
            else:
                QMessageBox.warning(self, "No Selection", "Please select a field to edit.")
    
    def on_remove_field(self):
        """Remove the selected field from the struct definition"""
        # Get the struct fields tree
        struct_fields_tree = self.findChild(QTreeWidget, "struct_fields_tree")
        if struct_fields_tree:
            # Get the selected item
            item = struct_fields_tree.currentItem()
            if item:
                # Remove the item from the tree
                parent = item.parent()
                if parent:
                    parent.removeChild(item)
                else:
                    index = struct_fields_tree.indexOfTopLevelItem(item)
                    struct_fields_tree.takeTopLevelItem(index)
            else:
                QMessageBox.warning(self, "No Selection", "Please select a field to remove.")
    
    def populate_form(self, signal_data):
        """Populate the form with signal data
        
        Args:
            signal_data: Dictionary with signal data to populate the form
        """
        # Populate signal name
        signal_name_label = self.findChild(QLabel, "signal_name_label")
        signal_name_display = self.findChild(QLabel, "signal_name_display")
        if signal_name_label and signal_name_display and "name" in signal_data:
            signal_name_label.setText(signal_data["name"])
            signal_name_display.setText(signal_data["name"])
        
        # Populate variable port name
        variable_port_name_edit = self.findChild(QLineEdit, "variable_port_name_edit")
        if variable_port_name_edit and "variable_port_name" in signal_data:
            variable_port_name_edit.setText(signal_data["variable_port_name"])
        
        # Populate data type
        data_type_combo = self.findChild(QComboBox, "data_type_combo")
        if data_type_combo and "data_type" in signal_data:
            index = data_type_combo.findText(signal_data["data_type"])
            if index >= 0:
                data_type_combo.setCurrentIndex(index)
        
        # Populate memory region
        memory_region_combo = self.findChild(QComboBox, "memory_region_combo")
        if memory_region_combo and "memory_region" in signal_data:
            index = memory_region_combo.findText(signal_data["memory_region"])
            if index >= 0:
                memory_region_combo.setCurrentIndex(index)
        
        # Populate type
        type_combo = self.findChild(QComboBox, "type_combo")
        if type_combo and "type" in signal_data:
            index = type_combo.findText(signal_data["type"])
            if index >= 0:
                type_combo.setCurrentIndex(index)
        
        # Populate init value
        init_value_combo = self.findChild(QComboBox, "init_value_combo")
        if init_value_combo and "init_value" in signal_data:
            index = init_value_combo.findText(signal_data["init_value"])
            if index >= 0:
                init_value_combo.setCurrentIndex(index)
                
                # Show custom value button if custom is selected
                if signal_data["init_value"] == "Custom":
                    custom_value_button = self.findChild(QPushButton, "custom_value_button")
                    if custom_value_button:
                        custom_value_button.setVisible(True)
        
        # Populate ASIL
        asil_combo = self.findChild(QComboBox, "asil_combo")
        if asil_combo and "asil" in signal_data:
            index = asil_combo.findText(signal_data["asil"])
            if index >= 0:
                asil_combo.setCurrentIndex(index)
        
        # Populate struct fields if any
        if "struct_fields" in signal_data and signal_data.get("data_type") == "STRUCT":
            struct_fields_tree = self.findChild(QTreeWidget, "struct_fields_tree")
            struct_group = self.findChild(QWidget, "struct_group")
            
            if struct_fields_tree and struct_group:
                struct_group.setVisible(True)
                
                for field in signal_data["struct_fields"]:
                    item = QTreeWidgetItem(struct_fields_tree)
                    item.setText(0, field.get("field_name", ""))
                    item.setText(1, field.get("data_type", ""))
                    item.setText(2, field.get("description", ""))
                    
                    # Store the full field data in the item's data
                    item.setData(0, Qt.UserRole, field)
        
        # Populate advanced properties if any
        self.populate_advanced_properties(signal_data)
        
        # Populate core routing if any
        self.populate_core_routing(signal_data)
    
    def populate_advanced_properties(self, signal_data):
        """Populate the advanced properties tab with signal data
        
        Args:
            signal_data: Dictionary with signal data to populate the form
        """
        # Set advanced properties page
        self.set_active_page(1)
        
        # Populate buffer count IPC
        buffer_count_ipc_spin = self.findChild(QSpinBox, "buffer_count_ipc_spin")
        if buffer_count_ipc_spin and "buffer_count_ipc" in signal_data:
            buffer_count_ipc_spin.setValue(signal_data["buffer_count_ipc"])
        
        # Populate implementation approach
        impl_approach_combo = self.findChild(QComboBox, "impl_approach_combo")
        if impl_approach_combo and "impl_approach" in signal_data:
            index = impl_approach_combo.findText(signal_data["impl_approach"])
            if index >= 0:
                impl_approach_combo.setCurrentIndex(index)
        
        # Populate get object reference
        get_obj_ref_combo = self.findChild(QComboBox, "get_obj_ref_combo")
        if get_obj_ref_combo and "get_obj_ref" in signal_data:
            index = get_obj_ref_combo.findText(str(signal_data["get_obj_ref"]))
            if index >= 0:
                get_obj_ref_combo.setCurrentIndex(index)
        
        # Populate notifiers
        notifiers_combo = self.findChild(QComboBox, "notifiers_combo")
        if notifiers_combo and "notifiers" in signal_data:
            index = notifiers_combo.findText(str(signal_data["notifiers"]))
            if index >= 0:
                notifiers_combo.setCurrentIndex(index)
        
        # Populate SM buffer count
        sm_buff_count_spin = self.findChild(QSpinBox, "sm_buff_count_spin")
        if sm_buff_count_spin and "sm_buff_count" in signal_data:
            sm_buff_count_spin.setValue(signal_data["sm_buff_count"])
        
        # Populate timeout
        timeout_spin = self.findChild(QSpinBox, "timeout_spin")
        if timeout_spin and "timeout" in signal_data:
            timeout_spin.setValue(signal_data["timeout"])
        
        # Populate periodicity
        periodicity_spin = self.findChild(QSpinBox, "periodicity_spin")
        if periodicity_spin and "periodicity" in signal_data:
            periodicity_spin.setValue(signal_data["periodicity"])
        
        # Populate checksum
        checksum_combo = self.findChild(QComboBox, "checksum_combo")
        if checksum_combo and "checksum" in signal_data:
            index = checksum_combo.findText(signal_data["checksum"])
            if index >= 0:
                checksum_combo.setCurrentIndex(index)
        
        # Return to basic properties page
        self.set_active_page(0)
    
    def populate_core_routing(self, signal_data):
        """Populate the core routing tab with signal data
        
        Args:
            signal_data: Dictionary with signal data to populate the form
        """
        # Set core routing page
        self.set_active_page(2)
        
        # Populate source core
        source_combo = self.findChild(QComboBox, "source_combo")
        if source_combo and "source_core" in signal_data:
            index = source_combo.findText(signal_data["source_core"])
            if index >= 0:
                source_combo.setCurrentIndex(index)
        
        # TODO: Populate destination cores
        # This would depend on the specific structure used in the GUI
        
        # Return to basic properties page
        self.set_active_page(0)
    
    def collect_form_data(self):
        """Collect data from the form and return it as a dictionary"""
        result = {}
        
        # Collect signal name
        signal_name_display = self.findChild(QLabel, "signal_name_display")
        if signal_name_display:
            result["name"] = signal_name_display.text()
        
        # Collect variable port name
        variable_port_name_edit = self.findChild(QLineEdit, "variable_port_name_edit")
        if variable_port_name_edit:
            result["variable_port_name"] = variable_port_name_edit.text()
        
        # Collect data type
        data_type_combo = self.findChild(QComboBox, "data_type_combo")
        if data_type_combo:
            result["data_type"] = data_type_combo.currentText()
        
        # Collect memory region
        memory_region_combo = self.findChild(QComboBox, "memory_region_combo")
        if memory_region_combo:
            result["memory_region"] = memory_region_combo.currentText()
        
        # Collect type
        type_combo = self.findChild(QComboBox, "type_combo")
        if type_combo:
            result["type"] = type_combo.currentText()
        
        # Collect init value
        init_value_combo = self.findChild(QComboBox, "init_value_combo")
        if init_value_combo:
            result["init_value"] = init_value_combo.currentText()
        
        # Collect ASIL
        asil_combo = self.findChild(QComboBox, "asil_combo")
        if asil_combo:
            result["asil"] = asil_combo.currentText()
        
        # Collect struct fields if applicable
        if result.get("data_type") == "STRUCT":
            struct_fields_tree = self.findChild(QTreeWidget, "struct_fields_tree")
            if struct_fields_tree:
                struct_fields = []
                for i in range(struct_fields_tree.topLevelItemCount()):
                    item = struct_fields_tree.topLevelItem(i)
                    field = item.data(0, Qt.UserRole)
                    if field:
                        struct_fields.append(field)
                result["struct_fields"] = struct_fields
        
        # Collect advanced properties
        result.update(self.collect_advanced_properties())
        
        # Collect core routing
        result.update(self.collect_core_routing())
        
        return result
    
    def collect_advanced_properties(self):
        """Collect data from the advanced properties tab"""
        result = {}
        
        # Collect buffer count IPC
        buffer_count_ipc_spin = self.findChild(QSpinBox, "buffer_count_ipc_spin")
        if buffer_count_ipc_spin:
            result["buffer_count_ipc"] = buffer_count_ipc_spin.value()
        
        # Collect implementation approach
        impl_approach_combo = self.findChild(QComboBox, "impl_approach_combo")
        if impl_approach_combo:
            result["impl_approach"] = impl_approach_combo.currentText()
        
        # Collect get object reference
        get_obj_ref_combo = self.findChild(QComboBox, "get_obj_ref_combo")
        if get_obj_ref_combo:
            result["get_obj_ref"] = get_obj_ref_combo.currentText() == "True"
        
        # Collect notifiers
        notifiers_combo = self.findChild(QComboBox, "notifiers_combo")
        if notifiers_combo:
            result["notifiers"] = notifiers_combo.currentText() == "True"
        
        # Collect SM buffer count
        sm_buff_count_spin = self.findChild(QSpinBox, "sm_buff_count_spin")
        if sm_buff_count_spin:
            result["sm_buff_count"] = sm_buff_count_spin.value()
        
        # Collect timeout
        timeout_spin = self.findChild(QSpinBox, "timeout_spin")
        if timeout_spin:
            result["timeout"] = timeout_spin.value()
        
        # Collect periodicity
        periodicity_spin = self.findChild(QSpinBox, "periodicity_spin")
        if periodicity_spin:
            result["periodicity"] = periodicity_spin.value()
        
        # Collect checksum
        checksum_combo = self.findChild(QComboBox, "checksum_combo")
        if checksum_combo:
            result["checksum"] = checksum_combo.currentText()
        
        return result
    
    def collect_core_routing(self):
        """Collect data from the core routing tab"""
        result = {}
        
        # Collect source core
        source_combo = self.findChild(QComboBox, "source_combo")
        if source_combo:
            result["source_core"] = source_combo.currentText()
        
        # TODO: Collect destination cores
        # This would depend on the specific structure used in the GUI
        
        return result
    
    def validate_form(self):
        """Validate the form data
        
        Returns:
            bool: True if the form is valid, False otherwise
        """
        # Check for signal name
        signal_name_display = self.findChild(QLabel, "signal_name_display")
        if not signal_name_display or not signal_name_display.text().strip():
            QMessageBox.warning(self, "Validation Error", "Signal name is required.")
            return False
        
        # Check for variable port name
        variable_port_name_edit = self.findChild(QLineEdit, "variable_port_name_edit")
        if not variable_port_name_edit or not variable_port_name_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Variable port name is required.")
            self.set_active_page(0)  # Show the basic properties page
            variable_port_name_edit.setFocus()
            return False
        
        # If data type is STRUCT, check for struct fields
        data_type_combo = self.findChild(QComboBox, "data_type_combo")
        if data_type_combo and data_type_combo.currentText() == "STRUCT":
            struct_fields_tree = self.findChild(QTreeWidget, "struct_fields_tree")
            if not struct_fields_tree or struct_fields_tree.topLevelItemCount() == 0:
                QMessageBox.warning(self, "Validation Error", "Struct must have at least one field.")
                self.set_active_page(0)  # Show the basic properties page
                return False
        
        return True
    
    def on_ok(self):
        """Handle OK button click"""
        if self.validate_form():
            self.result_data = self.collect_form_data()
            self.accept()
    
    @staticmethod
    def get_signal_details(parent=None, signal_data=None):
        """Static method to show the dialog and get the result
        
        Args:
            parent: The parent widget
            signal_data: Optional dictionary with signal data to populate the form
            
        Returns:
            dict or None: The collected signal data if OK was clicked, None otherwise
        """
        dialog = SignalDetailsDialog(parent, signal_data)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            return dialog.result_data
        
        return None 