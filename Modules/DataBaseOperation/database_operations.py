#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database Operations Module for Signal Manager
Handles database-related operations for signal data
"""

import json
import os
from PyQt5.QtCore import QObject

class DatabaseOperations(QObject):
    """Handles database operations for the Signal Manager application"""
    
    def __init__(self, parent=None):
        """Initialize DatabaseOperations"""
        super(DatabaseOperations, self).__init__(parent)
        self.signals = []
        self.current_board = ""
        self.current_soc = ""
    
    def load_signals(self, data):
        """
        Load signals from data
        
        Args:
            data (dict): Data containing signal information
            
        Returns:
            bool: True if signals loaded successfully, False otherwise
        """
        try:
            if "signals" in data and isinstance(data["signals"], list):
                self.signals = data["signals"]
                return True
            return False
        except Exception as e:
            print(f"Error loading signals: {str(e)}")
            return False
    
    def save_signals(self, data):
        """
        Save signals to data
        
        Args:
            data (dict): Data dictionary to update with signal information
            
        Returns:
            bool: True if signals saved successfully, False otherwise
        """
        try:
            data["signals"] = self.signals
            return True
        except Exception as e:
            print(f"Error saving signals: {str(e)}")
            return False
    
    def add_signal(self, signal_data):
        """
        Add a new signal
        
        Args:
            signal_data (dict): Signal data to add
            
        Returns:
            bool: True if signal added successfully, False otherwise
        """
        try:
            # Check if signal with this ID already exists
            if "id" in signal_data:
                for signal in self.signals:
                    if signal.get("id") == signal_data["id"]:
                        return False  # Signal with this ID already exists
            
            # Add signal to the list
            self.signals.append(signal_data)
            return True
        except Exception as e:
            print(f"Error adding signal: {str(e)}")
            return False
    
    def update_signal(self, signal_id, updated_data):
        """
        Update an existing signal
        
        Args:
            signal_id: ID of the signal to update
            updated_data (dict): Updated signal data
            
        Returns:
            bool: True if signal updated successfully, False otherwise
        """
        try:
            for i, signal in enumerate(self.signals):
                if signal.get("id") == signal_id:
                    # Update the signal data
                    self.signals[i] = updated_data
                    return True
            return False  # Signal not found
        except Exception as e:
            print(f"Error updating signal: {str(e)}")
            return False
    
    def delete_signal(self, signal_id):
        """
        Delete a signal
        
        Args:
            signal_id: ID of the signal to delete
            
        Returns:
            bool: True if signal deleted successfully, False otherwise
        """
        try:
            for i, signal in enumerate(self.signals):
                if signal.get("id") == signal_id:
                    # Remove the signal
                    del self.signals[i]
                    return True
            return False  # Signal not found
        except Exception as e:
            print(f"Error deleting signal: {str(e)}")
            return False
    
    def get_signal(self, signal_id):
        """
        Get a signal by ID
        
        Args:
            signal_id: ID of the signal to get
            
        Returns:
            dict: Signal data if found, None otherwise
        """
        for signal in self.signals:
            if signal.get("id") == signal_id:
                return signal
        return None
    
    def get_all_signals(self):
        """
        Get all signals
        
        Returns:
            list: List of all signals
        """
        return self.signals
    
    def filter_signals(self, **kwargs):
        """
        Filter signals based on provided criteria
        
        Args:
            **kwargs: Filter criteria as key-value pairs
            
        Returns:
            list: List of filtered signals
        """
        filtered_signals = []
        
        for signal in self.signals:
            match = True
            for key, value in kwargs.items():
                if key not in signal or signal[key] != value:
                    match = False
                    break
            if match:
                filtered_signals.append(signal)
        
        return filtered_signals
    
    def set_current_board(self, board):
        """
        Set the current board
        
        Args:
            board (str): Board name
        """
        self.current_board = board
    
    def set_current_soc(self, soc):
        """
        Set the current SOC
        
        Args:
            soc (str): SOC name
        """
        self.current_soc = soc
    
    def get_boards(self):
        """
        Get list of unique boards from signals
        
        Returns:
            list: List of board names
        """
        boards = set()
        for signal in self.signals:
            if "board" in signal and signal["board"]:
                boards.add(signal["board"])
        return sorted(list(boards))
    
    def get_socs(self, board=None):
        """
        Get list of unique SOCs from signals
        
        Args:
            board (str, optional): Filter SOCs by board
            
        Returns:
            list: List of SOC names
        """
        socs = set()
        for signal in self.signals:
            if "soc" in signal and signal["soc"]:
                if board is None or signal.get("board") == board:
                    socs.add(signal["soc"])
        return sorted(list(socs))
    
    def get_build_images(self, board=None, soc=None):
        """
        Get list of unique build images from signals
        
        Args:
            board (str, optional): Filter build images by board
            soc (str, optional): Filter build images by SOC
            
        Returns:
            list: List of build image names
        """
        build_images = set()
        for signal in self.signals:
            if "build_image" in signal and signal["build_image"]:
                match = True
                if board is not None and signal.get("board") != board:
                    match = False
                if soc is not None and signal.get("soc") != soc:
                    match = False
                if match:
                    build_images.add(signal["build_image"])
        return sorted(list(build_images))