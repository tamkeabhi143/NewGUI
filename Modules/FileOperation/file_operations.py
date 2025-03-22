#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Operations Module for Signal Manager
Handles loading, saving, importing and exporting data files
"""

import os
import json
import csv
import traceback
from PyQt5.QtCore import QObject

class FileOperations(QObject):
    """Handles file operations for the Signal Manager application"""
    
    def __init__(self, parent=None):
        """Initialize FileOperations"""
        super(FileOperations, self).__init__(parent)
        self.last_file_path = ""
        self.current_data = {}
    
    def load_config_file(self, file_path):
        """
        Load a configuration file
        
        Args:
            file_path (str): Path to the configuration file
            
        Returns:
            bool: True if file loaded successfully, False otherwise
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.current_data = data
                self.last_file_path = file_path
                return True
        except Exception as e:
            print(f"Error loading config file: {str(e)}")
            traceback.print_exc()
            return False
    
    def save_config_file(self, file_path, config_data):
        """
        Save a configuration file
        
        Args:
            file_path (str): Path to save the configuration file
            config_data (dict): Configuration data to save
            
        Returns:
            bool: True if file saved successfully, False otherwise
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(config_data, file, indent=4)
                self.current_data = config_data
                self.last_file_path = file_path
                return True
        except Exception as e:
            print(f"Error saving config file: {str(e)}")
            traceback.print_exc()
            return False
    
    def export_to_excel(self, file_path, data):
        """
        Export data to Excel format (CSV for simplicity)
        
        Args:
            file_path (str): Path to save the Excel file
            data (dict): Data to export
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            # For simplicity, we'll use CSV format
            # In a real application, you would use a library like openpyxl or pandas for Excel files
            
            # Determine the file extension
            _, ext = os.path.splitext(file_path)
            
            if ext.lower() == '.csv':
                # Export as CSV
                self._export_to_csv(file_path, data)
            else:
                # For .xlsx or other formats, still use CSV for this example
                # In a real app, you would use proper Excel export here
                print("Warning: Excel export is simulated with CSV. Use openpyxl for real Excel files.")
                self._export_to_csv(file_path, data)
            
            return True
        except Exception as e:
            print(f"Error exporting to Excel: {str(e)}")
            traceback.print_exc()
            return False
    
    def _export_to_csv(self, file_path, data):
        """Helper method to export data as CSV"""
        # Flatten the data structure for CSV export
        flattened_data = []
        
        if isinstance(data, dict):
            # If the data is a simple dictionary with string keys and values
            if all(isinstance(k, str) and isinstance(v, (str, int, float, bool)) for k, v in data.items()):
                # Use dictionary as a single row
                headers = list(data.keys())
                row = [data[key] for key in headers]
                flattened_data = [headers, row]
            else:
                # Try to find a list of dictionaries to export
                for key, value in data.items():
                    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                        if value:  # Non-empty list
                            headers = list(value[0].keys())
                            flattened_data = [headers]
                            flattened_data.extend([[item.get(header, "") for header in headers] for item in value])
                            break
        
        # If we couldn't find a suitable structure, create a simple key-value format
        if not flattened_data:
            flattened_data = [["Key", "Value"]]
            for key, value in self._flatten_dict(data).items():
                flattened_data.append([key, value])
        
        # Write to CSV
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(flattened_data)
    
    def _flatten_dict(self, d, parent_key='', sep='.'):
        """Flatten a nested dictionary into key-value pairs"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Convert lists to string representation
                items.append((new_key, str(v)))
            else:
                items.append((new_key, v))
                
        return dict(items)
    
    def import_from_excel(self, file_path, data):
        """
        Import data from Excel format
        
        Args:
            file_path (str): Path to the Excel file
            data (dict): Variable to store the imported data
            
        Returns:
            bool: True if import successful, False otherwise
        """
        try:
            # Determine the file extension
            _, ext = os.path.splitext(file_path)
            
            if ext.lower() == '.csv':
                # Import from CSV
                imported_data = self._import_from_csv(file_path)
            else:
                # For .xlsx or other formats, in a real app you would use openpyxl
                # For this example, we'll still use CSV
                print("Warning: Excel import is simulated with CSV. Use openpyxl for real Excel files.")
                imported_data = self._import_from_csv(file_path)
            
            # Update the output dictionary
            data.update(imported_data)
            
            return True
        except Exception as e:
            print(f"Error importing from Excel: {str(e)}")
            traceback.print_exc()
            return False
    
    def _import_from_csv(self, file_path):
        """Helper method to import data from CSV"""
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            
            # Read the headers
            headers = next(reader)
            
            if len(headers) == 2 and headers[0] == "Key" and headers[1] == "Value":
                # Simple key-value format
                result = {}
                for row in reader:
                    if len(row) >= 2:
                        key, value = row[0], row[1]
                        # Try to convert numeric strings to numbers
                        try:
                            if '.' in value:
                                value = float(value)
                            else:
                                value = int(value)
                        except ValueError:
                            # Keep as string if not numeric
                            pass
                            
                        # Handle nested keys (e.g., "parent.child")
                        keys = key.split('.')
                        current = result
                        for k in keys[:-1]:
                            current = current.setdefault(k, {})
                        current[keys[-1]] = value
            else:
                # Assume it's a list of records format
                result = {}
                records = []
                
                for row in reader:
                    if len(row) == len(headers):
                        record = {}
                        for i, header in enumerate(headers):
                            value = row[i]
                            # Try to convert numeric strings to numbers
                            try:
                                if '.' in value:
                                    value = float(value)
                                elif value.isdigit():
                                    value = int(value)
                            except (ValueError, AttributeError):
                                # Keep as is if not numeric or not a string
                                pass
                            record[header] = value
                        records.append(record)
                
                result["records"] = records
            
            return result
    
    def get_current_data(self):
        """Get the currently loaded data"""
        return self.current_data