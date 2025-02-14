import os
import sys


class ConfigManager:
    def __init__(self):
        self.font_family = "TkDefaultFont"
        self.font_size_small = 8
        self.font_size_normal = 10
        self.date_format = "%d. %b. %Y"
        self.frequency_hours = 6

        self.full_path = os.path.join(ConfigManager._get_full_path(), "task_notes.yaml")

    @staticmethod
    def _get_full_path():
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        return application_path

    def __str__(self):
        return """
Font family: {}
Font size: {}
Date format: {}
Frequency hours: {}
Output file: {}""".format(self.font_family, self.font_size_normal, self.date_format, self.frequency_hours, self.full_path)
