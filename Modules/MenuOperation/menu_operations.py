#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Menu Operations Module for Signal Manager
Handles menu-related operations and actions
"""

from PyQt5.QtWidgets import QAction, QMenu, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
import os
from Utils.path_utils import get_resource_path

class MenuOperations:
    """Handles menu operations for the Signal Manager application"""
    
    def __init__(self, main_window):
        """
        Initialize MenuOperations
        
        Args:
            main_window: The main application window
        """
        self.main_window = main_window

    def setup(self):
        """
        Set up all menus for the application
        
        This method should be called once during application initialization
        to create and configure all menus.
        """
        # Find the menubar
        menubar = self.main_window.menuBar
        if not menubar:
            print("Warning: MenuBar not found in main window")
            return
            
        # Create each menu
        self.create_file_menu(menubar)
        self.create_edit_menu(menubar)
        self.create_code_generator_menu(menubar)
        self.create_help_menu(menubar)
        
        # Connect code generator actions if not already connected
        self.connect_code_generator_actions()
        
    def connect_code_generator_actions(self):
        """Connect actions for the Code Generator menu"""
        # Find code generator actions
        signal_mgr_action = self.main_window.findChild(QAction, "actionSignalMgr")
        ipc_manager_action = self.main_window.findChild(QAction, "actionIpcManager")
        ipc_ov_eth_mgr_action = self.main_window.findChild(QAction, "actionIpcOvEthMgr")
        
        # Connect to handler methods if they exist
        if signal_mgr_action and hasattr(self.main_window, "on_signal_mgr_generator"):
            signal_mgr_action.triggered.connect(self.main_window.on_signal_mgr_generator)
            
        if ipc_manager_action and hasattr(self.main_window, "on_ipc_manager_generator"):
            ipc_manager_action.triggered.connect(self.main_window.on_ipc_manager_generator)
            
        if ipc_ov_eth_mgr_action and hasattr(self.main_window, "on_ipc_ov_eth_mgr_generator"):
            ipc_ov_eth_mgr_action.triggered.connect(self.main_window.on_ipc_ov_eth_mgr_generator)
    
    def create_file_menu(self, menubar):
        """
        Create the File menu
        
        Args:
            menubar: The menu bar to add the File menu to
            
        Returns:
            QMenu: The created File menu
        """
        file_menu = menubar.addMenu("File")
        
        # New action
        new_action = QAction(QIcon(get_resource_path('Cfg\\Resources\\icons\\NewFile.png')), "New", self.main_window)
        new_action.setShortcut("Ctrl+N")
        new_action.setStatusTip("Create a new signal configuration")
        new_action.triggered.connect(self.main_window.on_new)
        file_menu.addAction(new_action)
        
        # Open action
        open_action = QAction(QIcon(get_resource_path('Cfg\\Resources\\icons\\OpenFile.png')), "Open", self.main_window)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open an existing signal configuration")
        open_action.triggered.connect(self.main_window.on_open)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        # Save action
        save_action = QAction(QIcon(get_resource_path('Cfg\\Resources\\icons\\Save.png')), "Save", self.main_window)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Save the current signal configuration")
        save_action.triggered.connect(self.main_window.on_save)
        file_menu.addAction(save_action)
        
        # Save As action
        save_as_action = QAction(QIcon(get_resource_path('Cfg\\Resources\\icons\\SaveAs.png')), "Save As", self.main_window)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.setStatusTip("Save the current signal configuration with a new name")
        save_as_action.triggered.connect(self.main_window.on_save_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Export to Excel action
        export_action = QAction(QIcon(get_resource_path('Cfg\\Resources\\icons\\ExportToExcel.png')), "Export To Excel", self.main_window)
        export_action.setStatusTip("Export the current configuration to Excel")
        export_action.triggered.connect(self.main_window.on_export_to_excel)
        file_menu.addAction(export_action)
        
        # Import from Excel action
        import_action = QAction(QIcon(get_resource_path('Cfg\\Resources\\icons\\Import.png')), "Import From Excel", self.main_window)
        import_action.setStatusTip("Import configuration from Excel")
        import_action.triggered.connect(self.main_window.on_import_from_excel)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        # Close action
        close_action = QAction(QIcon(get_resource_path('Cfg\\Resources\\icons\\Close.png')), "Close", self.main_window)
        close_action.setShortcut("Ctrl+W")
        close_action.setStatusTip("Close the current configuration")
        close_action.triggered.connect(self.main_window.on_close)
        file_menu.addAction(close_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction(QIcon(get_resource_path('Cfg\\Resources\\icons\\Exit.png')), "Exit", self.main_window)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.main_window.close)
        file_menu.addAction(exit_action)
        
        return file_menu
    
    def create_edit_menu(self, menubar):
        """
        Create the Edit menu
        
        Args:
            menubar: The menu bar to add the Edit menu to
            
        Returns:
            QMenu: The created Edit menu
        """
        edit_menu = menubar.addMenu("Edit")
        
        # Add Entry action
        add_action = QAction(QIcon(get_resource_path('Cfg\\Resources\\icons\\NewAdd.png')), "Add Entry", self.main_window)
        add_action.setShortcut("Ctrl+A")
        add_action.setStatusTip("Add a new signal entry")
        add_action.triggered.connect(self.main_window.on_add_entry)
        edit_menu.addAction(add_action)
        
        # Delete Entry action
        delete_action = QAction(QIcon(get_resource_path('Cfg\\Resources\\icons\\NewDelete.png')), "Delete Entry", self.main_window)
        delete_action.setShortcut("Delete")
        delete_action.setStatusTip("Delete the selected signal entry")
        delete_action.triggered.connect(self.main_window.on_delete_entry)
        edit_menu.addAction(delete_action)
        
        edit_menu.addSeparator()
        
        # Update Entry action
        update_action = QAction(QIcon(get_resource_path('Cfg\\Resources\\icons\\UpdateEntry.png')), "Update Entry", self.main_window)
        update_action.setShortcut("Ctrl+U")
        update_action.setStatusTip("Update the selected signal entry")
        update_action.triggered.connect(self.main_window.on_update_entry)
        edit_menu.addAction(update_action)
        
        return edit_menu
    
    def create_code_generator_menu(self, menubar):
        """
        Create the Code Generator menu
        
        Args:
            menubar: The menu bar to add the Code Generator menu to
            
        Returns:
            QMenu: The created Code Generator menu
        """
        code_generator_menu = menubar.addMenu("Code Generator")
        
        # SignalMgr action
        signal_mgr_action = QAction("SignalMgr", self.main_window)
        signal_mgr_action.setStatusTip("Generate SignalMgr code")
        code_generator_menu.addAction(signal_mgr_action)
        
        # IpcManager action
        ipc_manager_action = QAction("IpcManager", self.main_window)
        ipc_manager_action.setStatusTip("Generate IpcManager code")
        code_generator_menu.addAction(ipc_manager_action)
        
        # IpcOvEthMgr action
        ipc_ov_eth_mgr_action = QAction("IpcOvEthMgr", self.main_window)
        ipc_ov_eth_mgr_action.setStatusTip("Generate IpcOvEthMgr code")
        code_generator_menu.addAction(ipc_ov_eth_mgr_action)
        
        return code_generator_menu
    
    def create_help_menu(self, menubar):
        """
        Create the Help menu
        
        Args:
            menubar: The menu bar to add the Help menu to
            
        Returns:
            QMenu: The created Help menu
        """
        help_menu = menubar.addMenu("Help")
        
        # About Tool action
        about_action = QAction("About Tool", self.main_window)
        about_action.setStatusTip("Show information about the Signal Manager tool")
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
        # License action
        license_action = QAction("License", self.main_window)
        license_action.setStatusTip("Show license information")
        license_action.triggered.connect(self.show_license_dialog)
        help_menu.addAction(license_action)
        
        return help_menu
    
    def show_about_dialog(self):
        """Show the About dialog"""
        QMessageBox.about(
            self.main_window,
            "About Signal Manager",
            """<b>Signal Manager</b> v1.0.0<br>
            <br>
            A modern PyQt5-based application for signal data management with dark theme.<br>
            <br>
            &copy; 2023 Your Organization"""
        )
    
    def show_license_dialog(self):
        """Show the License dialog"""
        QMessageBox.about(
            self.main_window,
            "License",
            """<b>Signal Manager</b> is licensed under the terms of the MIT License.<br>
            <br>
            Permission is hereby granted, free of charge, to any person obtaining a copy
            of this software and associated documentation files, to deal
            in the Software without restriction, including without limitation the rights
            to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
            copies of the Software, and to permit persons to whom the Software is
            furnished to do so, subject to the following conditions:<br>
            <br>
            The above copyright notice and this permission notice shall be included in all
            copies or substantial portions of the Software."""
        )