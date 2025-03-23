#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create User Dialog module for creating new user accounts
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QMessageBox, QFormLayout,
                           QDialogButtonBox)
from PyQt5.QtCore import Qt
import os
from icecream import ic

class CreateUserDialog(QDialog):
    """Dialog for creating new users"""
    
    def __init__(self, parent=None):
        """Initialize the dialog
        
        Args:
            parent: The parent widget
        """
        super(CreateUserDialog, self).__init__(parent)
        
        # Set up member variables
        self.username = ""
        
        # Set up UI
        self.setup_ui()
        
        # Connect signals and slots
        self.connect_signals_slots()
    
    def setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("Create New User")
        self.setFixedSize(400, 250)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # Apply dark theme styles
        self.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d7;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
        """)
        
        # Create layout
        main_layout = QVBoxLayout(self)
        
        # Create form layout
        form_layout = QFormLayout()
        
        # Username
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter new username")
        form_layout.addRow("Username:", self.username_edit)
        
        # Password
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("Enter password")
        form_layout.addRow("Password:", self.password_edit)
        
        # Confirm Password
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit.setPlaceholderText("Confirm password")
        form_layout.addRow("Confirm Password:", self.confirm_password_edit)
        
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.create_button = QPushButton("Create User")
        self.create_button.setDefault(True)
        self.create_button.setFixedWidth(100)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedWidth(100)
        
        button_layout.addStretch()
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_layout)
    
    def connect_signals_slots(self):
        """Connect signals and slots for dialog interactions"""
        self.create_button.clicked.connect(self.on_create)
        self.cancel_button.clicked.connect(self.reject)
    
    def validate_form(self):
        """Validate the form data
        
        Returns:
            bool: True if the form is valid, False otherwise
        """
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()
        
        if not username:
            QMessageBox.warning(self, "Validation Error", "Please enter a username.")
            self.username_edit.setFocus()
            return False
        
        if not password:
            QMessageBox.warning(self, "Validation Error", "Please enter a password.")
            self.password_edit.setFocus()
            return False
        
        if password != confirm_password:
            QMessageBox.warning(self, "Validation Error", "Passwords do not match.")
            self.confirm_password_edit.setFocus()
            return False
        
        # TODO: Add additional validation (e.g., password complexity, username uniqueness)
        
        return True
    
    def on_create(self):
        """Handle create button click"""
        if self.validate_form():
            username = self.username_edit.text().strip()
            password = self.password_edit.text()
            
            # Get the user manager instance
            from Modules.Dialogs.UserManager import UserManager
            # Get the base directory (NewGUI folder)
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            ic(f"Base directory: {base_dir}")
            user_manager = UserManager(base_dir)
            
            if user_manager.user_exists(username):
                QMessageBox.information(
                    self,
                    "User Exists",
                    f"User '{username}' already exists.\nPlease log in instead."
                )
                self.reject()
                return
            
            if user_manager.create_user(username, password):
                self.username = username
                self.accept()
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Failed to create user. Please try again."
                ) 