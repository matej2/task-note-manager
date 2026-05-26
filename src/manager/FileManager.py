import webbrowser
from io import TextIOWrapper
from typing import Any, IO

from src.manager.ConfigManager import ConfigManager


class FileManager:

    def __init__(self, config: ConfigManager) -> None:
        self.full_path = config.full_path

        with open(self.full_path, "a") as f:
            f.write("")

    def get_read_wrapper(self) -> TextIOWrapper | IO[Any]:
        return open(self.full_path, "r")

    def get_write_wrapper(self) -> TextIOWrapper | IO[Any]:
        return open(self.full_path, "w")

    def open_file_in_ext_app(self):
        webbrowser.open(self.full_path)

