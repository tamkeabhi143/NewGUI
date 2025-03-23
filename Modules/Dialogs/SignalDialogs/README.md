# Signal Dialogs Module

This module contains dialogs related to signal management in the application.

## Directory Structure

The `SignalDialogs` module is organized as follows:

- `__init__.py`: Package initialization file
- `SignalDetailsDialog.py`: Main dialog for editing signal details
- `SignalAttributesDialog.py`: Dialog for managing signal attributes
- `StructFieldDialog.py`: Dialog for configuring struct fields
- `ArrayTypeDialog.py`: Dialog for configuring array types

## Usage

To use these dialogs, import them from the new location:

```python
from Modules.Dialogs.SignalDialogs.SignalDetailsDialog import SignalDetailsDialog
from Modules.Dialogs.SignalDialogs.SignalAttributesDialog import SignalAttributesDialog
from Modules.Dialogs.SignalDialogs.StructFieldDialog import StructFieldDialog
```

Or you can simply use the redirector modules in the parent directory:

```python
from Modules.Dialogs.SignalDetailsDialog import SignalDetailsDialog
from Modules.Dialogs.StructFieldDialog import StructFieldDialog
```

## Migration Notes

Previously, these classes were defined directly in the `Modules/Dialogs` directory. 
They have been moved to this dedicated module to improve code organization.

For backward compatibility, redirector modules have been added in the original locations.
These redirectors simply import the classes from their new locations. 