#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Core Configuration Manager
Modern implementation of the CoreConfigManager.ui
"""

import os
import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                           QLabel, QListView, QFrame, QPushButton, QTreeView,
                           QSplitter, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSize

class CoreConfigManager(QWidget):
    """Core Configuration Manager widget"""
    
    def __init__(self, parent=None):
        super(CoreConfigManager, self).__init__(parent)
        
        self.setup_ui()
        self.connect_signals_slots()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Set window properties
        self.setWindowTitle("Core Configuration Manager")
        self.resize(900, 650)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create tab pages
        self.create_build_image_tab()
        self.create_board_config_tab()
        self.create_soc_core_tab()
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.build_image_tab, "Build Image Config")
        self.tab_widget.addTab(self.board_config_tab, "Board Configuration")
        self.tab_widget.addTab(self.soc_core_tab, "SOC - Core Configuration")
        
        # Set the default tab
        self.tab_widget.setCurrentIndex(0)
        
        # Add tab widget to main layout
        self.main_layout.addWidget(self.tab_widget)
    
    def create_build_image_tab(self):
        """Create the Build Image Configuration tab"""
        self.build_image_tab = QWidget()
        self.build_image_layout = QHBoxLayout(self.build_image_tab)
        
        # Create Build Image frame
        self.build_image_frame = QFrame()
        self.build_image_frame.setObjectName("card")
        self.build_image_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Create Build Image frame layout
        self.build_image_frame_layout = QVBoxLayout(self.build_image_frame)
        
        # Create Build Image title label
        bold_font = QFont()
        bold_font.setBold(True)
        
        self.build_image_label = QLabel("Build Image Types")
        self.build_image_label.setFont(bold_font)
        
        # Create Build Image list view
        self.build_image_list_view = QListView()
        self.build_image_list_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Add widgets to Build Image frame layout
        self.build_image_frame_layout.addWidget(self.build_image_label)
        self.build_image_frame_layout.addWidget(self.build_image_list_view)
        
        # Create button layout
        self.build_image_button_layout = QVBoxLayout()
        
        # Add spacer above buttons
        self.build_image_button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Create Add Image Type button
        self.add_image_type_button = QPushButton("Add Image Type")
        self.build_image_button_layout.addWidget(self.add_image_type_button)
        
        # Add spacer between buttons
        self.build_image_button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Create Remove button
        self.remove_image_type_button = QPushButton("Remove")
        self.build_image_button_layout.addWidget(self.remove_image_type_button)
        
        # Add spacer below buttons
        self.build_image_button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Add frame and button layout to tab layout
        self.build_image_layout.addWidget(self.build_image_frame)
        self.build_image_layout.addLayout(self.build_image_button_layout)
    
    def create_board_config_tab(self):
        """Create the Board Configuration tab"""
        self.board_config_tab = QWidget()
        self.board_config_layout = QVBoxLayout(self.board_config_tab)
        
        # Create Board List frame
        self.board_list_frame = QFrame()
        self.board_list_frame.setObjectName("card")
        self.board_list_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Create Board List frame layout
        self.board_list_layout = QVBoxLayout(self.board_list_frame)
        
        # Create Board list title label
        bold_font = QFont()
        bold_font.setBold(True)
        
        self.board_frame_label = QLabel("Supported Board Lists")
        self.board_frame_label.setFont(bold_font)
        
        # Create Board list view
        self.board_list_view = QListView()
        
        # Create Board button layout
        self.board_button_layout = QHBoxLayout()
        
        # Create Add Board button
        self.add_board_button = QPushButton("Add Board")
        
        # Create Remove Board button
        self.remove_board_button = QPushButton("Remove Board")
        
        # Add buttons to layout
        self.board_button_layout.addWidget(self.add_board_button)
        self.board_button_layout.addWidget(self.remove_board_button)
        self.board_button_layout.addStretch()
        
        # Add widgets to Board List frame layout
        self.board_list_layout.addWidget(self.board_frame_label)
        self.board_list_layout.addWidget(self.board_list_view)
        self.board_list_layout.addLayout(self.board_button_layout)
        
        # Add Board List frame to tab layout
        self.board_config_layout.addWidget(self.board_list_frame)
    
    def create_soc_core_tab(self):
        """Create the SOC-Core Configuration tab"""
        self.soc_core_tab = QWidget()
        self.soc_core_layout = QHBoxLayout(self.soc_core_tab)
        
        # Create SOC Core Config frame
        self.soc_core_config_frame = QFrame()
        self.soc_core_config_frame.setObjectName("card")
        self.soc_core_config_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Create SOC Core Config frame layout
        self.soc_core_config_layout = QVBoxLayout(self.soc_core_config_frame)
        
        # Create SOC Core Config title label
        bold_font = QFont()
        bold_font.setBold(True)
        
        self.soc_core_label = QLabel("SOC - Core Configuration List")
        self.soc_core_label.setFont(bold_font)
        
        # Create SOC Core tree view
        self.soc_core_tree_view = QTreeView()
        self.soc_core_tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Set up a basic model for the tree view
        self.soc_core_model = QStandardItemModel()
        self.soc_core_model.setHorizontalHeaderLabels(["SOC / Core"])
        self.soc_core_tree_view.setModel(self.soc_core_model)
        
        # Add widgets to SOC Core Config frame layout
        self.soc_core_config_layout.addWidget(self.soc_core_label)
        self.soc_core_config_layout.addWidget(self.soc_core_tree_view)
        
        # Create button layout
        self.soc_core_button_layout = QVBoxLayout()
        
        # Add spacer above buttons
        self.soc_core_button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Create Add SOC button
        self.add_soc_button = QPushButton("Add SOC")
        self.soc_core_button_layout.addWidget(self.add_soc_button)
        
        # Add spacer between buttons
        self.soc_core_button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Create Remove SOC button
        self.remove_soc_button = QPushButton("Remove SOC")
        self.soc_core_button_layout.addWidget(self.remove_soc_button)
        
        # Add spacer between buttons
        self.soc_core_button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Create Add Core button
        self.add_core_button = QPushButton("Add Core")
        self.soc_core_button_layout.addWidget(self.add_core_button)
        
        # Add spacer between buttons
        self.soc_core_button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Create Remove Core button
        self.remove_core_button = QPushButton("Remove Core")
        self.soc_core_button_layout.addWidget(self.remove_core_button)
        
        # Add spacer between buttons
        self.soc_core_button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Create Save button
        self.save_soc_core_button = QPushButton("Save")
        self.soc_core_button_layout.addWidget(self.save_soc_core_button)
        
        # Add spacer below buttons
        self.soc_core_button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Add frame and button layout to tab layout
        self.soc_core_layout.addWidget(self.soc_core_config_frame)
        self.soc_core_layout.addLayout(self.soc_core_button_layout)
    
    def connect_signals_slots(self):
        """Connect signals and slots"""
        # Connect Build Image tab buttons
        self.add_image_type_button.clicked.connect(self.on_add_image_type)
        self.remove_image_type_button.clicked.connect(self.on_remove_image_type)
        
        # Connect Board Configuration tab buttons
        self.add_board_button.clicked.connect(self.on_add_board)
        self.remove_board_button.clicked.connect(self.on_remove_board)
        
        # Connect SOC Core tab buttons
        self.add_soc_button.clicked.connect(self.on_add_soc)
        self.remove_soc_button.clicked.connect(self.on_remove_soc)
        self.add_core_button.clicked.connect(self.on_add_core)
        self.remove_core_button.clicked.connect(self.on_remove_core)
        self.save_soc_core_button.clicked.connect(self.on_save_soc_core)
    
    def on_add_image_type(self):
        """Handle Add Image Type button clicked"""
        print("Add Image Type clicked")
        # TODO: Implement add image type functionality
    
    def on_remove_image_type(self):
        """Handle Remove Image Type button clicked"""
        print("Remove Image Type clicked")
        # TODO: Implement remove image type functionality
    
    def on_add_board(self):
        """Handle Add Board button clicked"""
        print("Add Board clicked")
        # TODO: Implement add board functionality
    
    def on_remove_board(self):
        """Handle Remove Board button clicked"""
        print("Remove Board clicked")
        # TODO: Implement remove board functionality
    
    def on_add_soc(self):
        """Handle Add SOC button clicked"""
        print("Add SOC clicked")
        # TODO: Implement add SOC functionality
    
    def on_remove_soc(self):
        """Handle Remove SOC button clicked"""
        print("Remove SOC clicked")
        # TODO: Implement remove SOC functionality
    
    def on_add_core(self):
        """Handle Add Core button clicked"""
        print("Add Core clicked")
        # TODO: Implement add core functionality
        
        # Open core properties dialog
        from core_properties_dialog import CorePropertiesDialog
        dialog = CorePropertiesDialog(self)
        dialog.exec_()
    
    def on_remove_core(self):
        """Handle Remove Core button clicked"""
        print("Remove Core clicked")
        # TODO: Implement remove core functionality
    
    def on_save_soc_core(self):
        """Handle Save SOC Core button clicked"""
        print("Save SOC Core clicked")
        # TODO: Implement save SOC core functionality