from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from converters.linear_converter import LinearConverter
from converters.converters_gui.linear_converter_gui import LinearConverterGUI
from units.linear_unit import LinearUnit
from utilities.event import Event
from converters.xml.xml_converter_loader import XMLConverterLoader

class CustomLinearConverterGUI(LinearConverterGUI):
    def __init__(self, converter: LinearConverter, converter_name: str, xml_loader: XMLConverterLoader):
        super().__init__(converter)
        self.converter_name = converter_name
        self.on_name_changed = Event()
        self.on_deleted = Event()
        self.xml_loader = xml_loader

    def open_converter(self, parent=None):
        self.converter_dialog = QDialog(parent)
        self.converter_dialog.setWindowTitle(self.converter_name)

        layout = QVBoxLayout()

        # UI elements
        self.combo1, self.input1 = QComboBox(), QLineEdit()
        self.combo2, self.input2 = QComboBox(), QLineEdit()
        self.input1.setPlaceholderText("0")
        self.input2.setPlaceholderText("0")

        # Fill combo boxes with units
        for unit in self.converter.units:
            for combo in (self.combo1, self.combo2):
                combo.addItem(unit.name)
                combo.setItemData(combo.count() - 1, unit.description, Qt.ToolTipRole)

        # Layout rows
        layout.addLayout(self._make_row(self.combo1, self.input1))
        layout.addLayout(self._make_row(self.combo2, self.input2))

        # Conversion dispatcher
        def convert(source_input, source_combo, target_input, target_combo):
            try:
                value = source_input.text() if source_input.text().strip() else "0"
                result = round(float(self.converter.convert(value, source_combo.currentText(), target_combo.currentText())), 10)
                target_input.blockSignals(True)
                target_input.setText(str(result) if result != 0 else "")
                target_input.blockSignals(False)
            except ValueError:
                target_input.blockSignals(True)
                target_input.setText("Invalid")
                target_input.blockSignals(False)

        # Connect signals
        self.input1.textChanged.connect(lambda: convert(self.input1, self.combo1, self.input2, self.combo2))
        self.input2.textChanged.connect(lambda: convert(self.input2, self.combo2, self.input1, self.combo1))
        self.combo1.currentTextChanged.connect(lambda: convert(self.input2, self.combo2, self.input1, self.combo1))
        self.combo2.currentTextChanged.connect(lambda: convert(self.input1, self.combo1, self.input2, self.combo2))

        # Trigger initial conversion
        convert(self.input1, self.combo1, self.input2, self.combo2)

        # Edit button
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: self.open_edit_dialog(self.converter_dialog))
        layout.addWidget(edit_button)

        self.converter_dialog.setLayout(layout)
        self.converter_dialog.exec_()

    def _make_row(self, combo: QComboBox, input_field: QLineEdit) -> QHBoxLayout:
        row = QHBoxLayout()
        row.addWidget(combo)
        row.addWidget(input_field)
        return row

    def open_edit_dialog(self, parent):
        edit_dialog = QDialog(parent)
        edit_dialog.setWindowTitle(f"Edit {self.converter_name}")

        layout = QVBoxLayout()

        unit_list = QListWidget()
        for unit in self.converter.units:
            unit_list.addItem(f"{unit.name} ({unit.factor})")

        layout.addWidget(unit_list)

        button_layout = QHBoxLayout()

        rename_converter_button = QPushButton("Rename Converter") 
        delete_converter_button = QPushButton("Delete Converter")
        add_unit_button = QPushButton("Add Unit")
        delete_unit_button = QPushButton("Delete Unit")

        button_layout.addWidget(rename_converter_button)
        button_layout.addWidget(delete_converter_button)
        button_layout.addWidget(add_unit_button)
        button_layout.addWidget(delete_unit_button)

        layout.addLayout(button_layout)

        rename_converter_button.clicked.connect(lambda: self.rename_converter(edit_dialog))
        delete_converter_button.clicked.connect(lambda: self.delete_converter(edit_dialog))
        add_unit_button.clicked.connect(lambda: self.add_unit(unit_list, edit_dialog))
        delete_unit_button.clicked.connect(lambda: self.delete_unit(unit_list, edit_dialog))

        edit_dialog.setLayout(layout)
        edit_dialog.exec_()

    def add_unit(self, unit_list, parent):
        text, ok = QInputDialog.getText(
            parent, 
            "Add Unit", 
            "Enter unit (name:factor):"
        )

        if ok and ":" in text:
            try:
                name, factor = text.split(":")
                unit_list.addItem(f"{name.strip()} ({float(factor.strip())})")
                self.save_changes(unit_list)
            except ValueError:
                QMessageBox.warning(parent, "Error", "Invalid format. Use 'name:factor'.")

    def delete_unit(self, unit_list, parent):
        selected_item = unit_list.currentItem()
        if selected_item:
            reply = QMessageBox.question(
                parent, 
                "Delete Unit",
                f"Are you sure you want to delete '{selected_item.text()}'?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                unit_list.takeItem(unit_list.row(selected_item))
                self.save_changes(unit_list)

    def save_changes(self, unit_list):
        units = []
        for index in range(unit_list.count()):
            item_text = unit_list.item(index).text()
            name, factor = item_text.rsplit(" (", 1)
            factor = float(factor[:-1])  # Remove closing parenthesis
            units.append({"name": name.strip(), "factor": factor})

        try:
            self.xml_loader.update_converter_in_xml(self.converter_name, units)

            self.converter.units = [LinearUnit(unit['name'], None, unit['factor']) for unit in units]

            self.combo1.clear()
            self.combo2.clear()

            for unit in self.converter.units:
                self.combo1.addItem(unit.name)
                self.combo1.setItemData(self.combo1.count() - 1, unit.description, Qt.ToolTipRole)

            for unit in self.converter.units:
                self.combo2.addItem(unit.name)
                self.combo2.setItemData(self.combo2.count() - 1, unit.description, Qt.ToolTipRole)

        except ValueError as e:
            QMessageBox.warning(None, "Error", str(e))

    def rename_converter(self, parent):
        new_name, ok = QInputDialog.getText(
            parent, "Rename Converter", 
            "Enter new converter name:", 
            QLineEdit.Normal, self.converter_name
        )
        if ok and new_name.strip():
            old_name = self.converter_name
            self.converter_name = new_name.strip()

            try:
                self.xml_loader.rename_converter_in_xml(old_name, self.converter_name)
                self.on_name_changed.invoke()
            except ValueError as e:
                QMessageBox.warning(parent, "Error", str(e))

    def delete_converter(self, parent):
        """
        Deletes the current converter after confirmation.
        """
        reply = QMessageBox.question(
            parent, "Delete Converter",
            f"Are you sure you want to delete '{self.converter_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.xml_loader.delete_converter_from_xml(self.converter_name)
                parent.accept()
                self.converter_dialog.accept()
                self.on_deleted.invoke()
            except ValueError as e:
                QMessageBox.warning(parent, "Error", str(e))
