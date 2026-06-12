import os
import platform
import subprocess
import webbrowser
from io import TextIOWrapper
from typing import Any, IO

from src.manager.ConfigManager import ConfigManager


class FileManager:

    def __init__(self, config: ConfigManager) -> None:
        self.full_path = config.FULL_PATH

        # Creates a file if it does not exist
        with open(self.full_path, "a") as f:
            f.write("")

    def get_read_wrapper(self) -> TextIOWrapper | IO[Any]:
        return open(self.full_path, "r")

    def get_write_wrapper(self) -> TextIOWrapper | IO[Any]:
        return open(self.full_path, "w")

    def open_file_in_ext_app(self):
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', self.full_path))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(self.full_path)
        else:  # linux variants
            subprocess.call(('xdg-open', self.full_path))

