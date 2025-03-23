# Signal Operations Module

This module contains classes for managing signal operations in the application.

## Directory Structure

The `SignalOperations` module is organized as follows:

- `__init__.py`: Package initialization file
- `SignalManager.py`: Main class for managing signal operations

## Usage

To use the SignalManager class in your application:

```python
from Modules.SignalOperations.SignalManager import SignalManager

# Create an instance of SignalManager
signal_manager = SignalManager(parent=self)

# Set the project data
signal_manager.set_project_data(self.project_data)

# Find a signal by ID
signal = signal_manager.find_signal_by_id(signal_id)

# Add a signal to the database
signal_id = signal_manager.add_signal_to_database(signal_data)

# Update a signal
success = signal_manager.update_signal_in_database(signal_id, updated_data)

# Delete a signal
success = signal_manager.delete_signal_from_database(signal_id)

# Update the signal tree
signal_manager.update_signal_tree(self.signal_tree_widget)

# Populate signal details
signal_manager.populate_signal_details(self, signal_data, self.signal_details_layout)

# Collect signal form data
collected_data = signal_manager.collect_signal_form_data(self)

# Validate signal data
is_valid, error_message = signal_manager.validate_signal_data(signal_data)
```

## Migration Notes

Previously, signal operations were handled directly in the `signal_manager_app.py` file. They have been moved to this dedicated module to improve code organization and maintainability.

To migrate the code, replace direct signal operations in `signal_manager_app.py` with calls to the corresponding methods in the `SignalManager` class. 