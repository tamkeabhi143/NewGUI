#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Signal Manager App - Main Window Implementation
"""

import os
import json
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QStackedWidget, QFrame, 
                            QSplitter, QLineEdit, QComboBox, QFormLayout, 
                            QDateTimeEdit, QPlainTextEdit, QTableWidget, 
                            QHeaderView, QAbstractItemView, QMessageBox,
                            QFileDialog, QGraphicsDropShadowEffect, QCheckBox,
                            QTableWidgetItem, QStatusBar, QAction, QTreeWidget,
                            QTreeWidgetItem)
from PyQt5.QtCore import Qt, QSize, QDateTime, QSettings, pyqtSignal, QEvent, QRegExp
from PyQt5.QtGui import QIcon, QColor, QResizeEvent, QCloseEvent, QPixmap, QStandardItem
from PyQt5 import uic  # Import uic for loading UI files

# Import modules
from Modules.FileOperation.file_operations import FileOperations
from Modules.Dialogs.SignalDetailsDialog import SignalDetailsDialog

class SignalManagerApp(QMainWindow):
    """Main application window for Signal Manager"""
    
    # Custom signal for resize events
    resized = pyqtSignal()
    
    def __init__(self, parent=None):
        super(SignalManagerApp, self).__init__(parent)
        
        # Initialize properties
        self.file_operations = FileOperations()
        self.current_project_name = "Untitled"
        self.current_file_path = ""
        self.has_unsaved_changes = False
        self.project_data = {}
        self.recent_files = []
        self.max_recent_files = 5
        
        # Load UI from file
        self.setup_ui()
        
        # Connect signals and slots
        self.connect_signals_slots()
        
        # Load settings
        self.load_settings()
        
        # Update window title
        self.update_window_title()
    
    def setup_ui(self):
        """Load and set up the user interface from UI file"""
        # Load UI file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        ui_file_path = os.path.join(parent_dir, "Cfg", "LayoutFiles", "signal_manager_app.ui")
        uic.loadUi(ui_file_path, self)
        
        # Get references to important widgets from loaded UI
        self.content_stack = self.findChild(QStackedWidget, "content_stack")
        self.nav_buttons = []
        
        # Get navigation buttons
        nav_buttons_layout = self.findChild(QVBoxLayout, "nav_buttons_layout")
        if nav_buttons_layout:
            for i in range(nav_buttons_layout.count()):
                widget = nav_buttons_layout.itemAt(i).widget()
                if isinstance(widget, QPushButton) and widget.objectName().startswith("navButton"):
                    self.nav_buttons.append(widget)
        
        # Create and load project config page
        project_config_ui_path = os.path.join(parent_dir, "Cfg", "LayoutFiles", "project_config.ui")
        project_config_widget = QWidget()
        uic.loadUi(project_config_ui_path, project_config_widget)
        
        # Create and load signal database page
        signal_db_ui_path = os.path.join(parent_dir, "Cfg", "LayoutFiles", "signal_database.ui")
        signal_db_widget = QWidget()
        uic.loadUi(signal_db_ui_path, signal_db_widget)
        
        # Get existing pages or create new ones if needed
        page_project_config = self.content_stack.widget(1)
        page_signal_database = self.content_stack.widget(2)
        
        # If the pages exist, clear and update them; otherwise add new pages
        if page_project_config:
            # Remove existing page and replace with new one
            self.content_stack.removeWidget(page_project_config)
            self.content_stack.insertWidget(1, project_config_widget)
        
        if page_signal_database:
            # Remove existing page and replace with new one
            self.content_stack.removeWidget(page_signal_database)
            self.content_stack.insertWidget(2, signal_db_widget)
        
        # Set up dynamic elements not defined in UI file
        self.setup_shadow_effects()
        
        # Set up the FAB button position
        self.update_fab_position()
        
        # Initialize status bar - check if statusBar is a method or object
        try:
            # Try to access it as a method first
            if callable(self.statusBar):
                sb = self.statusBar()
                sb.showMessage("Ready")
            else:
                # If it's not callable, try to find it as an object
                sb = self.findChild(QStatusBar, "statusBar")
                if sb:
                    sb.showMessage("Ready")
        except (TypeError, AttributeError):
            # If all else fails, just create a new status bar
            print("Warning: Could not set status bar message")
    
    def setup_shadow_effects(self):
        """Add shadow effects to cards"""
        card_frames = self.findChildren(QFrame, QRegExp(".*_card$"))
        for card in card_frames:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setColor(QColor(0, 0, 0, 60))
            shadow.setOffset(0, 2)
            card.setGraphicsEffect(shadow)
    
    def update_fab_position(self):
        """Position the floating action button in the bottom-right corner of its parent"""
        # Find FAB button if it exists
        fab_button = self.findChild(QPushButton, "fabButton")
        if fab_button:
            page = fab_button.parent()
            if page:
                fab_button.move(page.width() - 76, page.height() - 76)
    
    def resizeEvent(self, event):
        """Handle resize events for the main window"""
        super().resizeEvent(event)
        
        # Update FAB position on resize
        self.update_fab_position()
        
        # Emit resized signal
        self.resized.emit()
    
    def closeEvent(self, event):
        """Handle close event for the main window"""
        if self.maybe_save():
            self.save_settings()
            event.accept()
        else:
            event.ignore()
    
    def connect_signals_slots(self):
        """Connect signals and slots for the application"""
        # Connect navigation buttons
        for i, button in enumerate(self.nav_buttons):
            button.clicked.connect(lambda checked, idx=i: self.set_active_page(idx))
        
        # Connect file menu actions
        # New action
        action_new = self.findChild(QAction, "actionNew")
        if action_new:
            action_new.setShortcut("Ctrl+N")
            action_new.setStatusTip("Create a new signal configuration")
            action_new.triggered.connect(self.on_new)
        
        # Open action
        action_open = self.findChild(QAction, "actionOpen")
        if action_open:
            action_open.setShortcut("Ctrl+O")
            action_open.setStatusTip("Open an existing signal configuration")
            action_open.triggered.connect(self.on_open)
        
        # Save action
        action_save = self.findChild(QAction, "actionSave")
        if action_save:
            action_save.setShortcut("Ctrl+S")
            action_save.setStatusTip("Save the current signal configuration")
            action_save.triggered.connect(self.on_save)
        
        # Save As action
        action_save_as = self.findChild(QAction, "actionSave_As")
        if action_save_as:
            action_save_as.setShortcut("Ctrl+Shift+S")
            action_save_as.setStatusTip("Save the current signal configuration with a new name")
            action_save_as.triggered.connect(self.on_save_as)
        
        # Export to Excel action
        action_export_to_excel = self.findChild(QAction, "actionExport_To_Excel")
        if action_export_to_excel:
            action_export_to_excel.setShortcut("Ctrl+E")
            action_export_to_excel.setStatusTip("Export the current configuration to Excel")
            action_export_to_excel.triggered.connect(self.on_export_to_excel)
        
        # Import from Excel action
        action_import_from_excel = self.findChild(QAction, "actionImport_From_Excel")
        if action_import_from_excel:
            action_import_from_excel.setShortcut("Ctrl+I")
            action_import_from_excel.setStatusTip("Import configuration from Excel")
            action_import_from_excel.triggered.connect(self.on_import_from_excel)
        
        # Close action
        action_close = self.findChild(QAction, "actionClose")
        if action_close:
            action_close.setShortcut("Ctrl+W")
            action_close.setStatusTip("Close the current configuration")
            action_close.triggered.connect(self.on_close)
        
        # Exit action
        action_exit = self.findChild(QAction, "actionExit")
        if action_exit:
            action_exit.setShortcut("Ctrl+Q")
            action_exit.setStatusTip("Exit the application")
            action_exit.triggered.connect(self.close)
        
        # Set up recent files menu if it exists
        self.setup_recent_files_menu()
        
        # Connect edit menu actions
        action_add_entry = self.findChild(QAction, "actionAdd_Entry")
        if action_add_entry:
            action_add_entry.setShortcut("Ctrl+A")
            action_add_entry.setStatusTip("Add a new entry")
            action_add_entry.triggered.connect(self.on_add_entry)
        
        action_delete_entry = self.findChild(QAction, "actionDelete_Entry")
        if action_delete_entry:
            action_delete_entry.setShortcut("Delete")
            action_delete_entry.setStatusTip("Delete the selected entry")
            action_delete_entry.triggered.connect(self.on_delete_entry)
        
        action_update_entry = self.findChild(QAction, "actionUpdate_Entry")
        if action_update_entry:
            action_update_entry.setShortcut("F2")
            action_update_entry.setStatusTip("Update the selected entry")
            action_update_entry.triggered.connect(self.on_update_entry)
        
        # Connect Code Generator menu actions
        action_signal_mgr = self.findChild(QAction, "actionSignalMgr")
        if action_signal_mgr:
            action_signal_mgr.setStatusTip("Generate SignalMgr code")
            action_signal_mgr.triggered.connect(self.on_signal_mgr_generator)
        
        action_ipc_manager = self.findChild(QAction, "actionIpcManager")
        if action_ipc_manager:
            action_ipc_manager.setStatusTip("Generate IpcManager code")
            action_ipc_manager.triggered.connect(self.on_ipc_manager_generator)
        
        action_ipc_ov_eth_mgr = self.findChild(QAction, "actionIpcOvEthMgr")
        if action_ipc_ov_eth_mgr:
            action_ipc_ov_eth_mgr.setStatusTip("Generate IpcOvEthMgr code")
            action_ipc_ov_eth_mgr.triggered.connect(self.on_ipc_ov_eth_mgr_generator)
        
        # Connect Help menu actions
        action_about_tool = self.findChild(QAction, "actionAbout_Tool")
        if action_about_tool:
            action_about_tool.setShortcut("F1")
            action_about_tool.setStatusTip("Show information about Signal Manager")
            action_about_tool.triggered.connect(self.on_about_tool)
        
        action_license = self.findChild(QAction, "actionLicense")
        if action_license:
            action_license.setStatusTip("Show license information")
            action_license.triggered.connect(self.on_license)
        
        # Connect FAB button if it exists
        fab_button = self.findChild(QPushButton, "fabButton")
        if fab_button:
            fab_button.clicked.connect(self.on_add_entry)
    
    def set_active_page(self, index):
        """Set the active page in the content stack"""
        # Update button states
        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)
        
        # Switch page in stack
        self.content_stack.setCurrentIndex(index)
    
    # File menu actions
    def on_new(self):
        """Create a new project"""
        if self.maybe_save():
            self.new_project()
    
    def on_open(self):
        """Open an existing project"""
        if self.maybe_save():
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open Project",
                os.path.expanduser("~/Documents"),
                "Signal Manager Files (*.smgr);;All Files (*)"
            )
            
            if file_path:
                self.load_project(file_path)
    
    def on_save(self):
        """Save the current project"""
        if not self.current_file_path:
            return self.on_save_as()
        else:
            return self.save_project(self.current_file_path)
    
    def on_save_as(self):
        """Save the current project as a new file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project",
            os.path.expanduser("~/Documents"),
            "Signal Manager Files (*.smgr);;All Files (*)"
        )
        
        if file_path:
            if not file_path.endswith(".smgr"):
                file_path += ".smgr"
            return self.save_project(file_path)
        return False
    
    def on_export_to_excel(self):
        """Export the current project data to Excel"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export to Excel",
            os.path.expanduser("~/Documents"),
            "Excel Files (*.xlsx);;CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            # Update data from UI before exporting
            self.update_data_from_ui()
            
            # Export data to Excel
            if self.file_operations.export_to_excel(file_path, self.project_data):
                QMessageBox.information(self, "Export Successful", f"Data was successfully exported to {file_path}")
                return True
            else:
                QMessageBox.warning(self, "Export Failed", f"Failed to export data to {file_path}")
                return False
        return False
    
    def on_import_from_excel(self):
        """Import project data from Excel"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import from Excel",
            os.path.expanduser("~/Documents"),
            "Excel Files (*.xlsx);;CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            # Import data from Excel
            imported_data = {}
            if self.file_operations.import_from_excel(file_path, imported_data):
                # Update project data with imported data
                self.project_data = imported_data
                
                # Update UI with new data
                self.update_ui_from_data()
                
                # Mark as having unsaved changes
                self.has_unsaved_changes = True
                self.update_window_title()
                
                QMessageBox.information(self, "Import Successful", f"Data was successfully imported from {file_path}")
                return True
            else:
                QMessageBox.warning(self, "Import Failed", f"Failed to import data from {file_path}")
                return False
        return False
    
    def on_close(self):
        """Close the current project"""
        if self.maybe_save():
            self.new_project()
            return True
        return False
    
    # Edit menu actions
    def on_add_entry(self):
        """Handler for add entry menu action"""
        # Create a new signal with default data
        default_signal_data = {
            "name": "New_Signal",
            "variable_port_name": "",
            "data_type": "UINT32",
            "memory_region": "Default",
            "type": "Input",
            "init_value": "Default",
            "asil": "QM",
            "buffer_count_ipc": 1,
            "impl_approach": "Default",
            "get_obj_ref": False,
            "notifiers": False,
            "sm_buff_count": 1,
            "timeout": 0,
            "periodicity": 0,
            "checksum": "None",
            "source_core": "Default"
        }
        
        # Open the dialog
        signal_data = SignalDetailsDialog.get_signal_details(self, default_signal_data)
        
        # If the user clicked OK, add the signal to the model
        if signal_data:
            self.add_signal_to_model(signal_data)
            self.statusBar().showMessage(f"Added signal: {signal_data['name']}", 3000)

    def add_signal_to_model(self, signal_data):
        """Add a signal to the model
        
        Args:
            signal_data: Dictionary with signal data
        """
        # Get the current model
        model = self.signal_tree.model()
        if not model:
            return
        
        # Create parent item for the signal
        parent_item = QStandardItem(signal_data["name"])
        parent_item.setData(signal_data, Qt.UserRole)
        
        # Add child items for important properties
        variable_port_name_item = QStandardItem("Variable Port: " + signal_data.get("variable_port_name", ""))
        data_type_item = QStandardItem("Data Type: " + signal_data.get("data_type", ""))
        memory_region_item = QStandardItem("Memory Region: " + signal_data.get("memory_region", ""))
        
        # Add items to parent
        parent_item.appendRow(variable_port_name_item)
        parent_item.appendRow(data_type_item)
        parent_item.appendRow(memory_region_item)
        
        # Add parent item to model
        model.appendRow(parent_item)
        
        # Expand the item
        index = model.indexFromItem(parent_item)
        self.signal_tree.expand(index)
        
        # Select the item
        self.signal_tree.setCurrentIndex(index)
    
    def on_delete_entry(self):
        """Handler for delete entry menu action"""
        # Get the selected item
        index = self.signal_tree.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "No Selection", "Please select a signal to delete.")
            return
        
        # Get the model
        model = self.signal_tree.model()
        if not model:
            return
        
        # Get the item
        item = model.itemFromIndex(index)
        if not item:
            return
        
        # If the item is a child item, get the parent item
        if item.parent():
            item = item.parent()
            index = item.index()
        
        # Get the signal name
        signal_name = item.text()
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the signal '{signal_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Remove the item from the model
            model.removeRow(index.row(), index.parent())
            self.statusBar().showMessage(f"Deleted signal: {signal_name}", 3000)
    
    def on_update_entry(self):
        """Handler for update entry menu action"""
        # Get the selected item
        index = self.signal_tree.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "No Selection", "Please select a signal to update.")
            return
        
        # Get the model
        model = self.signal_tree.model()
        if not model:
            return
        
        # Get the item and its data
        item = model.itemFromIndex(index)
        if not item:
            return
        
        # If the item is a child item, get the parent item
        if item.parent():
            item = item.parent()
            index = item.index()
        
        # Get the signal data
        signal_data = item.data(Qt.UserRole)
        if not signal_data:
            QMessageBox.warning(self, "No Data", "The selected item has no signal data.")
            return
        
        # Open the dialog
        updated_signal_data = SignalDetailsDialog.get_signal_details(self, signal_data)
        
        # If the user clicked OK, update the signal in the model
        if updated_signal_data:
            self.update_signal_in_model(index, updated_signal_data)
            self.statusBar().showMessage(f"Updated signal: {updated_signal_data['name']}", 3000)

    def update_signal_in_model(self, index, signal_data):
        """Update a signal in the model
        
        Args:
            index: The index of the signal to update
            signal_data: Dictionary with updated signal data
        """
        # Get the model
        model = self.signal_tree.model()
        if not model:
            return
        
        # Get the item
        item = model.itemFromIndex(index)
        if not item:
            return
        
        # Update the item
        item.setText(signal_data["name"])
        item.setData(signal_data, Qt.UserRole)
        
        # Remove all child items
        item.removeRows(0, item.rowCount())
        
        # Add child items for important properties
        variable_port_name_item = QStandardItem("Variable Port: " + signal_data.get("variable_port_name", ""))
        data_type_item = QStandardItem("Data Type: " + signal_data.get("data_type", ""))
        memory_region_item = QStandardItem("Memory Region: " + signal_data.get("memory_region", ""))
        
        # Add items to parent
        item.appendRow(variable_port_name_item)
        item.appendRow(data_type_item)
        item.appendRow(memory_region_item)
        
        # Expand the item
        self.signal_tree.expand(index)
        
        # Select the item
        self.signal_tree.setCurrentIndex(index)
    
    # Code Generator menu actions
    def on_signal_mgr_generator(self):
        """Generate SignalMgr code"""
        QMessageBox.information(self, "SignalMgr Generator", "SignalMgr Generator functionality to be implemented")
    
    def on_ipc_manager_generator(self):
        """Generate IpcManager code"""
        QMessageBox.information(self, "IpcManager Generator", "IpcManager Generator functionality to be implemented")
    
    def on_ipc_ov_eth_mgr_generator(self):
        """Generate IpcOvEthMgr code"""
        QMessageBox.information(self, "IpcOvEthMgr Generator", "IpcOvEthMgr Generator functionality to be implemented")
    
    # Help menu actions
    def on_about_tool(self):
        """Show About dialog"""
        about_text = """
        <h2>Signal Manager</h2>
        <p>Version 1.0.0</p>
        <p>A tool for managing signal configurations for embedded systems.</p>
        <p>&copy; 2023 Your Organization</p>
        """
        QMessageBox.about(self, "About Signal Manager", about_text)
    
    def on_license(self):
        """Show License dialog"""
        license_text = """
        Signal Manager - Signal configuration tool for embedded systems
        
        Copyright (C) 2023 Your Organization
        
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.
        
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        """
        QMessageBox.information(self, "License", license_text)
    
    # Project management
    def new_project(self):
        """Create a new project"""
        # Clear current project data
        self.current_project_name = "Untitled"
        self.current_file_path = ""
        self.has_unsaved_changes = False
        self.project_data = {}
        
        # Update UI
        self.update_ui_from_data()
        self.update_window_title()
    
    def load_project(self, file_path):
        """Load a project from a file"""
        if self.file_operations.load_config_file(file_path):
            # Get the project data
            self.project_data = self.file_operations.get_current_data()
            
            # Update file path and project name
            self.current_file_path = file_path
            file_info = os.path.basename(file_path)
            self.current_project_name = os.path.splitext(file_info)[0]
            
            # Update UI with loaded data
            self.update_ui_from_data()
            
            # Reset unsaved changes flag
            self.has_unsaved_changes = False
            self.update_window_title()
            
            # Add to recent files
            self.add_recent_file(file_path)
            
            QMessageBox.information(self, "Load Successful", f"Project was successfully loaded from {file_path}")
            return True
        else:
            QMessageBox.warning(self, "Load Failed", f"Failed to load project from {file_path}")
            return False
    
    def save_project(self, file_path):
        """Save the current project to a file"""
        # Update data from UI before saving
        self.update_data_from_ui()
        
        if self.file_operations.save_config_file(file_path, self.project_data):
            # Update file path and project name
            self.current_file_path = file_path
            file_info = os.path.basename(file_path)
            self.current_project_name = os.path.splitext(file_info)[0]
            
            # Reset unsaved changes flag
            self.has_unsaved_changes = False
            self.update_window_title()
            
            # Add to recent files
            self.add_recent_file(file_path)
            
            QMessageBox.information(self, "Save Successful", f"Project was successfully saved to {file_path}")
            return True
        else:
            QMessageBox.warning(self, "Save Failed", f"Failed to save project to {file_path}")
            return False
    
    def update_data_from_ui(self):
        """Update project data from UI elements"""
        # Version Details Card
        version_number_field = self.findChild(QLineEdit, "version_number_field")
        version_date_field = self.findChild(QDateTimeEdit, "version_date_field")
        updated_by_field = self.findChild(QLineEdit, "updated_by_field")
        change_desc_field = self.findChild(QPlainTextEdit, "change_desc_field")
        
        # Update project data with form values
        if "version" not in self.project_data:
            self.project_data["version"] = {}
            
        if version_number_field:
            self.project_data["version"]["number"] = version_number_field.text()
        
        if version_date_field:
            self.project_data["version"]["date"] = version_date_field.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        
        if updated_by_field:
            self.project_data["version"]["updated_by"] = updated_by_field.text()
        
        if change_desc_field:
            self.project_data["version"]["change_description"] = change_desc_field.toPlainText()
        
        # Handle Core Info Tree if it exists
        core_info_tree = self.findChild(QTreeWidget, "CoreInfoTreeObj")
        if core_info_tree:
            # Here you would implement the logic to extract data from the tree widget
            # This is a placeholder for the actual implementation
            pass
        
        # Mark as having unsaved changes
        self.has_unsaved_changes = True
        self.update_window_title()
    
    def update_ui_from_data(self):
        """Update UI elements from project data"""
        # Version Details Card
        version_number_field = self.findChild(QLineEdit, "version_number_field")
        version_date_field = self.findChild(QDateTimeEdit, "version_date_field")
        updated_by_field = self.findChild(QLineEdit, "updated_by_field")
        change_desc_field = self.findChild(QPlainTextEdit, "change_desc_field")
        
        # Update form values from project data
        if "version" in self.project_data:
            if version_number_field and "number" in self.project_data["version"]:
                version_number_field.setText(self.project_data["version"]["number"])
            
            if version_date_field and "date" in self.project_data["version"]:
                date_time = QDateTime.fromString(self.project_data["version"]["date"], "yyyy-MM-dd hh:mm:ss")
                if date_time.isValid():
                    version_date_field.setDateTime(date_time)
            
            if updated_by_field and "updated_by" in self.project_data["version"]:
                updated_by_field.setText(self.project_data["version"]["updated_by"])
            
            if change_desc_field and "change_description" in self.project_data["version"]:
                change_desc_field.setPlainText(self.project_data["version"]["change_description"])
        
        # Handle Core Info Tree if it exists
        core_info_tree = self.findChild(QTreeWidget, "CoreInfoTreeObj")
        if core_info_tree:
            # Here you would implement the logic to populate the tree widget from data
            # This is a placeholder for the actual implementation
            core_info_tree.clear()
            # Set column headers
            core_info_tree.setHeaderLabels(["Property", "Value"])
            # Example of populating tree (adjust based on your data structure)
            if "core_info" in self.project_data:
                self.populate_tree(core_info_tree, self.project_data["core_info"])
    
    def populate_tree(self, tree_widget, data_dict, parent_item=None):
        """Recursively populate a tree widget from a dictionary"""
        for key, value in data_dict.items():
            if parent_item:
                item = QTreeWidgetItem(parent_item, [str(key), ""])
            else:
                item = QTreeWidgetItem(tree_widget, [str(key), ""])
            
            if isinstance(value, dict):
                self.populate_tree(tree_widget, value, item)
            else:
                item.setText(1, str(value))
    
    def update_window_title(self):
        """Update the window title to reflect current project and save state"""
        title = "Signal Manager"
        
        if self.current_project_name:
            title += f" - {self.current_project_name}"
        
        if self.has_unsaved_changes:
            title += " *"
        
        self.setWindowTitle(title)
    
    def maybe_save(self):
        """Check if current project has unsaved changes and prompt to save"""
        if not self.has_unsaved_changes:
            return True
        
        reply = QMessageBox.question(
            self,
            "Signal Manager",
            "The document has been modified.\nDo you want to save your changes?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Save:
            return self.on_save()
        elif reply == QMessageBox.Cancel:
            return False
        
        return True
    
    def load_settings(self):
        """Load application settings"""
        settings = QSettings("YourOrganization", "SignalManager")
        
        # Window geometry
        geometry = settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        # Window state
        state = settings.value("windowState")
        if state:
            self.restoreState(state)
        
        # Recent files
        self.recent_files = settings.value("recentFiles", [])
        if self.recent_files:
            # Make sure it's a list
            if isinstance(self.recent_files, str):
                self.recent_files = [self.recent_files]
            
            # Filter out non-existent files
            self.recent_files = [f for f in self.recent_files if os.path.exists(f)]
            
            # Update the recent files menu
            self.update_recent_files_menu()
        
        # Other settings can be loaded here
    
    def save_settings(self):
        """Save application settings"""
        settings = QSettings("YourOrganization", "SignalManager")
        
        # Window geometry
        settings.setValue("geometry", self.saveGeometry())
        
        # Window state
        settings.setValue("windowState", self.saveState())
        
        # Recent files
        settings.setValue("recentFiles", self.recent_files)
        
        # Other settings can be saved here
    
    # Recent files handling
    def setup_recent_files_menu(self):
        """Set up the recent files menu"""
        # Find the menu bar and file menu
        menubar = self.findChild(QWidget, "menuBar")
        if menubar and isinstance(menubar, QWidget):
            # Find the File menu
            file_menu = None
            for action in menubar.actions():
                if action.text() == "File":
                    file_menu = action.menu()
                    break
            
            if file_menu:
                # Check if there's already a Recent Files menu
                for action in file_menu.actions():
                    if action.text() == "Recent Files":
                        self.recent_files_menu = action.menu()
                        return
                
                # Create Recent Files menu if it doesn't exist
                self.recent_files_menu = file_menu.addMenu("Recent Files")
                
                # Add a separator before Recent Files menu
                file_menu.insertSeparator(self.recent_files_menu.menuAction())
                
                # Update the menu with recent files
                self.update_recent_files_menu()
    
    def update_recent_files_menu(self):
        """Update the recent files menu with the current list of recent files"""
        if hasattr(self, 'recent_files_menu'):
            self.recent_files_menu.clear()
            
            for file_path in self.recent_files:
                file_name = os.path.basename(file_path)
                action = self.recent_files_menu.addAction(file_name)
                action.setData(file_path)
                action.triggered.connect(self.on_recent_file_triggered)
            
            if self.recent_files:
                self.recent_files_menu.addSeparator()
                self.recent_files_menu.addAction("Clear Recent Files").triggered.connect(self.on_clear_recent_files)
    
    def add_recent_file(self, file_path):
        """Add a file to the recent files list"""
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        
        self.recent_files.insert(0, file_path)
        
        # Limit the number of recent files
        if len(self.recent_files) > self.max_recent_files:
            self.recent_files = self.recent_files[:self.max_recent_files]
        
        self.update_recent_files_menu()
    
    def on_recent_file_triggered(self):
        """Handle a recent file being selected from the menu"""
        action = self.sender()
        if action and isinstance(action, QAction):
            file_path = action.data()
            if file_path and os.path.exists(file_path):
                if self.maybe_save():
                    self.load_project(file_path)
    
    def on_clear_recent_files(self):
        """Clear the recent files list"""
        self.recent_files = []
        self.update_recent_files_menu()