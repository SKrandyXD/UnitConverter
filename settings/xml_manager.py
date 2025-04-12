import os
import json

class XMLManager:
    SETTINGS_FILE = "config/config.json"

    def __init__(self):
        self.config = self.load_settings()

    def load_settings(self):
        if not os.path.exists(self.SETTINGS_FILE):
            self.config = {"custom_converters_path": "custom_converters.xml"}
            self.save_settings()
        else:
            with open(self.SETTINGS_FILE, "r") as file:
                self.config = json.load(file)
        return self.config

    def save_settings(self):
        os.makedirs(os.path.dirname(self.SETTINGS_FILE), exist_ok=True)
        with open(self.SETTINGS_FILE, "w") as file:
            json.dump(self.config, file, indent=4)

    def get_custom_converters_path(self):
        return self.config.get("custom_converters_path", "custom_converters.xml")

    def set_custom_converters_path(self, path):
        self.config["custom_converters_path"] = path
        self.save_settings()
