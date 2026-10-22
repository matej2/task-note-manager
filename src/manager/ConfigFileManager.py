import os
from io import TextIOWrapper
from typing import Any, IO

import yaml

from manager.ConfigManager import ConfigManager
from models.Config import Config
from utils.FileUtils import FileUtils
from utils.YamlUtils import YamlUtils


class ConfigFileManager:
    def __init__(self):
        self.__CONFIG_FULL_PATH = os.path.join(FileUtils.get_working_dir(), "task_notes_conf.yaml")
        self.config = Config()

    def __get_config_read_wrapper(self) -> TextIOWrapper | IO[Any]:
        return open(self.__CONFIG_FULL_PATH, "r")

    async def read_config_from_file_async_direct(self) -> None:
        with self.__get_config_read_wrapper() as file:
            config = yaml.load(file, Loader=YamlUtils.get_loader())
            if config is not None:
                self.config = config
            else:
                self.config = Config()
