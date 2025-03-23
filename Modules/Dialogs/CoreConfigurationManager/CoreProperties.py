from PyQt5 import QtWidgets, QtCore, QtGui, uic
import os

class CorePropertiesDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, core_data=None):
        super().__init__(parent)
        self.core_data = core_data or {}
        
        # Load the UI
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        ui_file = os.path.join(project_dir, "Cfg", "LayoutFiles", "Dialogs", "CorePropertiesDialog.ui")
        print(f"Loading CorePropertiesDialog UI file: {ui_file}")
        uic.loadUi(ui_file, self)
        
        # Apply dark theme style sheet
        self.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                color: #f0f0f0;
            }
            QLabel {
                color: #f0f0f0;
            }
            QLineEdit, QComboBox, QSpinBox {
                background-color: #3d3d3d;
                color: #f0f0f0;
                border: 1px solid #555555;
                padding: 4px;
                border-radius: 4px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 1px solid #7a7a7a;
            }
            QCheckBox {
                color: #f0f0f0;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #555555;
                background-color: #3d3d3d;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #555555;
                background-color: #007acc;
            }
            QPushButton {
                background-color: #3d3d3d;
                color: #f0f0f0;
                border: 1px solid #555555;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
        """)
        
        # Connect signals and slots
        self.ok_button = self.findChild(QtWidgets.QPushButton, "ok_button")
        self.cancel_button = self.findChild(QtWidgets.QPushButton, "cancel_button")
        
        if self.ok_button:
            self.ok_button.clicked.connect(self.accept)
        
        if self.cancel_button:
            self.cancel_button.clicked.connect(self.reject)
        
        # Populate with existing data if provided
        if core_data:
            self.populate_form(core_data)
        
        # Connect signal for the OS type combobox to show/hide custom OS field
        os_combo = self.findChild(QtWidgets.QComboBox, "os_combo")
        custom_os_edit = self.findChild(QtWidgets.QLineEdit, "custom_os_edit")
        
        if os_combo and custom_os_edit:
            os_combo.currentTextChanged.connect(lambda text: 
                custom_os_edit.setVisible(text == "Other"))
            
            # Connect to toggle Autosar/QNX checkboxes based on OS selection
            os_combo.currentTextChanged.connect(self.update_checkboxes_based_on_os)
        
        # Connect signal for the SOC family combobox to show/hide custom SOC field
        soc_family_combo = self.findChild(QtWidgets.QComboBox, "soc_family_combo")
        custom_soc_family_edit = self.findChild(QtWidgets.QLineEdit, "custom_soc_family_edit")
        
        if soc_family_combo and custom_soc_family_edit:
            soc_family_combo.currentTextChanged.connect(lambda text: 
                custom_soc_family_edit.setVisible(text == "Other"))
                
        # Connect checkbox signals to handle mutual exclusivity
        qnx_checkbox = self.findChild(QtWidgets.QCheckBox, "qnx_checkbox")
        autosar_checkbox = self.findChild(QtWidgets.QCheckBox, "autosar_checkbox")
        
        if qnx_checkbox and autosar_checkbox:
            qnx_checkbox.toggled.connect(lambda checked: 
                autosar_checkbox.setDisabled(checked))
            autosar_checkbox.toggled.connect(lambda checked: 
                qnx_checkbox.setDisabled(checked))
    
    def update_checkboxes_based_on_os(self, os_type):
        """Update the checkboxes based on OS selection"""
        qnx_checkbox = self.findChild(QtWidgets.QCheckBox, "qnx_checkbox")
        autosar_checkbox = self.findChild(QtWidgets.QCheckBox, "autosar_checkbox")
        
        if not qnx_checkbox or not autosar_checkbox:
            return
        
        # Handle Autosar OS type
        if os_type == "Autosar":
            autosar_checkbox.setChecked(True)
            autosar_checkbox.setEnabled(False)
            qnx_checkbox.setChecked(False)
            qnx_checkbox.setEnabled(False)
        # Handle QNX OS type
        elif os_type == "QNX":
            qnx_checkbox.setChecked(True)
            qnx_checkbox.setEnabled(False)
            autosar_checkbox.setChecked(False)
            autosar_checkbox.setEnabled(False)
        else:
            # For other OS types, enable both checkboxes
            qnx_checkbox.setEnabled(True)
            autosar_checkbox.setEnabled(True)
            
            # Respect mutual exclusivity
            if qnx_checkbox.isChecked():
                autosar_checkbox.setEnabled(False)
            elif autosar_checkbox.isChecked():
                qnx_checkbox.setEnabled(False)
    
    def populate_form(self, core_data):
        """Populate the form with existing core data"""
        # Set core name
        name_edit = self.findChild(QtWidgets.QLineEdit, "name_edit")
        if name_edit and 'name' in core_data:
            name_edit.setText(core_data['name'])
        
        # Set description
        description_edit = self.findChild(QtWidgets.QLineEdit, "description_edit")
        if description_edit and 'description' in core_data:
            description_edit.setText(core_data['description'])
        
        # Set master core checkbox
        master_checkbox = self.findChild(QtWidgets.QCheckBox, "master_checkbox")
        if master_checkbox and 'is_master_core' in core_data:
            master_checkbox.setChecked(core_data['is_master_core'])
        
        # Set OS type
        os_combo = self.findChild(QtWidgets.QComboBox, "os_combo")
        custom_os_edit = self.findChild(QtWidgets.QLineEdit, "custom_os_edit")
        
        if os_combo and 'os_type' in core_data:
            # Set the OS combo to the matching item or "Other"
            index = os_combo.findText(core_data['os_type'])
            if index >= 0:
                os_combo.setCurrentIndex(index)
            else:
                os_combo.setCurrentText("Other")
                # Set the custom OS field
                if custom_os_edit:
                    custom_os_edit.setText(core_data['os_type'])
        
        # Set SOC family
        soc_family_combo = self.findChild(QtWidgets.QComboBox, "soc_family_combo")
        custom_soc_family_edit = self.findChild(QtWidgets.QLineEdit, "custom_soc_family_edit")
        
        if soc_family_combo and 'soc_family' in core_data:
            # Set the SOC combo to the matching item or "Other"
            index = soc_family_combo.findText(core_data['soc_family'])
            if index >= 0:
                soc_family_combo.setCurrentIndex(index)
            else:
                soc_family_combo.setCurrentText("Other")
                # Set the custom SOC field
                if custom_soc_family_edit:
                    custom_soc_family_edit.setText(core_data['soc_family'])
        
        # Set QNX checkbox
        qnx_checkbox = self.findChild(QtWidgets.QCheckBox, "qnx_checkbox")
        if qnx_checkbox and 'is_qnx_core' in core_data:
            qnx_checkbox.setChecked(core_data['is_qnx_core'])
        
        # Set autosar checkbox
        autosar_checkbox = self.findChild(QtWidgets.QCheckBox, "autosar_checkbox")
        if autosar_checkbox and 'is_autosar_compliant' in core_data:
            autosar_checkbox.setChecked(core_data['is_autosar_compliant'])
        
        # Set simulation checkbox
        sim_checkbox = self.findChild(QtWidgets.QCheckBox, "sim_checkbox")
        if sim_checkbox and 'is_simulation_core' in core_data:
            sim_checkbox.setChecked(core_data['is_simulation_core'])
    
    def get_core_data(self):
        """Get the core data from the form"""
        core_data = {}
        
        # Get core name
        name_edit = self.findChild(QtWidgets.QLineEdit, "name_edit")
        if name_edit:
            core_data['name'] = name_edit.text()
        
        # Get description
        description_edit = self.findChild(QtWidgets.QLineEdit, "description_edit")
        if description_edit:
            core_data['description'] = description_edit.text()
        
        # Get master core checkbox
        master_checkbox = self.findChild(QtWidgets.QCheckBox, "master_checkbox")
        if master_checkbox:
            core_data['is_master_core'] = master_checkbox.isChecked()
        
        # Get OS type
        os_combo = self.findChild(QtWidgets.QComboBox, "os_combo")
        custom_os_edit = self.findChild(QtWidgets.QLineEdit, "custom_os_edit")
        
        if os_combo:
            os_type = os_combo.currentText()
            if os_type == "Other" and custom_os_edit and custom_os_edit.isVisible():
                os_type = custom_os_edit.text()
            core_data['os_type'] = os_type
        
        # Get SOC family
        soc_family_combo = self.findChild(QtWidgets.QComboBox, "soc_family_combo")
        custom_soc_family_edit = self.findChild(QtWidgets.QLineEdit, "custom_soc_family_edit")
        
        if soc_family_combo:
            soc_family = soc_family_combo.currentText()
            if soc_family == "Other" and custom_soc_family_edit and custom_soc_family_edit.isVisible():
                soc_family = custom_soc_family_edit.text()
            core_data['soc_family'] = soc_family
        
        # Get QNX checkbox
        qnx_checkbox = self.findChild(QtWidgets.QCheckBox, "qnx_checkbox")
        if qnx_checkbox:
            core_data['is_qnx_core'] = qnx_checkbox.isChecked()
        
        # Get autosar checkbox
        autosar_checkbox = self.findChild(QtWidgets.QCheckBox, "autosar_checkbox")
        if autosar_checkbox:
            core_data['is_autosar_compliant'] = autosar_checkbox.isChecked()
        
        # Get simulation checkbox
        sim_checkbox = self.findChild(QtWidgets.QCheckBox, "sim_checkbox")
        if sim_checkbox:
            core_data['is_simulation_core'] = sim_checkbox.isChecked()
        
        return core_data
    
    @staticmethod
    def get_core_properties(parent, core_data=None):
        """Static method to show the dialog and return the core properties"""
        dialog = CorePropertiesDialog(parent, core_data)
        result = dialog.exec_()
        
        if result == QtWidgets.QDialog.Accepted:
            return dialog.get_core_data()
        return None 