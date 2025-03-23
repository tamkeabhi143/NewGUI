#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Signal Manager App - Main Window Implementation
"""

import os
import json
from PyQt5 import QtWidgets, uic  # Import QtWidgets and uic
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QStackedWidget, QFrame, 
                            QSplitter, QLineEdit, QComboBox, QFormLayout, 
                            QDateTimeEdit, QPlainTextEdit, QTableWidget, 
                            QHeaderView, QAbstractItemView, QMessageBox,
                            QFileDialog, QGraphicsDropShadowEffect, QCheckBox,
                            QTableWidgetItem, QStatusBar, QAction, QTreeWidget,
                            QTreeWidgetItem, QDialog, QSpinBox)
from PyQt5.QtCore import Qt, QSize, QDateTime, QSettings, pyqtSignal, QEvent, QRegExp
from PyQt5.QtGui import QIcon, QColor, QResizeEvent, QCloseEvent, QPixmap, QStandardItem

# Import the compiled resources
import Cfg.Resources.resources_rc

# Import modules
from Modules.FileOperation.FileOperations import FileOperations
from Modules.MenuOperation.menu_operations import MenuOperations
from Modules.Dialogs.SignalDialogs.SignalDetailsDialog import SignalDetailsDialog
from Modules.Dialogs.CoreConfigurationManager.CoreConfig import CoreConfigManager
from Modules.SignalOperations.SignalManager import SignalManager

class SignalManagerApp(QMainWindow):
    """Main application window for Signal Manager"""
    
    # Custom signal for resize events
    resized = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize the main window"""
        super(SignalManagerApp, self).__init__(parent)
        
        # Initialize properties
        self.current_project_name = "Untitled"
        self.current_file_path = ""
        self.has_unsaved_changes = False
        self.project_data = {}
        self.recent_files = []
        self.max_recent_files = 5
        self.current_file = None
        self.username = "Guest"  # Default username
        self.signal_edit_stack = []  # For undo operations
        
        # Set project path
        self.project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Load UI from file
        self.setup_ui()

        # Create SignalManager instance
        self.signal_manager = SignalManager(self)
        self.signal_manager.set_project_data(self.project_data)
        
        # Initialize file operations after UI setup
        self.file_operations = FileOperations(self)
        
        # Connect signals and slots
        self.connect_signals_slots()
        
        # Load settings
        self.load_settings()
        
        # Update profile section
        self.set_username(self.username)
        
        # Set default values for version fields
        self.set_default_version_fields()
        
        # Initialize UI elements and connect signals
        self.init_ui()
    
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
        
        # Make sure the toolbar is visible
        toolbar = self.findChild(QWidget, "mainToolBar")
        if toolbar:
            toolbar.setVisible(True)
            # Ensure all icons in toolbar are properly set
            self.setup_toolbar_icons()
        
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
        
        # Initialize profile section
        self.initialize_profile_section()
    
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
        
        # Connect update button
        update_button = self.findChild(QPushButton, "update_button")
        if update_button:
            update_button.clicked.connect(self.on_update_configuration)
        
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
            # Call FileOperations to create a new project
            self.file_operations.new_file()

            # Call Core Configuration Manager to show the configuration dialog
            config_manager = CoreConfigManager(self)
            config_data = config_manager.show_and_get_config(is_new_file=True)
            if config_data:
                # Update the project with the new configuration
                self.project_data["core_info"] = config_data
                self.update_ui_from_data()
                self.has_unsaved_changes = True
                self.update_window_title()
    
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
        # Check if change description is empty
        change_desc_field = self.findChild(QPlainTextEdit, "change_desc_field")
        if change_desc_field and not change_desc_field.toPlainText().strip():
            # Highlight the change description field
            change_desc_field.setFocus()
            change_desc_field.setStyleSheet("background-color: #ffcccc;")
            
            # Prompt user to update the change description
            reply = QMessageBox.warning(
                self,
                "Missing Change Description",
                "Please enter a change description before exporting.",
                QMessageBox.Ok
            )
            return False
        
        # Reset style if it was highlighted
        if change_desc_field:
            change_desc_field.setStyleSheet("")
        
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
        """Handler for add entry menu action - forwards to add_signal method"""
        # Make sure we're on the signal database page
        self.switch_to_signal_database()
        # Call the add_signal method
        self.add_signal()
    
    def on_delete_entry(self):
        """Handler for delete entry menu action - forwards to delete_signal method"""
        # Make sure we're on the signal database page
        self.switch_to_signal_database()
        # Call the delete_signal method
        self.delete_signal()
    
    def on_update_entry(self):
        """Handler for update entry menu action - forwards to edit_signal method"""
        # Make sure we're on the signal database page
        self.switch_to_signal_database()
        # Call the edit_signal method
        self.edit_signal()
    
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
    
    # Signal model operations
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
        # Check if change description is empty
        change_desc_field = self.findChild(QPlainTextEdit, "change_desc_field")
        if change_desc_field and not change_desc_field.toPlainText().strip():
            # Highlight the change description field
            change_desc_field.setFocus()
            change_desc_field.setStyleSheet("background-color: #ffcccc;")
            
            # Prompt user to update the change description
            reply = QMessageBox.warning(
                self,
                "Missing Change Description",
                "Please enter a change description before saving.",
                QMessageBox.Ok
            )
            return False
        
        # Reset style if it was highlighted
        if change_desc_field:
            change_desc_field.setStyleSheet("")
        
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
        
        # If a file is open, update the updated_by field with current username
        if updated_by_field:
            if self.current_file_path:
                updated_by_field.setText(self.username)
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
        
        # Sync ComboBoxes with core configuration data
        if "core_info" in self.project_data:
            self.sync_combo_boxes_with_core_config(self.project_data["core_info"])
    
    def populate_tree(self, tree_widget, data_dict, parent_item=None):
        """Recursively populate a tree widget from a dictionary"""
        # If this is core_info data, only show core_properties
        if 'core_properties' in data_dict:
            # Clear and set header style
            tree_widget.setStyleSheet("QTreeWidget { background-color: #f5f5f5; }")
            
            # Create Core Properties parent item
            core_properties_item = QTreeWidgetItem(tree_widget, ["Core Properties", ""])
            core_properties_item.setBackground(0, QColor("#e0e0e0"))
            core_properties_item.setBackground(1, QColor("#e0e0e0"))
            
            # For each SoC in core_properties
            for soc_name, cores in data_dict['core_properties'].items():
                # Create SoC item
                soc_item = QTreeWidgetItem(core_properties_item, [soc_name, ""])
                soc_item.setBackground(0, QColor("#f0f0f0"))
                
                # For each core in the SoC
                for core_name, properties in cores.items():
                    # Create core item
                    core_item = QTreeWidgetItem(soc_item, [core_name, ""])
                    core_item.setBackground(0, QColor("#f8f8f8"))
                    
                    # Add properties as child items
                    for prop_name, prop_value in properties.items():
                        if prop_name != 'name':  # Skip the name as it's already shown
                            # Format property name for better display
                            display_name = prop_name.replace('_', ' ').title()
                            prop_item = QTreeWidgetItem(core_item, [display_name, str(prop_value)])
                
                # Expand the SoC item
                soc_item.setExpanded(True)
            
            # Expand the Core Properties item
            core_properties_item.setExpanded(True)
            return
            
        # Default recursive behavior for other dictionary data
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
        """Update the window title based on project state"""
        title = "Signal Manager"
        
        # Add project file name if available
        if hasattr(self, 'project_file') and self.project_file:
            title += f" - {os.path.basename(self.project_file)}"
        
        # Add modified indicator
        if hasattr(self, 'project_modified') and self.project_modified:
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

    def set_username(self, username):
        """Set the current username
        
        Args:
            username: The username to set
        """
        self.username = username
        
        # Find profile elements
        profile_name = self.findChild(QLabel, "profile_name")
        updated_by_field = self.findChild(QLineEdit, "updated_by_field")
        
        # Update profile name only if it exists
        if profile_name:
            # Get the current text format
            current_text = profile_name.text()
            
            # If the text already contains "Welcome," preserve it
            if "Welcome" in current_text:
                profile_name.setText(f"Welcome, {username}")
            else:
                # Otherwise, just set the username
                profile_name.setText(username)
        
        # Update updated_by_field if no file is open
        if updated_by_field and not self.current_file_path:
            updated_by_field.setText(username)
        
        # Update username in status bar
        self.statusBar.showMessage(f"Logged in as: {username}", 5000)

    def initialize_profile_section(self):
        """Initialize the profile section with default values"""
        profile_name = self.findChild(QLabel, "profile_name")

        if profile_name:
            # Set default username
            profile_name.setText("Guest")

    def set_icon_paths(self, main_app_icons_path, toolbar_icons_path):
        """Set the paths for application icons
        
        Args:
            main_app_icons_path: Path to main application icons
            toolbar_icons_path: Path to toolbar icons
        """
        self.main_app_icons_path = main_app_icons_path
        self.toolbar_icons_path = toolbar_icons_path
        
        # Apply icons to actions if paths are valid
        if os.path.exists(toolbar_icons_path):
            self.setup_toolbar_icons()
    
    def setup_toolbar_icons(self):
        """Set up toolbar icons from QActions defined in the UI file"""
        # List of action names to ensure icons are properly set
        action_names = [
            "actionNew", "actionOpen", "actionSave", "actionSave_As",
            "actionExport_To_Excel", "actionImport_From_Excel",
            "actionAdd_Entry", "actionDelete_Entry", "actionUpdate_Entry",
            "actionUndo", "actionRedo"
        ]
        
        # Loop through actions and ensure icons are set
        for action_name in action_names:
            action = self.findChild(QAction, action_name)
            if action:
                # If action has no icon, try to set it directly
                if action.icon().isNull() and hasattr(self, 'toolbar_icons_path'):
                    # Convert action name to icon filename
                    icon_name = action_name.replace("action", "")
                    if icon_name == "Save_As":
                        icon_name = "SaveAs"
                    icon_path = os.path.join(self.toolbar_icons_path, f"{icon_name}.png")
                    
                    # Set the icon if the file exists
                    if os.path.exists(icon_path):
                        action.setIcon(QIcon(icon_path))
        
        # Make sure the toolbar is visible
        toolbar = self.findChild(QWidget, "mainToolBar")
        if toolbar:
            toolbar.setVisible(True)

    def on_update_configuration(self):
        """Update the core configuration"""
        # Show the core configuration dialog with existing data
        config_manager = CoreConfigManager(self)
        
        # Get existing core info or an empty dict if it doesn't exist
        existing_data = self.project_data.get("core_info", {})
        
        # Show the dialog with existing data
        updated_config = config_manager.show_and_get_config(False, existing_data)
        
        if updated_config:
            # Update the project with the new configuration
            self.project_data["core_info"] = updated_config
            self.update_ui_from_data()
            self.has_unsaved_changes = True
            self.update_window_title()
            QMessageBox.information(self, "Configuration Updated", "The core configuration has been updated.")

    def sync_combo_boxes_with_core_config(self, core_info):
        """Synchronize ComboBoxes in signal_database.ui with core configuration data"""
        # Find the ComboBoxes in signal_database UI
        build_image_combo = self.findChild(QComboBox, "buildImageComboBox")
        soc_combo = self.findChild(QComboBox, "socComboBox")
        board_combo = self.findChild(QComboBox, "boardComboBox")
        
        # Also find ComboBoxes in core_configuration UI to ensure they're in sync
        core_build_image_combo = self.findChild(QComboBox, "coreImageTypeCombo")
        core_soc_combo = self.findChild(QComboBox, "coreSocCombo")
        core_board_combo = self.findChild(QComboBox, "coreBoardCombo")
        
        # Clear the ComboBoxes
        if build_image_combo:
            build_image_combo.clear()
        
        if soc_combo:
            soc_combo.clear()
        
        if board_combo:
            board_combo.clear()
            
        # Clear core config ComboBoxes if they exist
        if core_build_image_combo:
            core_build_image_combo.clear()
        
        if core_soc_combo:
            core_soc_combo.clear()
        
        if core_board_combo:
            core_board_combo.clear()
        
        # Populate build image ComboBox
        if 'image_types' in core_info:
            for image_type in core_info['image_types']:
                # Add to signal database combo
                if build_image_combo:
                    build_image_combo.addItem(image_type)
                # Add to core config combo
                if core_build_image_combo:
                    core_build_image_combo.addItem(image_type)
        
        # Populate SoC ComboBox
        if 'socs' in core_info:
            for soc in core_info['socs']:
                # Add to signal database combo
                if soc_combo:
                    soc_combo.addItem(soc)
                # Add to core config combo
                if core_soc_combo:
                    core_soc_combo.addItem(soc)
        
        # Populate board ComboBox
        if 'boards' in core_info:
            for board in core_info['boards']:
                # Add to signal database combo
                if board_combo:
                    board_combo.addItem(board)
                # Add to core config combo
                if core_board_combo:
                    core_board_combo.addItem(board)
        
        # Connect signals and slots for synchronization between UIs
        # Only connect if not already connected (avoid multiple connections)
        if build_image_combo and core_build_image_combo:
            # Disconnect existing connections if any
            try:
                build_image_combo.currentIndexChanged.disconnect()
                core_build_image_combo.currentIndexChanged.disconnect()
            except TypeError:
                pass  # No connections to disconnect
                
            # Connect new signals
            build_image_combo.currentIndexChanged.connect(
                lambda idx: core_build_image_combo.setCurrentIndex(idx) if core_build_image_combo.count() > idx else None)
            core_build_image_combo.currentIndexChanged.connect(
                lambda idx: build_image_combo.setCurrentIndex(idx) if build_image_combo.count() > idx else None)
        
        if soc_combo and core_soc_combo:
            # Disconnect existing connections if any
            try:
                soc_combo.currentIndexChanged.disconnect()
                core_soc_combo.currentIndexChanged.disconnect()
            except TypeError:
                pass  # No connections to disconnect
                
            # Connect new signals
            soc_combo.currentIndexChanged.connect(
                lambda idx: core_soc_combo.setCurrentIndex(idx) if core_soc_combo.count() > idx else None)
            core_soc_combo.currentIndexChanged.connect(
                lambda idx: soc_combo.setCurrentIndex(idx) if soc_combo.count() > idx else None)
        
        if board_combo and core_board_combo:
            # Disconnect existing connections if any
            try:
                board_combo.currentIndexChanged.disconnect()
                core_board_combo.currentIndexChanged.disconnect()
            except TypeError:
                pass  # No connections to disconnect
                
            # Connect new signals
            board_combo.currentIndexChanged.connect(
                lambda idx: core_board_combo.setCurrentIndex(idx) if core_board_combo.count() > idx else None)
            core_board_combo.currentIndexChanged.connect(
                lambda idx: board_combo.setCurrentIndex(idx) if board_combo.count() > idx else None)
                
        # Also update the source_combo in SignalDetailsDialog if it exists
        signal_details_dialogs = self.findChildren(QDialog)
        for dialog in signal_details_dialogs:
            if dialog.objectName() == "SignalDetailsDialog":
                source_combo = dialog.findChild(QComboBox, "source_combo")
                if source_combo:
                    source_combo.clear()
                    source_combo.addItem("<None>")
                    
                    # Add cores from all SOCs
                    if 'core_properties' in core_info:
                        for soc, cores in core_info['core_properties'].items():
                            for core_name in cores.keys():
                                source_combo.addItem(f"{soc} - {core_name}")
                
                # Update any other core-related comboboxes in the dialog if needed

    def set_default_version_fields(self):
        """Set default values for version fields"""
        # Find version fields
        version_number_field = self.findChild(QLineEdit, "version_number_field")
        version_date_field = self.findChild(QDateTimeEdit, "version_date_field")
        updated_by_field = self.findChild(QLineEdit, "updated_by_field")
        
        # Set default version number to 1.0
        if version_number_field:
            version_number_field.setText("1.0")
        
        # Set default version date to current date and time
        if version_date_field:
            version_date_field.setDateTime(QDateTime.currentDateTime())
        
        # Set default updated by to current username
        if updated_by_field:
            updated_by_field.setText(self.username)

    def setup_signal_database_page(self):
        """Set up the signal database page"""
        # Find widgets
        signal_tree = self.findChild(QTreeWidget, "signalTree")
        add_signal_btn = self.findChild(QPushButton, "addSignalBtn")
        delete_signal_btn = self.findChild(QPushButton, "deleteSignalBtn")
        edit_signal_btn = self.findChild(QPushButton, "editSignalBtn")
        save_signal_btn = self.findChild(QPushButton, "saveSignalBtn")
        cancel_btn = self.findChild(QPushButton, "cancelBtn")
        signal_details_card = self.findChild(QFrame, "signal_details_card")
        
        # Connect signals
        if signal_tree:
            signal_tree.itemSelectionChanged.connect(self.on_signal_selected)
        
        if add_signal_btn:
            add_signal_btn.clicked.connect(self.add_signal)
        
        if delete_signal_btn:
            delete_signal_btn.clicked.connect(self.delete_signal)
        
        if edit_signal_btn:
            edit_signal_btn.clicked.connect(self.edit_signal)
        
        if save_signal_btn:
            save_signal_btn.clicked.connect(self.save_signal)
        
        if cancel_btn:
            cancel_btn.clicked.connect(self.cancel_signal_edit)
        
        # Initialize the signal details section as disabled
        if signal_details_card:
            self.set_signal_details_enabled(False)
    
    def set_signal_details_enabled(self, enabled):
        """Enable or disable the signal details section"""
        signal_details_card = self.findChild(QFrame, "signal_details_card")
        if not signal_details_card:
            return
        
        # Find all input widgets in the signal details card
        input_widgets = []
        for input_type in [QLineEdit, QComboBox, QSpinBox, QCheckBox, QPushButton]:
            input_widgets.extend(signal_details_card.findChildren(input_type))
        
        # Enable or disable each widget
        for widget in input_widgets:
            # Don't disable the Cancel button
            if widget.objectName() == "cancelBtn":
                continue
                
            widget.setEnabled(enabled)
        
        # Set visual indicator that the section is disabled
        dynamic_attrs_placeholder = self.findChild(QLabel, "dynamicAttrsPlaceholder")
        if dynamic_attrs_placeholder:
            if enabled:
                dynamic_attrs_placeholder.setText("Dynamic attributes based on Core Configuration")
            else:
                dynamic_attrs_placeholder.setText("Select a signal to edit properties")
    
    def on_signal_selected(self):
        """Handle signal selection from the tree"""
        signal_tree = self.findChild(QTreeWidget, "signalTree")
        if not signal_tree:
            return
        
        selected_items = signal_tree.selectedItems()
        if not selected_items:
            # No selection, disable details section
            self.set_signal_details_enabled(False)
            return
        
        # Enable details section and populate with selected signal data
        self.set_signal_details_enabled(True)
        
        # Get the selected signal data
        selected_item = selected_items[0]
        signal_id = selected_item.text(0)
        signal_name = selected_item.text(1)
        
        # Find the signal data in the project data
        signal_data = self.find_signal_by_id(signal_id)
        if signal_data:
            self.populate_signal_details(signal_data)
    
    def add_signal(self):
        """Add a new signal"""
        # Create a temporary signal object
        temp_signal = {
            "id": self.generate_signal_id(),
            "name": "",
            "description": "",
            "data_type": ""
        }
        
        # First, prompt for signal name
        name, ok = QtWidgets.QInputDialog.getText(
            self, "Signal Name", "Enter signal name:")
        
        if not ok or not name.strip():
            return
        
        temp_signal["name"] = name.strip()
        
        # Then show data type selection dialog
        data_type_dialog = self.show_data_type_selection_dialog()
        if not data_type_dialog:
            return
        
        # Update the signal with data type information
        temp_signal.update(data_type_dialog)
        
        # Finally, show signal details dialog for properties
        signal_details = SignalDetailsDialog.get_signal_details(self, temp_signal)
        if not signal_details:
            return
        
        # If the user completed all steps, add the signal to the database
        self.add_signal_to_database(signal_details)
        
        # Refresh the signal tree
        self.update_signal_tree()
    
    def show_data_type_selection_dialog(self):
        """Show dialog for selecting data type"""
        # Load dialog from UI file
        data_type_dialog = QtWidgets.QDialog(self)
        
        # Find the path to the UI file
        ui_file = os.path.join(self.project_path, "Cfg", "LayoutFiles", "Dialogs", "DataTypeSelectionDialog.ui")
        
        # Check if the file exists
        if not os.path.exists(ui_file):
            QtWidgets.QMessageBox.warning(self, "Error", f"UI file not found: {ui_file}")
            return None
        
        # Load the UI
        uic.loadUi(ui_file, data_type_dialog)
        
        # Connect dialog buttons
        button_box = data_type_dialog.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        if button_box:
            button_box.accepted.connect(data_type_dialog.accept)
            button_box.rejected.connect(data_type_dialog.reject)
        
        # Connect signals and handlers based on selection
        primitive_radio = data_type_dialog.findChild(QtWidgets.QRadioButton, "primitive_radio")
        struct_radio = data_type_dialog.findChild(QtWidgets.QRadioButton, "struct_radio")
        array_radio = data_type_dialog.findChild(QtWidgets.QRadioButton, "array_radio")
        
        # Get references to the different type groups
        primitive_group = data_type_dialog.findChild(QtWidgets.QGroupBox, "primitive_group")
        struct_group = data_type_dialog.findChild(QtWidgets.QGroupBox, "struct_group")
        array_group = data_type_dialog.findChild(QtWidgets.QGroupBox, "array_group")
        
        # Connect radio buttons to show/hide appropriate groups
        if primitive_radio and struct_radio and array_radio:
            if primitive_group:
                primitive_radio.toggled.connect(lambda checked: primitive_group.setVisible(checked))
            
            if struct_group:
                struct_radio.toggled.connect(lambda checked: struct_group.setVisible(checked))
            
            if array_group:
                array_radio.toggled.connect(lambda checked: array_group.setVisible(checked))
                
            # Set default selection if none selected
            if not any([primitive_radio.isChecked(), struct_radio.isChecked(), array_radio.isChecked()]):
                primitive_radio.setChecked(True)
        
        # Handle struct field management
        add_field_button = data_type_dialog.findChild(QtWidgets.QPushButton, "add_field_button")
        if add_field_button:
            add_field_button.clicked.connect(lambda: self.add_struct_field(data_type_dialog))
        
        # Handle array type configuration
        array_configure_button = data_type_dialog.findChild(QtWidgets.QPushButton, "array_configure_button")
        if array_configure_button:
            array_configure_button.clicked.connect(lambda: self.configure_array_type(data_type_dialog))
        
        # Show the dialog
        result = data_type_dialog.exec_()
        
        if result == QtWidgets.QDialog.Accepted:
            # Collect data based on which radio button is selected
            if primitive_radio and primitive_radio.isChecked():
                type_combo = data_type_dialog.findChild(QtWidgets.QComboBox, "type_combo")
                if type_combo:
                    return {"data_type": type_combo.currentText()}
            
            elif struct_radio and struct_radio.isChecked():
                # Collect struct definition
                struct_fields = []
                struct_fields_tree = data_type_dialog.findChild(QtWidgets.QTreeWidget, "struct_fields_tree")
                
                if struct_fields_tree:
                    for i in range(struct_fields_tree.topLevelItemCount()):
                        item = struct_fields_tree.topLevelItem(i)
                        field = {
                            "field_name": item.text(0),
                            "data_type": item.text(1),
                            "description": item.text(2)
                        }
                        struct_fields.append(field)
                
                return {
                    "data_type": "STRUCT",
                    "struct_fields": struct_fields
                }
            
            elif array_radio and array_radio.isChecked():
                # Collect array configuration
                array_type_combo = data_type_dialog.findChild(QtWidgets.QComboBox, "array_type_combo")
                array_size_spin = data_type_dialog.findChild(QtWidgets.QSpinBox, "array_size_spin")
                
                if array_type_combo and array_size_spin:
                    return {
                        "data_type": "ARRAY",
                        "array_element_type": array_type_combo.currentText(),
                        "array_size": array_size_spin.value()
                    }
        
        return None
    
    def add_struct_field(self, parent_dialog):
        """Show dialog to add a struct field"""
        # Load dialog from UI file
        struct_field_dialog = QtWidgets.QDialog(parent_dialog)
        
        # Find the path to the UI file
        ui_file = os.path.join(self.project_path, "Cfg", "LayoutFiles", "Dialogs", "StructFieldDialog.ui")
        
        # Check if the file exists
        if not os.path.exists(ui_file):
            QtWidgets.QMessageBox.warning(self, "Error", f"UI file not found: {ui_file}")
            return
        
        # Load the UI
        uic.loadUi(ui_file, struct_field_dialog)
        
        # Connect basic/array radio buttons
        basic_radio = struct_field_dialog.findChild(QtWidgets.QRadioButton, "basic_radio")
        array_radio = struct_field_dialog.findChild(QtWidgets.QRadioButton, "array_radio")
        array_layout = struct_field_dialog.findChild(QtWidgets.QHBoxLayout, "array_layout")
        
        if basic_radio and array_radio and array_layout:
            # Find array-related widgets
            array_type_label = struct_field_dialog.findChild(QtWidgets.QLabel, "array_type_label")
            array_display = struct_field_dialog.findChild(QtWidgets.QLineEdit, "array_display")
            configure_array_button = struct_field_dialog.findChild(QtWidgets.QPushButton, "configure_array_button")
            
            # Connect visibility based on radio selection
            if array_type_label and array_display and configure_array_button:
                basic_radio.toggled.connect(lambda checked: array_type_label.setVisible(not checked))
                basic_radio.toggled.connect(lambda checked: array_display.setVisible(not checked))
                basic_radio.toggled.connect(lambda checked: configure_array_button.setVisible(not checked))
        
        # Connect configure array button
        configure_array_button = struct_field_dialog.findChild(QtWidgets.QPushButton, "configure_array_button")
        if configure_array_button:
            configure_array_button.clicked.connect(lambda: self.configure_field_array_type(struct_field_dialog))
        
        # Connect dialog buttons
        button_box = struct_field_dialog.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        if button_box:
            button_box.accepted.connect(struct_field_dialog.accept)
            button_box.rejected.connect(struct_field_dialog.reject)
        
        # Show the dialog
        if struct_field_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Get data from the dialog
            name_edit = struct_field_dialog.findChild(QtWidgets.QLineEdit, "name_edit")
            description_edit = struct_field_dialog.findChild(QtWidgets.QLineEdit, "description_edit")
            type_combo = struct_field_dialog.findChild(QtWidgets.QComboBox, "type_combo")
            
            if name_edit and description_edit and type_combo:
                # Get struct fields tree from parent dialog
                struct_fields_tree = parent_dialog.findChild(QtWidgets.QTreeWidget, "struct_fields_tree")
                
                if struct_fields_tree:
                    field_name = name_edit.text().strip()
                    description = description_edit.text().strip()
                    
                    if basic_radio and basic_radio.isChecked():
                        data_type = type_combo.currentText()
                    else:
                        # For array type, use the configured array information
                        array_display = struct_field_dialog.findChild(QtWidgets.QLineEdit, "array_display")
                        if array_display:
                            data_type = f"ARRAY[{array_display.text()}]"
                        else:
                            data_type = "ARRAY"
                    
                    # Add to tree widget
                    item = QtWidgets.QTreeWidgetItem([field_name, data_type, description])
                    struct_fields_tree.addTopLevelItem(item)
    
    def configure_field_array_type(self, parent_dialog):
        """Configure array type for a struct field"""
        # Load dialog from UI file
        array_type_dialog = QtWidgets.QDialog(parent_dialog)
        
        # Find the path to the UI file
        ui_file = os.path.join(self.project_path, "Cfg", "LayoutFiles", "Dialogs", "ArrayTypeDialog.ui")
        
        # Check if the file exists
        if not os.path.exists(ui_file):
            QtWidgets.QMessageBox.warning(self, "Error", f"UI file not found: {ui_file}")
            return
        
        # Load the UI
        uic.loadUi(ui_file, array_type_dialog)
        
        # Connect dialog buttons
        button_box = array_type_dialog.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        if button_box:
            button_box.accepted.connect(array_type_dialog.accept)
            button_box.rejected.connect(array_type_dialog.reject)
        else:
            # If buttonBox not found, look for OK and Cancel buttons individually
            ok_button = array_type_dialog.findChild(QtWidgets.QPushButton, "ok_button")
            cancel_button = array_type_dialog.findChild(QtWidgets.QPushButton, "cancel_button")
            
            if ok_button:
                ok_button.clicked.connect(array_type_dialog.accept)
            if cancel_button:
                cancel_button.clicked.connect(array_type_dialog.reject)
        
        # Show the dialog
        if array_type_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Get data from the dialog
            type_combo = array_type_dialog.findChild(QtWidgets.QComboBox, "type_combo")
            size_spin = array_type_dialog.findChild(QtWidgets.QSpinBox, "size_spin")
            
            if type_combo and size_spin:
                # Update the array display in the parent dialog
                array_display = parent_dialog.findChild(QtWidgets.QLineEdit, "array_display")
                if array_display:
                    array_display.setText(f"{size_spin.value()} of {type_combo.currentText()}")
    
    def configure_array_type(self, parent_dialog):
        """Configure array type"""
        # Load dialog from UI file
        array_type_dialog = QtWidgets.QDialog(parent_dialog)
        
        # Find the path to the UI file
        ui_file = os.path.join(self.project_path, "Cfg", "LayoutFiles", "Dialogs", "ArrayTypeDialog.ui")
        
        # Check if the file exists
        if not os.path.exists(ui_file):
            QtWidgets.QMessageBox.warning(self, "Error", f"UI file not found: {ui_file}")
            return
        
        # Load the UI
        uic.loadUi(ui_file, array_type_dialog)
        
        # Connect dialog buttons
        button_box = array_type_dialog.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        if button_box:
            button_box.accepted.connect(array_type_dialog.accept)
            button_box.rejected.connect(array_type_dialog.reject)
        else:
            # If buttonBox not found, look for OK and Cancel buttons individually
            ok_button = array_type_dialog.findChild(QtWidgets.QPushButton, "ok_button")
            cancel_button = array_type_dialog.findChild(QtWidgets.QPushButton, "cancel_button")
            
            if ok_button:
                ok_button.clicked.connect(array_type_dialog.accept)
            if cancel_button:
                cancel_button.clicked.connect(array_type_dialog.reject)
        
        # Show the dialog
        if array_type_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Get data from the dialog
            type_combo = array_type_dialog.findChild(QtWidgets.QComboBox, "type_combo")
            size_spin = array_type_dialog.findChild(QtWidgets.QSpinBox, "size_spin")
            
            if type_combo and size_spin:
                # Update the parent dialog UI
                array_type_combo = parent_dialog.findChild(QtWidgets.QComboBox, "array_type_combo")
                array_size_spin = parent_dialog.findChild(QtWidgets.QSpinBox, "array_size_spin")
                
                if array_type_combo and array_size_spin:
                    array_type_combo.setCurrentText(type_combo.currentText())
                    array_size_spin.setValue(size_spin.value())
    
    def edit_signal(self):
        """Edit the selected signal"""
        # Find the signal tree
        signal_tree = self.findChild(QTreeWidget, "signalTree")
        if not signal_tree:
            return
        
        # Get the selected signal
        selected_items = signal_tree.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a signal to edit.")
            return
        
        # Get the selected signal ID
        selected_item = selected_items[0]
        signal_id = selected_item.text(0)
        
        # Find the signal in the project data
        signal_data = self.find_signal_by_id(signal_id)
        if not signal_data:
            QtWidgets.QMessageBox.warning(self, "Error", f"Signal with ID {signal_id} not found.")
            return
        
        # Save current state for undo
        if "signals" in self.project_data:
            self.signal_edit_stack.append(self.project_data["signals"].copy())
        
        # Show signal details dialog
        signal_details = SignalDetailsDialog.get_signal_details(self, signal_data)
        if not signal_details:
            return
        
        # Update the signal in the database
        self.update_signal_in_database(signal_id, signal_details)
        
        # Refresh the signal tree
        self.update_signal_tree()
    
    def delete_signal(self):
        """Delete the selected signal"""
        # Find the signal tree
        signal_tree = self.findChild(QTreeWidget, "signalTree")
        if not signal_tree:
            return
        
        # Get the selected signal
        selected_items = signal_tree.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a signal to delete.")
            return
        
        # Get the selected signal ID
        selected_item = selected_items[0]
        signal_id = selected_item.text(0)
        signal_name = selected_item.text(1)
        
        # Confirm deletion
        confirm = QtWidgets.QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete the signal '{signal_name}'?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if confirm == QtWidgets.QMessageBox.Yes:
            # Delete the signal from the database
            self.delete_signal_from_database(signal_id)
            
            # Refresh the signal tree
            self.update_signal_tree()
            
            # Disable the signal details section
            self.set_signal_details_enabled(False)

    def init_ui(self):
        """Initialize UI elements and connect signals."""
        # Initialize empty data structures
        self.project_data = {}
        self.signal_edit_stack = []
        
        # Setup menu operations
        self.menu_ops = MenuOperations(self)
        self.menu_ops.setup()
        
        # Setup file operations
        self.file_ops = FileOperations(self)
        
        # Setup core configuration manager
        self.core_config_manager = CoreConfigManager(self)
        
        # Setup signal database page
        self.setup_signal_database_page()
        
        # Set up cross-references between pages
        self.setup_cross_references()
        
        # Connection for About dialog
        about_action = self.findChild(QAction, "actionAbout")
        if about_action:
            about_action.triggered.connect(self.show_about_dialog)

    def find_signal_by_id(self, signal_id):
        """Find signal by ID in the project data"""
        return self.signal_manager.find_signal_by_id(signal_id)
    
    def generate_signal_id(self):
        """Generate a unique signal ID"""
        return self.signal_manager.generate_signal_id()
    
    def add_signal_to_database(self, signal_data):
        """Add a new signal to the database"""
        return self.signal_manager.add_signal_to_database(signal_data)
    
    def update_signal_in_database(self, signal_id, updated_data):
        """Update existing signal in the database"""
        return self.signal_manager.update_signal_in_database(signal_id, updated_data)
    
    def delete_signal_from_database(self, signal_id):
        """Delete a signal from the database"""
        # Save current state for potential undo before deleting
        if "signals" in self.project_data:
            self.signal_edit_stack.append(self.project_data["signals"].copy())
            
        return self.signal_manager.delete_signal_from_database(signal_id)
    
    def update_signal_tree(self):
        """Update the signal tree with current data"""
        signal_tree = self.findChild(QTreeWidget, "signalTree")
        if signal_tree:
            self.signal_manager.update_signal_tree(signal_tree)
    
    def populate_signal_details(self, signal_data):
        """Populate the signal details section with signal data"""
        # Find all input fields
        var_port_name_input = self.findChild(QLineEdit, "varPortNameInput")
        description_input = self.findChild(QLineEdit, "descriptionInput")
        data_type_combo = self.findChild(QComboBox, "dataTypeCombo")
        init_value_combo = self.findChild(QComboBox, "initValueCombo")
        asil_combo = self.findChild(QComboBox, "asilCombo")
        buffer_count_spin = self.findChild(QSpinBox, "bufferCountSpinBox")
        notifiers_combo = self.findChild(QComboBox, "notifiersCombo")
        sm_buff_count_spin = self.findChild(QSpinBox, "smBuffCountSpinBox")
        timeout_spin = self.findChild(QSpinBox, "timeoutSpinBox")
        periodicity_spin = self.findChild(QSpinBox, "periodicitySpinBox")
        checksum_combo = self.findChild(QComboBox, "checksumCombo")
        
        # Create a form layout for signal details
        signal_details_layout = QFormLayout()
        
        # Find container for signal details
        details_container = self.findChild(QWidget, "signalDetailsContainer")
        if details_container:
            # Clear any existing layout
            if details_container.layout():
                # Remove all items from the layout
                while details_container.layout().count():
                    item = details_container.layout().takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                # Delete the layout
                QWidget().setLayout(details_container.layout())
            
            # Set the new layout
            details_container.setLayout(signal_details_layout)
            
            # Use the SignalManager to populate details
            self.signal_manager.populate_signal_details(self, signal_data, signal_details_layout)
        
        # Populate dynamic attributes
        self.populate_dynamic_attributes(signal_data)
    
    def populate_dynamic_attributes(self, signal_data):
        """Populate dynamic attributes based on core configuration"""
        # Find the dynamic attributes frame
        dynamic_attrs_frame = self.findChild(QFrame, "dynamicAttrsFrame")
        if not dynamic_attrs_frame:
            return
        
        # Clear previous attributes
        layout = dynamic_attrs_frame.layout()
        if layout:
            # Remove all items from the layout
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
        
        # Add core routing information if available
        if "source_core" in signal_data:
            self.add_dynamic_attribute(layout, "Source Core", signal_data["source_core"])
        
        if "destination_cores" in signal_data and isinstance(signal_data["destination_cores"], list):
            cores_str = ", ".join(signal_data["destination_cores"])
            self.add_dynamic_attribute(layout, "Destination Cores", cores_str)
        
        # Add placeholder if no dynamic attributes
        if layout.count() == 0:
            placeholder = QLabel("No dynamic attributes available")
            placeholder.setAlignment(Qt.AlignCenter)
            layout.addWidget(placeholder)
    
    def add_dynamic_attribute(self, layout, label_text, value_text):
        """Add a dynamic attribute to the layout"""
        # Create a form layout for this attribute
        form_layout = QFormLayout()
        
        # Create label and value widgets
        label = QLabel(label_text)
        value = QLineEdit(str(value_text))
        value.setReadOnly(True)
        
        # Add to form layout
        form_layout.addRow(label, value)
        
        # Add the form layout to the main layout
        layout.addLayout(form_layout)
    
    def save_signal(self):
        """Save changes to the current signal"""
        # Find the signal tree
        signal_tree = self.findChild(QTreeWidget, "signalTree")
        if not signal_tree:
            return
        
        # Get the selected signal
        selected_items = signal_tree.selectedItems()
        if not selected_items:
            return
        
        # Get the selected signal ID
        selected_item = selected_items[0]
        signal_id = selected_item.text(0)
        
        # Collect data from form
        signal_data = self.collect_signal_form_data()
        
        # Preserve the ID
        signal_data["id"] = signal_id
        
        # Update the signal in the database
        self.update_signal_in_database(signal_id, signal_data)
        
        # Update the signal name in the tree if it changed
        if "name" in signal_data:
            selected_item.setText(1, signal_data["name"])
        
        # Show success message
        QMessageBox.information(self, "Success", "Signal updated successfully.")
    
    def collect_signal_form_data(self):
        """Collect data from signal details form"""
        # Collect base signal data using SignalManager
        signal_data = self.signal_manager.collect_signal_form_data(self)
        
        # Add any additional signal-specific data collection here
        # Find all input fields
        var_port_name_input = self.findChild(QLineEdit, "varPortNameInput")
        description_input = self.findChild(QLineEdit, "descriptionInput")
        data_type_combo = self.findChild(QComboBox, "dataTypeCombo")
        init_value_combo = self.findChild(QComboBox, "initValueCombo")
        asil_combo = self.findChild(QComboBox, "asilCombo")
        buffer_count_spin = self.findChild(QSpinBox, "bufferCountSpinBox")
        notifiers_combo = self.findChild(QComboBox, "notifiersCombo")
        sm_buff_count_spin = self.findChild(QSpinBox, "smBuffCountSpinBox")
        timeout_spin = self.findChild(QSpinBox, "timeoutSpinBox")
        periodicity_spin = self.findChild(QSpinBox, "periodicitySpinBox")
        checksum_combo = self.findChild(QComboBox, "checksumCombo")
        
        # Collect data from each field
        if var_port_name_input:
            signal_data["name"] = var_port_name_input.text().strip()
        
        if description_input:
            signal_data["description"] = description_input.text().strip()
        
        if data_type_combo:
            signal_data["data_type"] = data_type_combo.currentText()
        
        if init_value_combo:
            signal_data["init_value_type"] = init_value_combo.currentText()
        
        if asil_combo:
            signal_data["asil"] = asil_combo.currentText()
        
        if buffer_count_spin:
            signal_data["buffer_count"] = buffer_count_spin.value()
        
        if notifiers_combo:
            signal_data["notifiers"] = notifiers_combo.currentText() == "True"
        
        if sm_buff_count_spin:
            signal_data["sm_buff_count"] = sm_buff_count_spin.value()
        
        if timeout_spin:
            signal_data["timeout"] = timeout_spin.value()
        
        if periodicity_spin:
            signal_data["periodicity"] = periodicity_spin.value()
        
        if checksum_combo:
            signal_data["checksum"] = checksum_combo.currentText()
        
        return signal_data
    
    def cancel_signal_edit(self):
        """Cancel editing the signal"""
        # Find the signal tree
        signal_tree = self.findChild(QTreeWidget, "signalTree")
        if not signal_tree:
            return
        
        # Get the selected signal
        selected_items = signal_tree.selectedItems()
        if not selected_items:
            # If no signal is selected, just disable the form
            self.set_signal_details_enabled(False)
            return
        
        # Get the selected signal ID
        selected_item = selected_items[0]
        signal_id = selected_item.text(0)
        
        # Re-populate form with original signal data
        signal_data = self.find_signal_by_id(signal_id)
        if signal_data:
            self.populate_signal_details(signal_data)
        else:
            # If signal not found, disable the form
            self.set_signal_details_enabled(False)

    def setup_cross_references(self):
        """Set up cross-references between different pages"""
        # Find the core configuration button on the signal database page
        core_config_btn = self.findChild(QPushButton, "coreConfigButton")
        
        if core_config_btn:
            # Connect to a function that switches to the core configuration page
            core_config_btn.clicked.connect(self.switch_to_core_config)
        
        # Find the signal database button on the core configuration page
        signal_db_btn = self.findChild(QPushButton, "signalDatabaseButton")
        
        if signal_db_btn:
            # Connect to a function that switches to the signal database page
            signal_db_btn.clicked.connect(self.switch_to_signal_database)
    
    def switch_to_core_config(self):
        """Switch to the core configuration page"""
        # Find the navigation buttons
        nav_button1 = self.findChild(QPushButton, "navButton1")
        
        if nav_button1:
            # Click the core configuration tab
            nav_button1.click()
    
    def switch_to_signal_database(self):
        """Switch to the signal database page"""
        # Find the navigation buttons
        nav_button2 = self.findChild(QPushButton, "navButton2")
        
        if nav_button2:
            # Click the signal database tab
            nav_button2.click()

    def set_project_modified(self, modified=True):
        """Set the project modified state and update UI accordingly"""
        self.project_modified = modified
        
        # Update window title
        self.update_window_title()
        
        # Update save actions
        save_action = self.findChild(QAction, "actionSave")
        save_as_action = self.findChild(QAction, "actionSave_As")
        
        if save_action:
            save_action.setEnabled(modified)
        
        if save_as_action:
            save_as_action.setEnabled(True)  # Always allow Save As