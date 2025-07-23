import os
import typing
import webbrowser

from ConfigManager import ConfigManager


class FileManager:

    def __init__(self, config: ConfigManager) -> None:
        self.full_path_yaml = config.full_path
        self.full_path_ods = config.export_file_name
        # Creates a file if it does not exist
        with open(self.full_path_yaml, "a") as f:
            f.write("")

    def get_read_instance(self) -> typing.TextIO:
        return open(self.full_path_yaml, "r")

    def get_write_instance(self) -> typing.TextIO:
        return open(self.full_path_yaml, "w")

    def open_file(self):
        webbrowser.open(self.full_path_yaml)

    def open_file_ods(self):
        os.startfile(self.full_path_ods)
