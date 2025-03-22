#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialog Integration Module
Shows how to integrate and use all the Signal Manager dialogs
"""

from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QVBoxLayout, 
                           QHBoxLayout, QWidget, QLabel, QGridLayout)
from PyQt5.QtCore import Qt

# Import all dialog classes
from Cfg.Dialogs.signal_details_dialog import SignalDetailsDialog
from Cfg.Dialogs.struct_field_dialog import StructFieldDialog
from Cfg.Dialogs.array_type_dialog import ArrayTypeDialog
from Cfg.Dialogs.data_type_selection_dialog import DataTypeSelectionDialog
from Cfg.Dialogs.core_properties_dialog import CorePropertiesDialog
from Cfg.Dialogs.core_config_manager import CoreConfigManager

class DialogIntegrationDemo(QMainWindow):
    """Dialog integration demo for Signal Manager"""
    
    def __init__(self):
        super(DialogIntegrationDemo, self).__init__()
        
        self.setWindowTitle("Signal Manager Dialog Demo")
        self.resize(800, 500)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create title
        title_label = QLabel("Signal Manager Dialog Demo")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        main_layout.addWidget(title_label)
        
        # Create a grid layout for dialog buttons
        grid_layout = QGridLayout()
        
        # Create buttons for each dialog
        self.signal_details_button = QPushButton("Signal Details Dialog")
        self.signal_details_button.clicked.connect(self.show_signal_details_dialog)
        grid_layout.addWidget(self.signal_details_button, 0, 0)
        
        self.struct_field_button = QPushButton("Structure Field Dialog")
        self.struct_field_button.clicked.connect(self.show_struct_field_dialog)
        grid_layout.addWidget(self.struct_field_button, 0, 1)
        
        self.array_type_button = QPushButton("Array Type Dialog")
        self.array_type_button.clicked.connect(self.show_array_type_dialog)
        grid_layout.addWidget(self.array_type_button, 0, 2)
        
        self.data_type_button = QPushButton("Data Type Selection Dialog")
        self.data_type_button.clicked.connect(self.show_data_type_dialog)
        grid_layout.addWidget(self.data_type_button, 1, 0)
        
        self.core_properties_button = QPushButton("Core Properties Dialog")
        self.core_properties_button.clicked.connect(self.show_core_properties_dialog)
        grid_layout.addWidget(self.core_properties_button, 1, 1)
        
        self.core_config_button = QPushButton("Core Configuration Manager")
        self.core_config_button.clicked.connect(self.show_core_config_manager)
        grid_layout.addWidget(self.core_config_button, 1, 2)
        
        # Add grid layout to main layout
        main_layout.addLayout(grid_layout)
        
        # Add stretcher to push content to the top
        main_layout.addStretch()
    
    def show_signal_details_dialog(self):
        """Show the Signal Details dialog"""
        dialog = SignalDetailsDialog(self, "MySignal")
        result = dialog.exec_()
        
        if result == SignalDetailsDialog.Accepted:
            print("Signal details were accepted")
        else:
            print("Signal details were cancelled")
    
    def show_struct_field_dialog(self):
        """Show the Structure Field dialog"""
        dialog = StructFieldDialog(self)
        result = dialog.exec_()
        
        if result == StructFieldDialog.Accepted:
            field_data = dialog.get_field_data()
            print("Structure field data:", field_data)
        else:
            print("Structure field dialog was cancelled")
    
    def show_array_type_dialog(self):
        """Show the Array Type dialog"""
        dialog = ArrayTypeDialog(self)
        result = dialog.exec_()
        
        if result == ArrayTypeDialog.Accepted:
            array_config = dialog.get_array_config()
            print("Array configuration:", array_config)
        else:
            print("Array type dialog was cancelled")
    
    def show_data_type_dialog(self):
        """Show the Data Type Selection dialog"""
        dialog = DataTypeSelectionDialog(self)
        result = dialog.exec_()
        
        if result == DataTypeSelectionDialog.Accepted:
            data_type = dialog.get_data_type()
            print("Data type:", data_type)
        else:
            print("Data type dialog was cancelled")
    
    def show_core_properties_dialog(self):
        """Show the Core Properties dialog"""
        dialog = CorePropertiesDialog(self)
        result = dialog.exec_()
        
        if result == CorePropertiesDialog.Accepted:
            core_data = dialog.get_core_data()
            print("Core properties:", core_data)
        else:
            print("Core properties dialog was cancelled")
    
    def show_core_config_manager(self):
        """Show the Core Configuration Manager"""
        # Since CoreConfigManager is a widget, not a dialog,
        # we'll create and show it as a standalone window
        self.core_config_window = QMainWindow()
        self.core_config_window.setWindowTitle("Core Configuration Manager")
        self.core_config_window.resize(900, 650)
        
        # Create Core Config Manager widget as central widget
        core_config = CoreConfigManager()
        self.core_config_window.setCentralWidget(core_config)
        
        # Show the window
        self.core_config_window.show()


def main():
    """Main application entry point"""
    app = QApplication([])
    
    # Set stylesheet 
    with open("Cfg/Resources/styles/dark_theme.qss", "r") as f:
        app.setStyleSheet(f.read())
    
    # Create and show the demo window
    demo = DialogIntegrationDemo()
    demo.show()
    
    # Run the application event loop
    app.exec_()


if __name__ == "__main__":
    main()