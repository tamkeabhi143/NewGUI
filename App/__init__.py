# This file makes the App directory a Python package
import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Add the parent directory to Python path so we can import Modules
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


# Import UI modules
from Cfg.Dialogs.signal_details_dialog import SignalDetailsDialog
from Cfg.Dialogs.struct_field_dialog import StructFieldDialog
from Cfg.Dialogs.array_type_dialog import ArrayTypeDialog
from Cfg.Dialogs.data_type_selection_dialog import DataTypeSelectionDialog
from Cfg.Dialogs.core_properties_dialog import CorePropertiesDialog
from Cfg.Dialogs.core_config_manager import CoreConfigManager
from Cfg.Dialogs.dialog_integration import DialogIntegrationDemo