import os
import sys

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Add the ModernLookUI directory to the Python path to allow internal imports
if current_dir not in sys.path:
    sys.path.append(current_dir)

from App.run_app import run_app
from App.signal_manager_app import SignalManagerApp

from Cfg.Resources import resources_rc  # Import resource file to initialize resources

from Modules.MenuOperation.menu_operations import MenuOperations
from Modules.FileOperation.FileOperations import FileOperations
from Modules.DataBaseOperation.database_operations import DatabaseOperations

from Modules.Dialogs.UserManager import UserManager
from Modules.Dialogs.LoginDialog import LoginDialog
from Modules.Dialogs.CoreConfigurationManager.CoreConfig import CoreConfigManager
from Modules.Dialogs.CreateUserDialog import CreateUserDialog
from Modules.Dialogs.ForgotPasswordDialog import ForgotPasswordDialog
from Modules.Dialogs.LoginDialog import LoginDialog
from Modules.Dialogs.SignalDetailsDialog import SignalDetailsDialog
