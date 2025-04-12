import xml.etree.ElementTree as ET
import os
from converters.linear_converter import LinearConverter
from units.linear_unit import LinearUnit
from PyQt5.QtWidgets import *

class XMLConverterLoader:
    """
    A class to load linear converter data from an XML file and construct LinearConverter objects.
    """
    def __init__(self, xml_file: str):
        self.xml_file = xml_file
        self.ensure_xml_file()
        self.converters = self.load_converters_from_xml()

    def ensure_xml_file(self):
        """
        Ensures that the XML file exists and is not empty.
        If it doesn't exist, create it with a root element.
        If it's empty, write a valid XML structure.
        """
        if not os.path.exists(self.xml_file):
            self.create_empty_xml()
        elif os.path.getsize(self.xml_file) == 0:
            self.create_empty_xml()

    def create_empty_xml(self):
        """
        Creates an empty XML file with a root element.
        """
        root = ET.Element("converters")
        tree = ET.ElementTree(root)
        with open(self.xml_file, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)

    def load_converters_from_xml(self):
        """
        Loads the converter definitions from the XML file.
        Returns a list of LinearConverter objects.
        """
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
        except ET.ParseError:
            self.create_empty_xml()
            tree = ET.parse(self.xml_file)
            root = tree.getroot()

        converters = []

        for converter_element in root.findall('converter'):
            converter_name = converter_element.get('name')  # Get the name of the converter
            units = []

            # Collect the units for the converter
            for unit_element in converter_element.findall('unit'):
                name = unit_element.find('name').text
                description = unit_element.find('description').text if unit_element.find('description') is not None else None
                factor = float(unit_element.find('factor').text)
                units.append(LinearUnit(name, description, factor))

            # Create a LinearConverter object for this converter and add it to the list
            converters.append({
                "name": converter_name,
                "converter": LinearConverter(units)
            })

        return converters

    def get_converters(self):
        """
        Returns the list of loaded LinearConverter objects.
        """
        return self.converters

    def save_converter_to_xml(self, name, units):
        """
        Saves a new custom converter with its units to the XML file.
        :param name: Name of the converter
        :param units: List of unit dictionaries with 'name' and 'factor' keys
        """
        if not name or not units:
            raise ValueError("Converter name and units must be provided.")

        if os.path.exists(self.xml_file):
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
        else:
            root = ET.Element("converters")
            tree = ET.ElementTree(root)

        # Check for duplicate converters
        if any(converter.get("name") == name for converter in root.findall("converter")):
            raise ValueError(f"A converter with the name '{name}' already exists.")

        # Create a new converter element
        converter_element = ET.Element("converter", name=name)
        for unit in units:
            unit_element = ET.SubElement(converter_element, "unit")
            ET.SubElement(unit_element, "name").text = unit["name"]
            ET.SubElement(unit_element, "factor").text = str(unit["factor"])

        root.append(converter_element)

        # Write back to the XML file
        with open(self.xml_file, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)

    def delete_converter_from_xml(self, name):
        """
        Deletes a converter from the XML file by its name.
        :param name: Name of the converter to delete
        """
        if not name:
            raise ValueError("Converter name must be provided.")

        if not os.path.exists(self.xml_file):
            raise ValueError("XML file not found.")

        tree = ET.parse(self.xml_file)
        root = tree.getroot()

        # Find the converter to delete
        for converter in root.findall("converter"):
            if converter.get("name") == name:
                root.remove(converter)

                # Save the updated XML
                with open(self.xml_file, "wb") as f:
                    tree.write(f, encoding="utf-8", xml_declaration=True)

                return  # Exit after deletion

        raise ValueError(f"Converter '{name}' not found.")


    def update_converter_in_xml(self, name, units):
        """
        Updates an existing converter's units in the XML file.
        :param name: Name of the converter to update
        :param units: List of unit dictionaries with 'name' and 'factor' keys
        """
        if not name or not units:
            raise ValueError("Converter name and units must be provided.")

        if not os.path.exists(self.xml_file):
            raise ValueError("XML file not found.")

        tree = ET.parse(self.xml_file)
        root = tree.getroot()

        # Find the existing converter
        for converter in root.findall("converter"):
            if converter.get("name") == name:
                # Remove existing units
                for unit in converter.findall("unit"):
                    converter.remove(unit)

                # Add new units
                for unit in units:
                    unit_element = ET.SubElement(converter, "unit")
                    ET.SubElement(unit_element, "name").text = unit["name"]
                    ET.SubElement(unit_element, "factor").text = str(unit["factor"])

                # Save the updated XML
                with open(self.xml_file, "wb") as f:
                    tree.write(f, encoding="utf-8", xml_declaration=True)

                return  # Exit after updating

        raise ValueError(f"Converter '{name}' not found.")

    def rename_converter_in_xml(self, old_name, new_name):
        """
        Renames a converter in the XML file.
        :param old_name: The current name of the converter
        :param new_name: The new name to assign
        """
        if not old_name or not new_name:
            raise ValueError("Both old and new converter names must be provided.")

        if not os.path.exists(self.xml_file):
            raise ValueError("XML file not found.")

        tree = ET.parse(self.xml_file)
        root = tree.getroot()

        # Check if the new name already exists
        if any(converter.get("name") == new_name for converter in root.findall("converter")):
            raise ValueError(f"A converter with the name '{new_name}' already exists.")

        # Find the converter to rename
        for converter in root.findall("converter"):
            if converter.get("name") == old_name:
                converter.set("name", new_name)  # Rename the converter

                # Save the updated XML
                with open(self.xml_file, "wb") as f:
                    tree.write(f, encoding="utf-8", xml_declaration=True)

                return  # Exit after renaming

        raise ValueError(f"Converter '{old_name}' not found.")


