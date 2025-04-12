from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from converters.base_converter import BaseConverter


class BaseConverterGUI:
    def __init__(self, converter: BaseConverter):
        self.converter = converter

    def open_converter(self, parent=None):
        self.converter_dialog = QDialog(parent)
        self.converter_dialog.setWindowTitle(f"{self.converter.__class__.__name__}")

        layout = QVBoxLayout()

        # Create combo boxes and input fields
        self.combo1, self.input1 = QComboBox(), QLineEdit()
        self.combo2, self.input2 = QComboBox(), QLineEdit()
        self.input1.setPlaceholderText("0")
        self.input2.setPlaceholderText("0")

        # Add units to combo boxes with tooltips
        for unit in self.converter.units:
            for combo in (self.combo1, self.combo2):
                combo.addItem(unit.name)
                combo.setItemData(combo.count() - 1, unit.description, Qt.ToolTipRole)

        # Create input rows
        layout.addLayout(self._make_row(self.combo1, self.input1))
        layout.addLayout(self._make_row(self.combo2, self.input2))

        self.converter_dialog.setLayout(layout)

        # Conversion dispatcher
        def convert(source_input, source_combo, target_input, target_combo):
            try:
                value = source_input.text() if source_input.text().strip() else "0"
                result = self.converter.convert(value, source_combo.currentText(), target_combo.currentText())
                target_input.blockSignals(True)
                target_input.setText(str(result))
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

        self.converter_dialog.exec_()

    def _make_row(self, combo: QComboBox, input_field: QLineEdit) -> QHBoxLayout:
        row = QHBoxLayout()
        row.addWidget(combo)
        row.addWidget(input_field)
        return row
