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
