import os
import sys


class ConfigManager:
    def __init__(self):
        self.font_family = "TkDefaultFont"
        self.font_size_small = 8
        self.font_size_normal = 10
        self.date_format = "%d. %b. %Y"
        self.frequency_hours = 6
        self.task_name_regex = r"\s*([^:;]*):"

        # Export
        self.export_empty_row = "No data"
        self.export_file_name = os.path.join(ConfigManager._get_full_curr_dir_path(), "task_notes.ods")
        self.export_file_tab_name_default = "Default"
        self.export_file_tab_name_task_names = "Task names"
        self.export_data_date = "Date"
        self.export_data_done = "Done"
        self.export_data_in_progress = "In progress"
        self.export_data_problems = "Problems"
        self.full_path = os.path.join(ConfigManager._get_full_curr_dir_path(), "task_notes.yaml")

    @staticmethod
    def _get_full_curr_dir_path():
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
Output file: {}
Excel file: {}""".format(
            self.font_family,
            self.font_size_normal,
            self.date_format,
            self.frequency_hours,
            self.full_path,
            self.export_file_name)
