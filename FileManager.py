import typing
import webbrowser

from ConfigManager import ConfigManager


class FileManager:

    def __init__(self, config: ConfigManager) -> None:
        self.full_path = config.full_path
        # Creates a file if it does not exist
        with open(self.full_path, "a") as f:
            f.write("")

    def get_read_instance(self) -> typing.TextIO:
        return open(self.full_path, "r")

    def get_write_instance(self) -> typing.TextIO:
        return open(self.full_path, "w")

    def open_file(self):
        webbrowser.open(self.full_path)

