#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Application initialization module
Imports and exports necessary components
"""

import sys
import os

# Add the project root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import main application modules
from .main import main