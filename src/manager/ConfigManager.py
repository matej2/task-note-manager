import logging
import os
import sys


class ConfigManager:
    def __init__(self):
        # Font
        self.FONT_FAMILY = "TkDefaultFont"
        self.FONT_SIZE_NORMAL = 10

        # Date, time
        self.DATE_FORMAT = "%d. %b. %Y"
        self.frequency_hours = 6
        self.TASK_NAME_REGEX = r"\s*([^:;]*)\s*:\s*([^:;]*)"

        # Excel export
        self.EXPORT_EMPTY_ROW = ["No data", ]
        self.EXPORT_FILE_NAME = os.path.join(ConfigManager._get_full_curr_dir_path(), "../../task_notes.ods")
        self.EXPORT_TAB_NAME_DEFAULT = "Default"
        self.EXPORT_TAB_NAME_TASK_NAMES = "Task names"

        #  Excel export headers
        self.EXPORT_TH_DATE = "Date"
        self.EXPORT_TH_DONE = "Done"
        self.EXPORT_TH_IN_PROGRESS = "In progress"
        self.EXPORT_TH_PROBLEMS = "Problems"

        # Yaml
        self.FULL_PATH = os.path.join(ConfigManager._get_full_curr_dir_path(), "../../task_notes.yaml")

        # Logging
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S")

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
            self.FONT_FAMILY,
            self.FONT_SIZE_NORMAL,
            self.DATE_FORMAT,
            self.frequency_hours,
            self.FULL_PATH,
            self.EXPORT_FILE_NAME)
