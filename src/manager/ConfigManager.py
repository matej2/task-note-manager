import logging
import os
import platform

from customtkinter import CTkFont as Font


class ConfigManager:
    def __init__(self):
        # Font
        self.FONT_FAMILY = "TkDefaultFont"
        self.REM_MULT = 14
        self.FONT_SIZE_LARGE = 1.3
        self.FONT_SIZE_NORMAL = 1
        self.FONT_SIZE_SMALL = 0.8

        # Date, time
        self.DATE_FORMAT = "%d. %b. %Y"
        self.frequency_hours = 6
        self.TASK_NAME_REGEX = r"\s*([^:;]*)\s*:\s*([^:;]*)"

        # Excel export
        self.EXPORT_EMPTY_ROW = ["No data", ]
        self.EXPORT_FILE_NAME = os.path.join(ConfigManager.get_full_curr_dir_path(), "../../task_notes.ods")
        self.EXPORT_TAB_NAME_DEFAULT = "Default"
        self.EXPORT_TAB_NAME_TASK_NAMES = "Task names"

        #  Excel export headers
        self.EXPORT_TH_DATE = "Date"
        self.EXPORT_TH_DONE = "Done"
        self.EXPORT_TH_IN_PROGRESS = "In progress"
        self.EXPORT_TH_PROBLEMS = "Problems"

        # Default padding
        self.NEW_NOTE_INPUT_PADX = 20
        self.NEW_NOTE_INPUT_PADY = 20
        self.NEW_NOTE_LABEL_PADX = 5
        self.NEW_NOTE_LABEL_PADY = 5
        self.BUTTON_BORDER_SPACING = 10
        self.BUTTON_PADX = 20
        self.BUTTON_PADY = 10

        #  Colors
        self.FRAME_BACKGROUND = "#EEEEEE"
        self.FRAME_BORDER = "#BDBDBD"
        self.SECONDARY_BUTTON_COLOR = "#1565C0"
        self.SECONDARY_BUTTON_COLOR_HOVER = "#0D47A1"
        self.PRIMARY_BUTTON_COLOR = "#388E3C"
        self.PRIMARY_BUTTON_COLOR_HOVER = "#2E7D32"

        # Yaml
        self.FULL_PATH = os.path.join(ConfigManager.get_full_curr_dir_path(), "task_notes.yaml")

        # Logging
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S")

    @staticmethod
    def get_full_curr_dir_path():
        if platform.system() == "Windows":
            os.makedirs(os.path.join(os.environ["APPDATA"], "TaskNoteManager"), exist_ok=True)
            return os.path.join(os.environ["APPDATA"], "TaskNoteManager")
        else:
            os.makedirs(os.path.join(os.path.expanduser("~"), ".TaskNoteManager"), exist_ok=True)
            return os.path.join(os.path.expanduser("~"), ".TaskNoteManager")

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

    def rem(self, val: float):
        return int(val * self.REM_MULT)

    def get_regular_font(self):
        return Font(
            family=self.FONT_FAMILY,
            size=self.rem(self.FONT_SIZE_NORMAL)
        )

    def get_large_font(self):
        return Font(
            family=self.FONT_FAMILY,
            size=self.rem(self.FONT_SIZE_LARGE)
        )

    def get_small_font(self):
        return Font(
            family=self.FONT_FAMILY,
            size=self.rem(self.FONT_SIZE_SMALL)
        )