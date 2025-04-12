from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from converters import (length_converter, area_converter, volume_converter,
                        data_converter, mass_converter, time_converter,
                        currency_converter, temperature_converter, numeral_system_converter,
                        base64_converter)
from converters.converters_gui import (base_converter_gui, linear_converter_gui, speed_converter_gui, custom_linear_converter_gui)
from converters.xml import xml_converter_loader
from settings.xml_manager import XMLManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unit Converter")
        self.setStyleSheet(self.load_styles())
        self.setMinimumSize(500, 500)
        self.xml_manager = XMLManager()
        self.init_ui()

    def load_styles(self): 
        return """
            QWidget {
                background-color: #ffffff;
                font-family: Arial, sans-serif;
                font-size: 14px;
                color: #333;
            }

            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #222;
            }

            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 5px;
                padding: 10px;
                border: none;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #005A9E;
            }

            QPushButton:pressed {
                background-color: #004280;
            }

            QLineEdit, QComboBox, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px;
                font-size: 14px;
                background-color: #f9f9f9;
            }

            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #0078D7;
                background-color: #ffffff;
            }

            QComboBox::drop-down {
                border: none;
            }

            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                background-color: white;
                selection-background-color: #0078D7;
                selection-color: white;
            }

            QTableWidget {
                border: 1px solid #ddd;
                gridline-color: #eee;
                selection-background-color: #0078D7;
                selection-color: white;
            }

            QTableWidget QHeaderView::section {
                background-color: #f3f3f3;
                padding: 8px;
                border: 1px solid #ddd;
                font-weight: bold;
            }

            QScrollBar:vertical, QScrollBar:horizontal {
                border: none;
                background: #f1f1f1;
                width: 10px;
                height: 10px;
            }

            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #0078D7;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
                background: #005A9E;
            }

            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
                border: none;
            }

            QTabWidget::pane {
                border: 1px solid #ddd;
                background: #ffffff;
            }

            QTabBar::tab {
                background: #f9f9f9;
                border: 1px solid #ddd;
                padding: 8px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }

            QTabBar::tab:selected {
                background: #0078D7;
                color: white;
                border-bottom: 2px solid #0078D7;
            }

            QStatusBar {
                background: #f1f1f1;
                border-top: 1px solid #ddd;
            }

            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                background: #f9f9f9;
                text-align: center;
            }

            QProgressBar::chunk {
                background: #0078D7;
            }
        """

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        self.standard_tab = self.create_standard_tab()
        self.custom_tab = self.create_custom_tab()
        self.settings_tab = self.create_settings_tab()

        self.tab_widget.addTab(self.standard_tab, "Standard Converters")
        self.tab_widget.addTab(self.custom_tab, "Custom Converters")
        self.tab_widget.addTab(self.settings_tab, "Settings")

        main_layout.addWidget(self.tab_widget)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_standard_tab(self):
        standard_tab = QWidget()
        layout = QVBoxLayout()
        scroll_area, button_container, button_layout = self.create_scroll_area()

        converters = [
            ("Length", linear_converter_gui.LinearConverterGUI(length_converter.LengthConverter())),
            ("Area", linear_converter_gui.LinearConverterGUI(area_converter.AreaConverter())),
            ("Volume", linear_converter_gui.LinearConverterGUI(volume_converter.VolumeConverter())),
            ("Data", linear_converter_gui.LinearConverterGUI(data_converter.DataConverter())),
            ("Mass", linear_converter_gui.LinearConverterGUI(mass_converter.MassConverter())),
            ("Time", linear_converter_gui.LinearConverterGUI(time_converter.TimeConverter())),
            ("Speed", speed_converter_gui.SpeedConverterGUI()),
            ("Temperature", linear_converter_gui.LinearConverterGUI(temperature_converter.TemperatureConverter())),
            ("Numeral system", base_converter_gui.BaseConverterGUI(numeral_system_converter.NumeralSystemConverter())),
            ("Base64", base_converter_gui.BaseConverterGUI(base64_converter.Base64Converter()))
        ]

        try:
            converters.append(("Currency", linear_converter_gui.LinearConverterGUI(currency_converter.CurrencyConverter())))
        except Exception:
            converters.append(("Currency", None))

        self.create_buttons(converters, button_layout)
        button_container.setLayout(button_layout)
        scroll_area.setWidget(button_container)
        layout.addWidget(scroll_area)
        standard_tab.setLayout(layout)
        return standard_tab

    def create_custom_tab(self):
        custom_tab = QWidget()
        layout = QVBoxLayout()
        scroll_area, button_container, button_layout = self.create_scroll_area()

        converter_loader = xml_converter_loader.XMLConverterLoader(self.xml_manager.get_custom_converters_path())
        custom_converters = converter_loader.get_converters()
        converters = [
            (converter_data["name"], custom_linear_converter_gui.CustomLinearConverterGUI(converter_data["converter"], converter_data["name"], converter_loader))
            for converter_data in custom_converters
        ]
        for converter in converters:
            converter[1].on_name_changed.add_listener(self.reload_custom_tab)
            converter[1].on_deleted.add_listener(self.reload_custom_tab)

        self.create_buttons(converters, button_layout)
        button_container.setLayout(button_layout)
        scroll_area.setWidget(button_container)
        layout.addWidget(scroll_area)

        create_button = QPushButton("Create New Custom Converter")
        create_button.clicked.connect(self.create_new_custom_converter)
        layout.addWidget(create_button)

        custom_tab.setLayout(layout)
        return custom_tab

    def create_new_custom_converter(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Create Custom Converter")
        dialog_layout = QVBoxLayout()

        # Input for converter name
        name_label = QLabel("Converter Name:")
        name_input = QLineEdit()
        dialog_layout.addWidget(name_label)
        dialog_layout.addWidget(name_input)

        # Input for units (comma-separated)
        units_label = QLabel("Units (name:factor, separated by commas):")
        units_input = QLineEdit()
        dialog_layout.addWidget(units_label)
        dialog_layout.addWidget(units_input)

        # Buttons
        save_button = QPushButton("Save")
    
        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        dialog_layout.addLayout(button_layout)

        dialog.setLayout(dialog_layout)

        # Handle button clicks
        save_button.clicked.connect(lambda: self.save_custom_converter(name_input.text(), units_input.text(), dialog))

        dialog.exec_()

    def save_custom_converter(self, name, units_text, dialog):
        if not name or not units_text:
            QMessageBox.warning(self, "Input Error", "Please provide a name and at least one unit.")
            return

        units = []
        try:
            for unit_entry in units_text.split(","):
                unit_name, factor = unit_entry.split(":")
                units.append({"name": unit_name.strip(), "factor": float(factor.strip())})
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid unit format. Use 'name:factor' (e.g., 'Meter:1, Kilometer:1000').")
            return

        xml_loader = xml_converter_loader.XMLConverterLoader(self.xml_manager.get_custom_converters_path())

        try:
            xml_loader.save_converter_to_xml(name, units)
            QMessageBox.information(self, "Success", "Custom Converter Created!")
            dialog.accept()
            self.reload_custom_tab()  # Reload custom converters
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))


    def create_settings_tab(self):
        settings_tab = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("Custom Converters Path:")
        self.path_display = QLineEdit(self.xml_manager.get_custom_converters_path())
        self.path_display.setReadOnly(True)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_for_custom_path)
        
        layout.addWidget(label)
        layout.addWidget(self.path_display)
        layout.addWidget(browse_button)
        settings_tab.setLayout(layout)
        return settings_tab

    def browse_for_custom_path(self):
        file_dialog = QFileDialog()
        path, _ = file_dialog.getOpenFileName(self, "Select Custom Converters File", "", "XML Files (*.xml)")
        if path:
            self.xml_manager.set_custom_converters_path(path)
            self.path_display.setText(path)
            self.reload_custom_tab()

    def reload_custom_tab(self):
        """
        Reloads the custom converters tab by updating only the button layout.
        """
        # Find the existing button layout
        custom_tab_layout = self.custom_tab.layout()
        if custom_tab_layout is None or custom_tab_layout.count() == 0:
            return

        # Locate the scroll area
        scroll_area = custom_tab_layout.itemAt(0).widget()
        if not isinstance(scroll_area, QScrollArea):
            return

        button_container = scroll_area.widget()
        if button_container is None:
            return

        button_layout = button_container.layout()
        if button_layout is None:
            return

        self.remove_all_widgets_from_layout(button_layout)

        # Reload converters and recreate buttons
        converter_loader = xml_converter_loader.XMLConverterLoader(self.xml_manager.get_custom_converters_path())
        custom_converters = converter_loader.get_converters()
        converters = [
            (converter_data["name"], custom_linear_converter_gui.CustomLinearConverterGUI(converter_data["converter"], converter_data["name"], converter_loader))
            for converter_data in custom_converters
        ]
        for converter in converters:
            converter[1].on_name_changed.add_listener(self.reload_custom_tab)
            converter[1].on_deleted.add_listener(self.reload_custom_tab)

        self.create_buttons(converters, button_layout)

    def remove_all_widgets_from_layout(self, layout):
        """
        Removes all widgets and sub-layouts from the given layout.
        """
        while layout.count():
            item = layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()  # Remove the widget
                else:
                    sub_layout = item.layout()
                    if sub_layout:
                        self.remove_all_widgets_from_layout(sub_layout)  # Recursively remove sub-layouts
                layout.removeItem(item)  # Remove the layout/item itself

    def create_scroll_area(self):
        scroll_area = QScrollArea()
        button_container = QWidget()
        button_layout = QVBoxLayout()
        scroll_area.setWidgetResizable(True)
        return scroll_area, button_container, button_layout

    def create_buttons(self, converters: linear_converter_gui.LinearConverterGUI, layout):
        COLS_COUNT = 3
        MAX_BUTTON_NAME_LENGTH = 18
        
        grid_layout = QGridLayout()
    
        for index, (name, converter) in enumerate(converters):
            row = index // COLS_COUNT # Determine the row
            col = index % COLS_COUNT # Determine the column

            button = QPushButton()
            button.setText(name[:MAX_BUTTON_NAME_LENGTH - 3] + "..." if len(name) > MAX_BUTTON_NAME_LENGTH else name)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            if converter is None:
                button.setEnabled(False)
            else:
                button.clicked.connect(lambda checked, conv=converter: conv.open_converter(self))

            grid_layout.addWidget(button, row, col)

        layout.addLayout(grid_layout)