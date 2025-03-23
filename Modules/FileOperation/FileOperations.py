import json
from PyQt5 import QtWidgets

class FileOperations:
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_file = None
        self.modified = False

    def new_file(self):
        """Handle File -> New action"""
        # Check if current file has unsaved changes
        if self.modified:
            reply = QtWidgets.QMessageBox.question(
                self.main_window,
                'Unsaved Changes',
                'You have unsaved changes. Do you want to save them before creating a new file?',
                QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel
            )
            
            if reply == QtWidgets.QMessageBox.Cancel:
                return False
            elif reply == QtWidgets.QMessageBox.Save:
                # Save current file
                if not self.save_file():
                    return False
        
        # Open a file dialog to create new file
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.main_window,
            "Create New File",
            "",
            "JSON Files (*.json);;All Files (*)",
            options=options
        )
        if not file_name:
            return False

        # Reset file state
        self.current_file = None
        self.modified = False
        
        # Create new default configuration
        # Let the main window handle showing the core configuration dialog
        return True

    def show_core_config_dialog(self):
        """Show core configuration dialog and handle results"""
        dialog = CoreConfigDialog(self.main_window)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Get the configuration data from the dialog
            config_data = dialog.get_config_data()
            
            # Update the current file with the new configuration
            self.update_config_file(config_data)
            
            # Update the GUI with the new configuration
            self.main_window.populate_core_config_gui(config_data)
            
    def update_config_file(self, config_data):
        """Update the current JSON file with new configuration"""
        try:
            with open(self.current_file, 'r') as f:
                current_config = json.load(f)
            
            current_config['core_config'] = config_data
            
            with open(self.current_file, 'w') as f:
                json.dump(current_config, f, indent=4)
                
            self.modified = False
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.main_window, "Error", f"Failed to update file: {str(e)}")
            
    def save_config_file(self, file_path, project_data):
        """Save project data to the specified file path"""
        try:
            with open(file_path, 'w') as f:
                json.dump(project_data, f, indent=4)
            
            self.current_file = file_path
            self.modified = False
            return True
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.main_window, "Error", f"Failed to save file: {str(e)}")
            return False
            
    def load_config_file(self, file_path):
        """Load project data from the specified file path"""
        try:
            with open(file_path, 'r') as f:
                self.current_data = json.load(f)
            
            self.current_file = file_path
            self.modified = False
            return True
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.main_window, "Error", f"Failed to load file: {str(e)}")
            return False
            
    def get_current_data(self):
        """Return the currently loaded data"""
        return self.current_data if hasattr(self, 'current_data') else {} 