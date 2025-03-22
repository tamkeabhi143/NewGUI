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
                            QTableWidgetItem)
from PyQt5.QtCore import Qt, QSize, QDateTime, QSettings, pyqtSignal, QEvent
from PyQt5.QtGui import QIcon, QColor, QResizeEvent, QCloseEvent, QPixmap

# Import modules
from Modules.FileOperation.file_operations import FileOperations

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
        
        # Set up UI
        self.setup_ui()
        
        # Connect signals and slots
        self.connect_signals_slots()
        
        # Load settings
        self.load_settings()
        
        # Update window title
        self.update_window_title()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Set window properties
        self.setWindowTitle("Signal Manager")
        self.setMinimumSize(1000, 700)
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setCentralWidget(self.central_widget)
        
        # Set up the sidebar navigation
        self.setup_sidebar()
        
        # Create content stack
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("contentStack")
        
        # Create content pages
        self.setup_core_config_page()
        self.setup_project_config_page()
        self.setup_signal_database_page()
        self.setup_code_generator_page()
        self.setup_settings_page()
        
        # Add content stack to main layout
        self.main_layout.addWidget(self.content_stack)
        
        # Set up the menu bar
        self.setup_menu_bar()
        
        # Set up the tool bar
        self.setup_tool_bar()
        
        # Set up the status bar
        self.statusBar().showMessage("Ready")
    
    def setup_sidebar(self):
        """Set up the sidebar navigation"""
        # Create sidebar widget
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setObjectName("sidebarWidget")
        self.sidebar_widget.setFixedWidth(220)
        
        # Create sidebar layout
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)
        self.sidebar_layout.setSpacing(5)
        
        # App title
        self.title_label = QLabel("Signal Manager")
        self.title_label.setObjectName("appTitle")
        self.sidebar_layout.addWidget(self.title_label)
        
        # Navigation buttons
        self.nav_buttons = []
        nav_items = [
            "Core Configuration", 
            "Project Config", 
            "Signal Database", 
            "Code Generator", 
            "Settings"
        ]
        
        for i, item in enumerate(nav_items):
            nav_button = QPushButton(item)
            nav_button.setCheckable(True)
            nav_button.setObjectName(f"navButton{i}")
            
            # Connect button click to page change
            nav_button.clicked.connect(lambda checked, idx=i: self.set_active_page(idx))
            
            self.sidebar_layout.addWidget(nav_button)
            self.nav_buttons.append(nav_button)
        
        # Set the first button as active by default
        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)
        
        # Add spacer to push profile to bottom
        self.sidebar_layout.addStretch()
        
        # Add user profile section
        profile_layout = QHBoxLayout()
        
        profile_icon = QLabel()
        profile_icon.setFixedSize(32, 32)
        profile_icon.setObjectName("profileIcon")
        
        profile_name = QLabel("User Profile")
        profile_name.setObjectName("profileName")
        
        profile_layout.addWidget(profile_icon)
        profile_layout.addWidget(profile_name)
        profile_layout.addStretch()
        
        self.sidebar_layout.addLayout(profile_layout)
        
        # Add sidebar to main layout
        self.main_layout.addWidget(self.sidebar_widget)
    
    def create_card(self, title=""):
        """Create a styled card frame with title"""
        card = QFrame()
        card.setObjectName("card")
        
        # Create shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 2)
        card.setGraphicsEffect(shadow)
        
        # Create layout for card
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        
        # Add title if provided
        if title:
            title_layout = QHBoxLayout()
            
            title_label = QLabel(title)
            title_label.setObjectName("cardTitle")
            title_layout.addWidget(title_label)
            title_layout.addStretch()
            
            card_layout.addLayout(title_layout)
            
            # Add separator line
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setObjectName("cardDivider")
            
            card_layout.addWidget(line)
            card_layout.addSpacing(10)
        
        return card, card_layout
    
    def setup_core_config_page(self):
        """Set up the Core Configuration page"""
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(20, 20, 20, 20)
        page_layout.setSpacing(20)
        
        # Top bar with search and actions
        top_bar_layout = QHBoxLayout()
        
        # Search field
        search_field = QLineEdit()
        search_field.setPlaceholderText("Search configurations...")
        search_field.setFixedHeight(36)
        
        # Action buttons
        new_button = QPushButton("New")
        new_button.setIcon(QIcon(os.path.join("Cfg", "Resources", "icons", "new.png")))
        
        import_button = QPushButton("Import")
        import_button.setIcon(QIcon(os.path.join("Cfg", "Resources", "icons", "import.png")))
        
        top_bar_layout.addWidget(search_field)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(new_button)
        top_bar_layout.addWidget(import_button)
        
        page_layout.addLayout(top_bar_layout)
        
        # Content cards layout
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        # Core Info Card
        core_info_card, core_info_layout = self.create_card("SOC Core Information")
        
        # Add form fields
        core_form = QFormLayout()
        core_form.setSpacing(15)
        
        core_id_field = QLineEdit()
        version_field = QLineEdit()
        config_type_combo = QComboBox()
        config_type_combo.addItems(["Standard", "Extended", "Custom"])
        
        core_form.addRow("Core ID:", core_id_field)
        core_form.addRow("Version:", version_field)
        core_form.addRow("Configuration Type:", config_type_combo)
        
        core_info_layout.addLayout(core_form)
        cards_layout.addWidget(core_info_card)
        
        # Version Details Card
        version_card, version_layout = self.create_card("Version Details")
        
        version_form = QFormLayout()
        version_form.setSpacing(15)
        
        version_number_field = QLineEdit()
        version_date_field = QDateTimeEdit(QDateTime.currentDateTime())
        updated_by_field = QLineEdit()
        change_desc_field = QPlainTextEdit()
        change_desc_field.setMaximumHeight(80)
        
        version_form.addRow("Version Number:", version_number_field)
        version_form.addRow("Date:", version_date_field)
        version_form.addRow("Updated By:", updated_by_field)
        version_form.addRow("Change Description:", change_desc_field)
        
        version_layout.addLayout(version_form)
        cards_layout.addWidget(version_card)
        
        page_layout.addLayout(cards_layout, 1)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(0, 10, 0, 0)
        
        update_button = QPushButton("Update Configuration")
        update_button.setMinimumWidth(150)
        
        reset_button = QPushButton("Reset")
        reset_button.setMinimumWidth(150)
        reset_button.setProperty("class", "secondary")
        
        action_layout.addStretch()
        action_layout.addWidget(update_button)
        action_layout.addWidget(reset_button)
        action_layout.addStretch()
        
        page_layout.addLayout(action_layout)
        
        # Status table
        status_card, status_layout = self.create_card("Configuration Status")
        
        status_table = QTableWidget(4, 5)
        status_table.setHorizontalHeaderLabels(["ID", "Name", "Status", "Last Updated", "Actions"])
        status_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        status_table.verticalHeader().setVisible(False)
        status_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        status_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        status_table.setAlternatingRowColors(True)
        
        # Sample data for the table
        sample_data = [
            {"id": "001", "name": "Core Configuration A", "status": "Active", "date": "2023-10-15"},
            {"id": "002", "name": "Core Configuration B", "status": "Inactive", "date": "2023-09-20"},
            {"id": "003", "name": "Core Configuration C", "status": "Draft", "date": "2023-10-05"},
            {"id": "004", "name": "Core Configuration D", "status": "Active", "date": "2023-10-12"},
        ]
        
        # Add data to the table
        for row, item in enumerate(sample_data):
            # ID
            status_table.setItem(row, 0, QTableWidgetItem(item["id"]))
            # Name
            status_table.setItem(row, 1, QTableWidgetItem(item["name"]))
            
            # Status (with custom widget and styling)
            status_widget = QWidget()
            status_layout_cell = QHBoxLayout(status_widget)
            status_layout_cell.setContentsMargins(5, 2, 5, 2)
            status_layout_cell.setAlignment(Qt.AlignCenter)
            
            status_label = QLabel(item["status"])
            status_label.setAlignment(Qt.AlignCenter)
            
            # Style based on status
            status_class = "StatusActive" if item["status"] == "Active" else \
                          "StatusInactive" if item["status"] == "Inactive" else \
                          "StatusDraft"
            status_label.setProperty("class", status_class)
            
            status_layout_cell.addWidget(status_label)
            status_table.setCellWidget(row, 2, status_widget)
            
            # Date
            status_table.setItem(row, 3, QTableWidgetItem(item["date"]))
            
            # Actions (with button widgets)
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_layout.setAlignment(Qt.AlignCenter)
            
            edit_button = QPushButton()
            edit_button.setIcon(QIcon(os.path.join("Cfg", "Resources", "icons", "edit.png")))
            edit_button.setFixedSize(24, 24)
            edit_button.setProperty("class", "editButton")
            
            delete_button = QPushButton()
            delete_button.setIcon(QIcon(os.path.join("Cfg", "Resources", "icons", "delete.png")))
            delete_button.setFixedSize(24, 24)
            delete_button.setProperty("class", "deleteButton")
            
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            
            status_table.setCellWidget(row, 4, actions_widget)
        
        status_layout.addWidget(status_table)
        page_layout.addWidget(status_card, 2)
        
        # Add floating action button
        fab_button = QPushButton("+")
        fab_button.setObjectName("fabButton")
        fab_button.setFixedSize(56, 56)
        
        # Set up position attributes for fab_button
        fab_button._parent_widget = page
        
        # Position FAB at bottom right of the page
        self.position_fab(fab_button, page)
        
        # Connect FAB to add entry action
        fab_button.clicked.connect(self.on_add_entry)
        
        # Add page to stack
        self.content_stack.addWidget(page)
    
    def setup_project_config_page(self):
        """Set up the Project Configuration page"""
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(20, 20, 20, 20)
        
        # Page header
        page_label = QLabel("Project Configuration")
        page_label.setObjectName("pageTitle")
        page_layout.addWidget(page_label)
        
        # API Configuration Card
        api_card, api_layout = self.create_card("API Configuration")
        
        # API Form placeholder
        api_layout.addWidget(QLabel("API configuration settings will be shown here"))
        
        # Path Configuration Card
        path_card, path_layout = self.create_card("Path Configuration")
        
        # Output path
        output_path_layout = QHBoxLayout()
        output_path_label = QLabel("Choose Output Directory:")
        output_path_line_edit = QLineEdit()
        output_path_button = QPushButton("Browse...")
        
        output_path_layout.addWidget(output_path_label)
        output_path_layout.addWidget(output_path_line_edit, 1)
        output_path_layout.addWidget(output_path_button)
        
        # Script path
        script_path_layout = QHBoxLayout()
        script_path_label = QLabel("Choose Scripts Directory:")
        script_path_line_edit = QLineEdit()
        script_path_button = QPushButton("Browse...")
        
        script_path_layout.addWidget(script_path_label)
        script_path_layout.addWidget(script_path_line_edit, 1)
        script_path_layout.addWidget(script_path_button)
        
        path_layout.addLayout(output_path_layout)
        path_layout.addLayout(script_path_layout)
        
        # Add cards to layout
        page_layout.addWidget(api_card)
        page_layout.addWidget(path_card)
        page_layout.addStretch()
        
        # Add page to stack
        self.content_stack.addWidget(page)
    
    def setup_signal_database_page(self):
        """Set up the Signal Database page"""
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(20, 20, 20, 20)
        
        # Signal Database Layout
        signal_db_layout = QHBoxLayout()
        
        # Signal Entry Frame
        signal_entry_card, signal_entry_layout = self.create_card("Signal Names")
        signal_entry_card.setMinimumWidth(400)
        signal_entry_layout.addWidget(QLabel("Signal list will appear here"))
        
        # Signal Details Frame
        signal_details_card, signal_details_layout = self.create_card("Signal Details")
        signal_details_card.setMinimumWidth(400)
        signal_details_layout.addWidget(QLabel("Signal details will appear here"))
        
        # Add frames to layout
        signal_db_layout.addWidget(signal_entry_card)
        signal_db_layout.addWidget(signal_details_card)
        page_layout.addLayout(signal_db_layout, 1)
        
        # Board selector layout
        selector_layout = QHBoxLayout()
        
        board_list_combo = QComboBox()
        board_list_combo.setMinimumWidth(200)
        board_list_combo.addItems(["Board 1", "Board 2", "Board 3"])
        
        soc_list_combo = QComboBox()
        soc_list_combo.setMinimumWidth(200)
        soc_list_combo.addItems(["SOC 1", "SOC 2", "SOC 3"])
        
        build_image_combo = QComboBox()
        build_image_combo.setMinimumWidth(200)
        build_image_combo.addItems(["Build Image 1", "Build Image 2", "Build Image 3"])
        
        selector_layout.addWidget(board_list_combo)
        selector_layout.addStretch()
        selector_layout.addWidget(soc_list_combo)
        selector_layout.addStretch()
        selector_layout.addWidget(build_image_combo)
        
        page_layout.addLayout(selector_layout)
        
        # Add page to stack
        self.content_stack.addWidget(page)
    
    def setup_code_generator_page(self):
        """Set up the Code Generator page"""
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(20, 20, 20, 20)
        
        page_label = QLabel("Code Generator")
        page_label.setObjectName("pageTitle")
        page_layout.addWidget(page_label)
        
        # Code Generator options
        generator_card, generator_layout = self.create_card("Generator Options")
        
        generator_type_combo = QComboBox()
        generator_type_combo.addItems(["SignalMgr", "IpcManager", "IpcOvEthMgr"])
        
        generator_form = QFormLayout()
        generator_form.addRow("Generator Type:", generator_type_combo)
        
        output_path_line_edit = QLineEdit()
        browse_button = QPushButton("Browse...")
        path_layout = QHBoxLayout()
        path_layout.addWidget(output_path_line_edit)
        path_layout.addWidget(browse_button)
        
        generator_form.addRow("Output Path:", path_layout)
        
        generator_layout.addLayout(generator_form)
        
        # Generate Button
        generate_button = QPushButton("Generate Code")
        generate_button.setMinimumWidth(200)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(generate_button)
        button_layout.addStretch()
        
        # Add to main layout
        page_layout.addWidget(generator_card)
        page_layout.addLayout(button_layout)
        page_layout.addStretch()
        
        # Add page to stack
        self.content_stack.addWidget(page)
    
    def setup_settings_page(self):
        """Set up the Settings page"""
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(20, 20, 20, 20)
        
        page_label = QLabel("Settings")
        page_label.setObjectName("pageTitle")
        page_layout.addWidget(page_label)
        
        # Appearance settings
        appearance_card, appearance_layout = self.create_card("Appearance")
        
        dark_mode_checkbox = QCheckBox("Dark Mode")
        dark_mode_checkbox.setChecked(True)
        
        appearance_layout.addWidget(dark_mode_checkbox)
        
        # Default paths
        default_paths_card, paths_layout = self.create_card("Default Paths")
        
        paths_form = QFormLayout()
        
        project_path_line_edit = QLineEdit()
        project_path_button = QPushButton("Browse...")
        project_path_layout = QHBoxLayout()
        project_path_layout.addWidget(project_path_line_edit)
        project_path_layout.addWidget(project_path_button)
        
        output_path_line_edit = QLineEdit()
        output_path_button = QPushButton("Browse...")
        output_path_layout = QHBoxLayout()
        output_path_layout.addWidget(output_path_line_edit)
        output_path_layout.addWidget(output_path_button)
        
        paths_form.addRow("Default Project Path:", project_path_layout)
        paths_form.addRow("Default Output Path:", output_path_layout)
        
        paths_layout.addLayout(paths_form)
        
        # Save settings button
        save_button = QPushButton("Save Settings")
        
        # Add to layout
        page_layout.addWidget(appearance_card)
        page_layout.addWidget(default_paths_card)
        page_layout.addStretch()
        page_layout.addWidget(save_button, 0, Qt.AlignCenter)
        
        # Add page to stack
        self.content_stack.addWidget(page)
    
    def setup_menu_bar(self):
        """Set up the application menu bar"""
        # File Menu
        file_menu = self.menuBar().addMenu("File")
        
        self.action_new = file_menu.addAction("New")
        self.action_new.triggered.connect(self.on_new)
        
        self.action_open = file_menu.addAction("Open")
        self.action_open.triggered.connect(self.on_open)
        
        file_menu.addSeparator()
        
        self.action_save = file_menu.addAction("Save")
        self.action_save.triggered.connect(self.on_save)
        
        self.action_save_as = file_menu.addAction("Save As")
        self.action_save_as.triggered.connect(self.on_save_as)
        
        file_menu.addSeparator()
        
        self.action_export_to_excel = file_menu.addAction("Export To Excel")
        self.action_export_to_excel.triggered.connect(self.on_export_to_excel)
        
        self.action_import_from_excel = file_menu.addAction("Import From Excel")
        self.action_import_from_excel.triggered.connect(self.on_import_from_excel)
        
        file_menu.addSeparator()
        
        self.action_close = file_menu.addAction("Close")
        self.action_close.triggered.connect(self.on_close)
        
        file_menu.addSeparator()
        
        self.action_exit = file_menu.addAction("Exit")
        self.action_exit.triggered.connect(self.close)
        
        # Edit Menu
        edit_menu = self.menuBar().addMenu("Edit")
        
        self.action_add_entry = edit_menu.addAction("Add Entry")
        self.action_add_entry.triggered.connect(self.on_add_entry)
        
        self.action_delete_entry = edit_menu.addAction("Delete Entry")
        self.action_delete_entry.triggered.connect(self.on_delete_entry)
        
        edit_menu.addSeparator()
        
        self.action_update_entry = edit_menu.addAction("Update Entry")
        self.action_update_entry.triggered.connect(self.on_update_entry)
        
        # Code Generator Menu
        code_generator_menu = self.menuBar().addMenu("Code Generator")
        
        self.action_signal_mgr = code_generator_menu.addAction("SignalMgr")
        self.action_ipc_manager = code_generator_menu.addAction("IpcManager")
        self.action_ipc_ov_eth_mgr = code_generator_menu.addAction("IpcOvEthMgr")
        
        # Help Menu
        help_menu = self.menuBar().addMenu("Help")
        
        self.action_about_tool = help_menu.addAction("About Tool")
        self.action_license = help_menu.addAction("License")
    
    def setup_tool_bar(self):
        """Set up the application tool bar"""
        tool_bar = self.addToolBar("Main")
        
        # Add common actions to toolbar
        tool_bar.addAction(self.action_new)
        tool_bar.addAction(self.action_open)
        tool_bar.addSeparator()
        tool_bar.addAction(self.action_save)
        tool_bar.addAction(self.action_save_as)
        tool_bar.addSeparator()
        tool_bar.addAction(self.action_export_to_excel)
        tool_bar.addAction(self.action_import_from_excel)
        tool_bar.addSeparator()
        tool_bar.addAction(self.action_add_entry)
        tool_bar.addAction(self.action_delete_entry)
        tool_bar.addAction(self.action_update_entry)
    
    def set_active_page(self, index):
        """Set the active page in the content stack"""
        # Update button states
        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)
        
        # Switch page in stack
        self.content_stack.setCurrentIndex(index)
    
    def position_fab(self, fab_button, parent_widget):
        """Position the floating action button in the bottom-right corner"""
        if hasattr(parent_widget, 'width') and hasattr(parent_widget, 'height'):
            fab_button.setParent(parent_widget)
            fab_button.move(parent_widget.width() - 76, parent_widget.height() - 76)
    
    def resizeEvent(self, event):
        """Handle resize events for the main window"""
        super().resizeEvent(event)
        
        # Find all floating action buttons and reposition them
        for page_idx in range(self.content_stack.count()):
            page = self.content_stack.widget(page_idx)
            for child in page.findChildren(QPushButton):
                if child.objectName() == "fabButton" and hasattr(child, "_parent_widget"):
                    self.position_fab(child, child._parent_widget)
        
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
        # Connect any additional signals and slots here
        pass
    
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
            self.on_save_as()
        else:
            self.save_project(self.current_file_path)
    
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
            self.save_project(file_path)
    
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
            else:
                QMessageBox.warning(self, "Export Failed", f"Failed to export data to {file_path}")
    
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
            else:
                QMessageBox.warning(self, "Import Failed", f"Failed to import data from {file_path}")
    
    def on_close(self):
        """Close the current project"""
        if self.maybe_save():
            self.new_project()
    
    # Edit menu actions
    def on_add_entry(self):
        """Add a new entry to the project"""
        QMessageBox.information(self, "Add Entry", "Add Entry functionality to be implemented")
    
    def on_delete_entry(self):
        """Delete an entry from the project"""
        QMessageBox.information(self, "Delete Entry", "Delete Entry functionality to be implemented")
    
    def on_update_entry(self):
        """Update an existing entry"""
        QMessageBox.information(self, "Update Entry", "Update Entry functionality to be implemented")
    
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
            
            QMessageBox.information(self, "Save Successful", f"Project was successfully saved to {file_path}")
            return True
        else:
            QMessageBox.warning(self, "Save Failed", f"Failed to save project to {file_path}")
            return False
    
    def update_data_from_ui(self):
        """Update project data from UI elements"""
        # TODO: Collect data from UI and update project_data
        # Mark as having unsaved changes
        self.has_unsaved_changes = True
        self.update_window_title()
    
    def update_ui_from_data(self):
        """Update UI elements from project data"""
        # TODO: Update UI with data from project_data
        pass
    
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
            return self.on_save(), True
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
        
        # Other settings can be loaded here
    
    def save_settings(self):
        """Save application settings"""
        settings = QSettings("YourOrganization", "SignalManager")
        
        # Window geometry
        settings.setValue("geometry", self.saveGeometry())
        
        # Window state
        settings.setValue("windowState", self.saveState())
        
        # Other settings can be saved here