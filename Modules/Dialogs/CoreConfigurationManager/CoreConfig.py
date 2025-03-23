from PyQt5 import QtWidgets, QtCore, QtGui, uic
import os
from .CoreProperties import CorePropertiesDialog

class CoreConfigManager:
    def __init__(self, parent):
        self.parent = parent

    def show_and_get_config(self, is_new_file=False, existing_data=None):
        """Show the core configuration dialog and return the configuration data"""
        dialog = CoreConfigDialog(self.parent, is_new_file)
        
        # If updating existing configuration, populate the dialog with existing data
        if existing_data:
            dialog.populate_from_existing_data(existing_data)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            return dialog.get_config_data()
        return None

class CoreConfigDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, is_new_file=False):
        super().__init__(parent)
        self.is_new_file = is_new_file
        # Load the UI directly instead of using the generated Python module
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        ui_file = os.path.join(project_dir, "Cfg", "LayoutFiles", "Dialogs", "CoreConfigManager.ui")
        print(f"Loading UI file: {ui_file}")
        uic.loadUi(ui_file, self)
        
        # Find and initialize the list views
        # For build image tab
        self.image_type_list_view = self.findChild(QtWidgets.QListView, "build_image_list_view")
        self.image_type_model = QtGui.QStandardItemModel(self)
        if self.image_type_list_view:
            self.image_type_list_view.setModel(self.image_type_model)
        
        # For SoC/Core tab (using tree view)
        self.soc_core_tree_view = self.findChild(QtWidgets.QTreeView, "soc_core_tree_view")
        self.soc_core_model = QtGui.QStandardItemModel(self)
        self.soc_core_model.setHorizontalHeaderLabels(["SoCs and Cores"])
        if self.soc_core_tree_view:
            self.soc_core_tree_view.setModel(self.soc_core_model)
        
        # For Board tab
        self.board_list_view = self.findChild(QtWidgets.QListView, "board_list_view")
        self.board_model = QtGui.QStandardItemModel(self)
        if self.board_list_view:
            self.board_list_view.setModel(self.board_model)
        
        # Connect buttons
        self.save_button = self.findChild(QtWidgets.QPushButton, "save_button")
        if self.save_button:
            self.save_button.clicked.connect(self.accept)
        
        self.cancel_button = self.findChild(QtWidgets.QPushButton, "cancel_button")
        if self.cancel_button:
            self.cancel_button.clicked.connect(self.reject)
        
        # Add/Remove buttons
        self.add_image_type_button = self.findChild(QtWidgets.QPushButton, "add_image_type_button")
        if self.add_image_type_button:
            self.add_image_type_button.clicked.connect(self.add_image_type)
        
        self.remove_image_type_button = self.findChild(QtWidgets.QPushButton, "remove_image_type_button")
        if self.remove_image_type_button:
            self.remove_image_type_button.clicked.connect(self.remove_image_type)
        
        self.add_soc_button = self.findChild(QtWidgets.QPushButton, "add_soc_button")
        if self.add_soc_button:
            self.add_soc_button.clicked.connect(self.add_soc)
        
        self.remove_soc_button = self.findChild(QtWidgets.QPushButton, "remove_soc_button")
        if self.remove_soc_button:
            self.remove_soc_button.clicked.connect(self.remove_soc)
        
        self.add_core_button = self.findChild(QtWidgets.QPushButton, "add_core_button")
        if self.add_core_button:
            self.add_core_button.clicked.connect(self.add_core)
        
        self.remove_core_button = self.findChild(QtWidgets.QPushButton, "remove_core_button")
        if self.remove_core_button:
            self.remove_core_button.clicked.connect(self.remove_core)
        
        self.add_board_button = self.findChild(QtWidgets.QPushButton, "add_board_button")
        if self.add_board_button:
            self.add_board_button.clicked.connect(self.add_board)
        
        self.remove_board_button = self.findChild(QtWidgets.QPushButton, "remove_board_button")
        if self.remove_board_button:
            self.remove_board_button.clicked.connect(self.remove_board)
    
    def add_image_type(self):
        """Add a new image type to the list"""
        text, ok = QtWidgets.QInputDialog.getText(self, "Add Image Type", "Enter image type name:")
        if ok and text:
            item = QtGui.QStandardItem(text)
            self.image_type_model.appendRow(item)
            print(f"Added image type: {text}")
    
    def remove_image_type(self):
        """Remove the selected image type"""
        if not self.image_type_list_view:
            return
            
        indexes = self.image_type_list_view.selectedIndexes()
        if not indexes:
            QtWidgets.QMessageBox.warning(self, "Selection Required", 
                                        "Please select an image type to remove.")
            return
            
        reply = QtWidgets.QMessageBox.question(
            self, "Confirm Removal", 
            "Are you sure you want to remove the selected image type?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            for index in sorted(indexes, key=lambda x: x.row(), reverse=True):
                self.image_type_model.removeRow(index.row())
    
    def add_soc(self):
        """Add a new SoC to the list"""
        text, ok = QtWidgets.QInputDialog.getText(self, "Add SoC", "Enter SoC name:")
        if ok and text:
            item = QtGui.QStandardItem(text)
            self.soc_core_model.appendRow(item)
            print(f"Added SoC: {text}")
    
    def remove_soc(self):
        """Remove the selected SoC"""
        if not self.soc_core_tree_view:
            return
            
        index = self.soc_core_tree_view.currentIndex()
        if not index.isValid() or index.parent().isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Required", 
                                        "Please select a SoC to remove.")
            return
            
        reply = QtWidgets.QMessageBox.question(
            self, "Confirm Removal", 
            "Are you sure you want to remove the selected SoC?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            self.soc_core_model.removeRow(index.row())
    
    def add_core(self):
        """Add a new core to the selected SoC"""
        if not self.soc_core_tree_view:
            return
            
        index = self.soc_core_tree_view.currentIndex()
        if not index.isValid() or index.parent().isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Required", 
                                        "Please select a SoC to add a core to.")
            return
        
        # Get the selected SoC name
        soc_item = self.soc_core_model.itemFromIndex(index)
        soc_name = soc_item.text() if soc_item else ""
        
        # Show the CorePropertiesDialog to get core properties
        core_properties = CorePropertiesDialog.get_core_properties(self)
        
        # If the user clicked OK and provided core properties
        if core_properties:
            core_name = core_properties.get('name', "Unnamed Core")
            # Create a new item for the core
            core_item = QtGui.QStandardItem(core_name)
            # Store the core properties in the item's data
            core_item.setData(core_properties, QtCore.Qt.UserRole)
            
            # Add child items for each core property to display in tree view
            for prop_name, prop_value in core_properties.items():
                if prop_name != 'name':  # Name is already the item text
                    prop_item = QtGui.QStandardItem(f"{prop_name}: {prop_value}")
                    core_item.appendRow(prop_item)
            
            # Add the item to the SoC
            soc_item.appendRow(core_item)
            # Expand the SoC item to show the new core
            self.soc_core_tree_view.expand(index)
            # Expand the core item to show its properties
            core_index = self.soc_core_model.indexFromItem(core_item)
            self.soc_core_tree_view.expand(core_index)
            
            print(f"Added core: {core_name} to SoC: {soc_item.text()}")
            print(f"Core properties: {core_properties}")
    
    def remove_core(self):
        """Remove the selected core"""
        if not self.soc_core_tree_view:
            return
            
        index = self.soc_core_tree_view.currentIndex()
        if not index.isValid() or not index.parent().isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Required", 
                                        "Please select a core to remove.")
            return
            
        reply = QtWidgets.QMessageBox.question(
            self, "Confirm Removal", 
            "Are you sure you want to remove the selected core?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            # Get the parent item (SoC) and remove the core from it
            parent_index = index.parent()
            parent_item = self.soc_core_model.itemFromIndex(parent_index)
            if parent_item:
                parent_item.removeRow(index.row())
    
    def add_board(self):
        """Add a new board to the list"""
        text, ok = QtWidgets.QInputDialog.getText(self, "Add Board", "Enter board name:")
        if ok and text:
            item = QtGui.QStandardItem(text)
            self.board_model.appendRow(item)
            print(f"Added board: {text}")
    
    def remove_board(self):
        """Remove the selected board"""
        if not self.board_list_view:
            return
            
        indexes = self.board_list_view.selectedIndexes()
        if not indexes:
            QtWidgets.QMessageBox.warning(self, "Selection Required", 
                                        "Please select a board to remove.")
            return
            
        reply = QtWidgets.QMessageBox.question(
            self, "Confirm Removal", 
            "Are you sure you want to remove the selected board?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            for index in sorted(indexes, key=lambda x: x.row(), reverse=True):
                self.board_model.removeRow(index.row())
    
    def get_config_data(self):
        """Get configuration data from the dialog"""
        print("Getting configuration data...")
        
        # Get core name and description
        core_name = "Default Core"
        description = "Default core configuration"
        
        core_name_edit = self.findChild(QtWidgets.QLineEdit, "core_name_edit")
        description_edit = self.findChild(QtWidgets.QTextEdit, "description_edit")
        
        print(f"Core name edit found: {core_name_edit is not None}")
        print(f"Description edit found: {description_edit is not None}")
        
        if core_name_edit:
            core_name = core_name_edit.text()
        
        if description_edit:
            description = description_edit.toPlainText()
        
        # Get image types from the model
        image_types = []
        for row in range(self.image_type_model.rowCount()):
            index = self.image_type_model.index(row, 0)
            image_types.append(self.image_type_model.data(index))
        
        print(f"Image types: {image_types}")
        
        # Get SoCs and cores from the model with core properties
        socs = []
        cores = {}
        core_properties = {}
        
        for soc_row in range(self.soc_core_model.rowCount()):
            soc_index = self.soc_core_model.index(soc_row, 0)
            soc_item = self.soc_core_model.itemFromIndex(soc_index)
            soc_name = self.soc_core_model.data(soc_index)
            
            socs.append(soc_name)
            cores[soc_name] = []
            core_properties[soc_name] = {}
            
            # Get cores for this SoC
            for core_row in range(soc_item.rowCount()):
                core_item = soc_item.child(core_row)
                core_index = core_item.index()
                core_name = self.soc_core_model.data(core_index)
                cores[soc_name].append(core_name)
                
                # Get core properties if available
                props = core_item.data(QtCore.Qt.UserRole)
                if props:
                    core_properties[soc_name][core_name] = props
                else:
                    core_properties[soc_name][core_name] = {'name': core_name}
        
        print(f"SoCs: {socs}")
        print(f"Cores: {cores}")
        print(f"Core properties: {core_properties}")
        
        # Get boards from the model
        boards = []
        for row in range(self.board_model.rowCount()):
            index = self.board_model.index(row, 0)
            boards.append(self.board_model.data(index))
        
        print(f"Boards: {boards}")
        
        # Create config data dictionary
        config_data = {
            'core_name': core_name,
            'description': description,
            'image_types': image_types,
            'socs': socs,
            'cores': cores,
            'core_properties': core_properties,
            'boards': boards
        }
        
        print(f"Returning config data: {config_data}")
        return config_data

    def populate_from_existing_data(self, config_data):
        """Populate the dialog with existing configuration data"""
        print(f"Populating dialog with existing data: {config_data}")
        
        # Set core name and description
        core_name_edit = self.findChild(QtWidgets.QLineEdit, "core_name_edit")
        description_edit = self.findChild(QtWidgets.QTextEdit, "description_edit")
        
        if core_name_edit and 'core_name' in config_data:
            core_name_edit.setText(config_data['core_name'])
        
        if description_edit and 'description' in config_data:
            description_edit.setPlainText(config_data['description'])
        
        # Populate image types
        if 'image_types' in config_data and self.image_type_model:
            for image_type in config_data['image_types']:
                item = QtGui.QStandardItem(image_type)
                self.image_type_model.appendRow(item)
        
        # Populate SoCs and cores with their properties
        if 'socs' in config_data and 'cores' in config_data and self.soc_core_model:
            core_properties = config_data.get('core_properties', {})
            
            for soc in config_data['socs']:
                soc_item = QtGui.QStandardItem(soc)
                
                # Add cores for this SoC if available
                if soc in config_data['cores']:
                    for core in config_data['cores'][soc]:
                        # Create core item
                        core_item = QtGui.QStandardItem(core)
                        
                        # Add core properties if available
                        if soc in core_properties and core in core_properties[soc]:
                            props = core_properties[soc][core]
                            core_item.setData(props, QtCore.Qt.UserRole)
                            
                            # Add child items for each property to display in tree view
                            for prop_name, prop_value in props.items():
                                if prop_name != 'name':  # Name is already the item text
                                    prop_item = QtGui.QStandardItem(f"{prop_name}: {prop_value}")
                                    core_item.appendRow(prop_item)
                        else:
                            # Create a minimal properties dict if none exists
                            core_item.setData({'name': core}, QtCore.Qt.UserRole)
                        
                        soc_item.appendRow(core_item)
                
                self.soc_core_model.appendRow(soc_item)
                
                # Expand the SoC item to show cores
                if self.soc_core_tree_view:
                    index = self.soc_core_model.indexFromItem(soc_item)
                    self.soc_core_tree_view.expand(index)
                    
                    # Expand core items to show properties
                    for row in range(soc_item.rowCount()):
                        core_index = self.soc_core_model.index(row, 0, index)
                        self.soc_core_tree_view.expand(core_index)
        
        # Populate boards
        if 'boards' in config_data and self.board_model:
            for board in config_data['boards']:
                item = QtGui.QStandardItem(board)
                self.board_model.appendRow(item)