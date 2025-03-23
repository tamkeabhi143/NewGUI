#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Login Dialog module for authenticating users
"""

import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QMessageBox, QGridLayout,
                           QFormLayout, QDialogButtonBox, QCheckBox)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from icecream import ic
from Utils.path_utils import get_resource_path

class LoginDialog(QDialog):
    """Dialog for user authentication"""
    
    def __init__(self, parent=None):
        """Initialize the dialog
        
        Args:
            parent: The parent widget
        """
        super(LoginDialog, self).__init__(parent)
        
        # Set up member variables
        self.authenticated = False
        self.username = ""
        self.settings = QSettings("SignalManagerApp", "Login")
        
        # Set up UI
        self.setup_ui()
        
        # Connect signals and slots
        self.connect_signals_slots()
        
        # Load saved username if available
        self.load_saved_credentials()
    
    def setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("Signal Manager - Login")
        self.setFixedSize(400, 300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # Set window icon
        icon_path = get_resource_path('Cfg\\Resources\\icons\\login.png')
        ic(icon_path)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
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
            QCheckBox {
                color: #ffffff;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:checked {
                background-color: #0078d7;
                border: 1px solid #555555;
            }
            QCheckBox::indicator:unchecked {
                background-color: #3a3a3a;
                border: 1px solid #555555;
            }
            QLabel#create_account_label {
                color: #888888;
                font-size: 10pt;
                text-align: center;
            }
            QPushButton#create_account_button {
                background-color: transparent;
                color: #0078d7;
                border: none;
                padding: 0;
                text-align: center;
                font-size: 8pt;
                margin: 0;
            }
            QPushButton#create_account_button:hover {
                color: #0056b3;
                text-decoration: underline;
            }
            QPushButton#forgot_password_button {
                background-color: transparent;
                color: #0078d7;
                border: none;
                padding: 0;
                text-align: center;
                font-size: 8pt;
                margin: 0;
            }
            QPushButton#forgot_password_button:hover {
                color: #0056b3;
                text-decoration: underline;
            }
        """)
        
        # Create layout
        main_layout = QVBoxLayout(self)
        
        # Add logo/header
        header_layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo_label.setText("")
        logo_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: #ffffff;")
        
        # Title
        title_label = QLabel("Signal Manager Login")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #ffffff;")
        
        # Create a centered layout for the title
        title_layout = QHBoxLayout()
        title_layout.addStretch()
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Add widgets to header layout
        header_layout.addWidget(logo_label)
        header_layout.addLayout(title_layout, 1)  # Add stretch to push title to center
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(20)
        
        # Create form layout
        form_layout = QFormLayout()
        
        # Username
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter your username")
        form_layout.addRow("Username:", self.username_edit)
        
        # Password
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("Enter your password")
        form_layout.addRow("Password:", self.password_edit)
        
        # Remember me
        self.remember_checkbox = QCheckBox("Remember username")
        form_layout.addRow("", self.remember_checkbox)
        
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton("Login")
        self.login_button.setDefault(True)
        self.login_button.setFixedWidth(100)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedWidth(100)
        
        # Add stretch on both sides to center the buttons
        button_layout.addStretch()
        button_layout.addWidget(self.login_button)
        button_layout.addSpacing(10)  # Add some spacing between buttons
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # Forgot password section
        forgot_password_layout = QVBoxLayout()
        forgot_password_layout.setContentsMargins(0, 5, 0, 0)  # Reduced top margin
        
        # Forgot password button
        self.forgot_password_button = QPushButton("Forgot Password?")
        self.forgot_password_button.setObjectName("forgot_password_button")
        self.forgot_password_button.setCursor(Qt.PointingHandCursor)
        self.forgot_password_button.setFixedWidth(110)  # Reduced width
        self.forgot_password_button.setFixedHeight(20)  # Reduced height
        
        forgot_password_layout.addWidget(self.forgot_password_button, 0, Qt.AlignCenter)
        main_layout.addLayout(forgot_password_layout)
        
        # Create account section
        create_account_layout = QVBoxLayout()
        create_account_layout.setContentsMargins(0, 5, 0, 0)  # Reduced top margin to match Forgot Password
        
        # Label
        create_account_label = QLabel("Don't have an account?")
        create_account_label.setObjectName("create_account_label")
        create_account_label.setAlignment(Qt.AlignCenter)
        
        # Create account button
        self.create_account_button = QPushButton("Create New")
        self.create_account_button.setObjectName("create_account_button")
        self.create_account_button.setCursor(Qt.PointingHandCursor)
        self.create_account_button.setFixedWidth(110)  # Match Forgot Password width
        self.create_account_button.setFixedHeight(20)  # Match Forgot Password height
        
        create_account_layout.addWidget(create_account_label)
        create_account_layout.addWidget(self.create_account_button, 0, Qt.AlignCenter)
        
        main_layout.addLayout(create_account_layout)
    
    def connect_signals_slots(self):
        """Connect signals and slots for dialog interactions"""
        self.login_button.clicked.connect(self.on_login)
        self.cancel_button.clicked.connect(self.reject)
        self.create_account_button.clicked.connect(self.on_create_account)
        self.password_edit.returnPressed.connect(self.on_login)
        self.forgot_password_button.clicked.connect(self.on_forgot_password)
    
    def load_saved_credentials(self):
        """Load saved username if available"""
        saved_username = self.settings.value("username", "")
        if saved_username:
            self.username_edit.setText(saved_username)
            self.remember_checkbox.setChecked(True)
            # Focus on password field if username is already filled
            self.password_edit.setFocus()
        else:
            self.username_edit.setFocus()
    
    def save_credentials(self):
        """Save username if remember me is checked"""
        if self.remember_checkbox.isChecked():
            self.settings.setValue("username", self.username_edit.text())
        else:
            self.settings.remove("username")
    
    def authenticate(self, username, password):
        """Authenticate user credentials"""
        from Modules.Dialogs.UserManager import UserManager
        # Get the base directory (NewGUI folder)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        ic(f"Base directory: {base_dir}")
        user_manager = UserManager(base_dir)
        return user_manager.authenticate(username, password)
    
    def on_login(self):
        """Handle login button click"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username:
            QMessageBox.warning(self, "Login Error", "Please enter a username.")
            self.username_edit.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, "Login Error", "Please enter a password.")
            self.password_edit.setFocus()
            return
        
        if self.authenticate(username, password):
            self.authenticated = True
            self.username = username
            self.save_credentials()
            self.accept()
        else:
            QMessageBox.critical(
                self, 
                "Authentication Failed", 
                "Invalid username or password.\n\nPlease try again."
            )
            self.password_edit.clear()
            self.password_edit.setFocus()
    
    def on_create_account(self):
        """Handle create account button click"""
        from Modules.Dialogs.CreateUserDialog import CreateUserDialog
        
        dialog = CreateUserDialog(self)
        if dialog.exec_() == QDialog.Accepted and dialog.username:
            # Set the username in the login form
            self.username_edit.setText(dialog.username)
            self.password_edit.setFocus()
    
    def on_forgot_password(self):
        """Handle forgot password button click"""
        from Modules.Dialogs.ForgotPasswordDialog import ForgotPasswordDialog
        
        dialog = ForgotPasswordDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # If password was successfully updated, focus on the password field
            self.password_edit.setFocus()
    
    @staticmethod
    def login(parent=None):
        """Static method to show the dialog and get the result
        
        Args:
            parent: The parent widget
            
        Returns:
            tuple: (success, username) where success is a bool indicating if login succeeded
        """
        dialog = LoginDialog(parent)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            return True, dialog.username
        
        return False, "" 