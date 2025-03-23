#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Forgot Password Dialog module for handling password recovery
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                           QPushButton, QMessageBox, QFormLayout)
from PyQt5.QtCore import Qt
from Modules.Dialogs.UserManager import UserManager

class ForgotPasswordDialog(QDialog):
    """Dialog for handling password recovery"""
    
    def __init__(self, parent=None):
        """Initialize the dialog
        
        Args:
            parent: The parent widget
        """
        super(ForgotPasswordDialog, self).__init__(parent)
        
        # Set up UI
        self.setup_ui()
        
        # Connect signals and slots
        self.connect_signals_slots()
    
    def setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("Forgot Password")
        self.setFixedSize(400, 200)
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
        self.username_edit.setPlaceholderText("Enter your username")
        form_layout.addRow("Username:", self.username_edit)
        
        # New Password
        self.new_password_edit = QLineEdit()
        self.new_password_edit.setEchoMode(QLineEdit.Password)
        self.new_password_edit.setPlaceholderText("Enter new password")
        form_layout.addRow("New Password:", self.new_password_edit)
        
        # Confirm New Password
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit.setPlaceholderText("Confirm new password")
        form_layout.addRow("Confirm Password:", self.confirm_password_edit)
        
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.reset_button = QPushButton("Reset Password")
        self.reset_button.setDefault(True)
        self.reset_button.setFixedWidth(120)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedWidth(100)
        
        button_layout.addStretch()
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_layout)
    
    def connect_signals_slots(self):
        """Connect signals and slots for dialog interactions"""
        self.reset_button.clicked.connect(self.on_reset_password)
        self.cancel_button.clicked.connect(self.reject)
    
    def validate_form(self):
        """Validate the form data
        
        Returns:
            bool: True if the form is valid, False otherwise
        """
        username = self.username_edit.text().strip()
        new_password = self.new_password_edit.text()
        confirm_password = self.confirm_password_edit.text()
        
        if not username:
            QMessageBox.warning(self, "Validation Error", "Please enter your username.")
            self.username_edit.setFocus()
            return False
        
        if not new_password:
            QMessageBox.warning(self, "Validation Error", "Please enter a new password.")
            self.new_password_edit.setFocus()
            return False
        
        if new_password != confirm_password:
            QMessageBox.warning(self, "Validation Error", "Passwords do not match.")
            self.confirm_password_edit.setFocus()
            return False
        
        return True
    
    def on_reset_password(self):
        """Handle reset password button click"""
        if self.validate_form():
            username = self.username_edit.text().strip()
            new_password = self.new_password_edit.text()
            
            # Get the user manager instance
            user_manager = UserManager(os.path.dirname(os.path.abspath(__file__)))
            
            if not user_manager.user_exists(username):
                QMessageBox.warning(
                    self,
                    "User Not Found",
                    f"User '{username}' does not exist."
                )
                return
            
            if user_manager.update_password(username, new_password):
                QMessageBox.information(
                    self,
                    "Password Updated",
                    "Your password has been successfully updated."
                )
                self.accept()
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Failed to update password. Please try again."
                ) 