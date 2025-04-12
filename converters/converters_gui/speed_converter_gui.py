from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from converters.speed_converter import SpeedConverter
from converters.converters_gui.linear_converter_gui import LinearConverterGUI


class SpeedConverterGUI(LinearConverterGUI):
    def __init__(self):
        super().__init__(SpeedConverter())

    def open_converter(self, parent=None):
        self.converter_dialog = QDialog(parent)
        self.converter_dialog.setWindowTitle(f"{self.converter.__class__.__name__}")

        layout = QVBoxLayout()

        # UI Elements
        self.length_from = QComboBox()
        self.time_from = QComboBox()
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("0")

        self.length_to = QComboBox()
        self.time_to = QComboBox()
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("0")

        # Populate combo boxes
        for unit in self.converter.length_converter.units:
            for combo in (self.length_from, self.length_to):
                combo.addItem(unit.name)
                combo.setItemData(combo.count() - 1, unit.description, Qt.ToolTipRole)

        for unit in self.converter.time_converter.units:
            for combo in (self.time_from, self.time_to):
                combo.addItem(unit.name)
                combo.setItemData(combo.count() - 1, unit.description, Qt.ToolTipRole)

        # Layout: input 1
        layout.addLayout(self._make_speed_row(self.length_from, self.time_from, self.input1))
        # Layout: input 2
        layout.addLayout(self._make_speed_row(self.length_to, self.time_to, self.input2))

        self.converter_dialog.setLayout(layout)

        # Conversion dispatcher
        def convert(source_input, source_length, source_time, target_input, target_length, target_time):
            try:
                value = float(source_input.text() if source_input.text().strip() else "0")
                result = round(
                    self.converter.convert(
                        value,
                        source_length.currentText(), target_length.currentText(),
                        source_time.currentText(), target_time.currentText()
                    ), 10
                )
                target_input.blockSignals(True)
                target_input.setText(str(result) if result != 0 else "")
                target_input.blockSignals(False)
            except ValueError:
                target_input.blockSignals(True)
                target_input.setText("Invalid")
                target_input.blockSignals(False)

        # Signal connections
        self.input1.textChanged.connect(
            lambda: convert(
                self.input1, self.length_from, self.time_from,
                self.input2, self.length_to, self.time_to
                )
            )

        self.input2.textChanged.connect(
            lambda: convert(
                self.input2, self.length_to, self.time_to,
                self.input1, self.length_from, self.time_from
                )
            )

        self.length_from.currentTextChanged.connect(
            lambda: convert(
                self.input2, self.length_to, self.time_to,
                self.input1, self.length_from, self.time_from
                )
            )

        self.length_to.currentTextChanged.connect(
            lambda: convert(
                self.input1, self.length_from, self.time_from,
                self.input2, self.length_to, self.time_to
                )
            )

        self.time_from.currentTextChanged.connect(
            lambda: convert(
                self.input2, self.length_to, self.time_to,
                self.input1, self.length_from, self.time_from
                )
            )

        self.time_to.currentTextChanged.connect(
            lambda: convert(
                self.input1, self.length_from, self.time_from,
                self.input2, self.length_to, self.time_to
                )
            )

        # Initial conversion
        convert(self.input1, self.length_from, self.time_from, self.input2, self.length_to, self.time_to)

        self.converter_dialog.exec_()

    def _make_speed_row(self, length_combo: QComboBox, time_combo: QComboBox, input_field: QLineEdit) -> QHBoxLayout:
        row = QHBoxLayout()
        row.addWidget(length_combo)
        row.addWidget(QLabel(" / "))
        row.addWidget(time_combo)
        row.addWidget(input_field)
        return row
