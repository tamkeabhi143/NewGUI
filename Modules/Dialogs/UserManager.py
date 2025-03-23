#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User Manager module for handling user authentication and storage
"""

import os
import json
import hashlib
from PyQt5.QtCore import QDateTime, Qt
from icecream import ic

class UserManager:
    """Class for managing user authentication and storage"""
    
    def __init__(self, base_dir):
        """Initialize the UserManager with the base directory"""
        # Construct the full path to users.json
        self.users_file = os.path.join(base_dir, "Cfg", "Resources", "Credentials", "users.json")
        ic(f"Looking for users.json at: {self.users_file}")  # Debug print
        self.users = self.load_users()
    
    def load_users(self):
        """Load users from the storage file"""
        if not os.path.exists(self.users_file):
            ic("users.json not found. Creating new user database.")  # Debug print
            return {}
        
        try:
            # Open in read-only mode
            with open(self.users_file, 'r') as f:
                ic("Successfully loaded users.json")  # Debug print
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            ic(f"Error loading users.json: {str(e)}")  # Debug print
            return {}
    
    def hash_password(self, password):
        """Hash a password using SHA-256 with salt"""
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return salt + key
    
    def verify_password(self, stored_password, provided_password):
        """Verify a password against the stored hash"""
        salt = stored_password[:32]
        key = stored_password[32:]
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt,
            100000
        )
        return key == new_key
    
    def user_exists(self, username):
        """Check if a user exists"""
        return username.lower() in (u.lower() for u in self.users.keys())
    
    def create_user(self, username, password):
        """Create a new user"""
        if self.user_exists(username):
            return False
        
        # Temporarily make file writable
        if os.path.exists(self.users_file):
            os.chmod(self.users_file, 0o600)  # Read-write for owner
        
        self.users[username] = {
            'password': self.hash_password(password).hex(),
            'created_at': QDateTime.currentDateTime().toString(Qt.ISODate)
        }
        
        # Save users
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)
        
        # Make file read-only
        os.chmod(self.users_file, 0o400)  # Read-only for owner
        return True
    
    def authenticate(self, username, password):
        """Authenticate a user"""
        user_data = self.users.get(username)
        if not user_data:
            return False
        
        stored_password = bytes.fromhex(user_data['password'])
        return self.verify_password(stored_password, password)
    
    def update_password(self, username, new_password):
        """Update a user's password"""
        if not self.user_exists(username):
            return False
        
        # Temporarily make file writable
        if os.path.exists(self.users_file):
            os.chmod(self.users_file, 0o600)  # Read-write for owner
        
        # Update password
        self.users[username]['password'] = self.hash_password(new_password).hex()
        
        # Save users
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)
        
        # Make file read-only
        os.chmod(self.users_file, 0o400)  # Read-only for owner
        return True