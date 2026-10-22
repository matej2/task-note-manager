import os
from io import TextIOWrapper
from typing import Any, IO, Type

import yaml
from yaml import SafeLoader

from manager.ConfigManager import ConfigManager
from models.Config import Config
from utils.FileUtils import FileUtils
from utils.YamlUtils import YamlUtils


class ConfigFileManager:
    def __init__(self):
        self.__CONFIG_FULL_PATH = os.path.join(FileUtils.get_working_dir(), "task_notes_conf.yaml")
        self.config = Config()

        # Creates a file if it does not exist
        with open(self.__CONFIG_FULL_PATH, "a") as f:
            f.write("")

    @staticmethod
    def config_representer(dumper, data: Config):
        return dumper.represent_mapping("!Config", data.__dict__)

    @staticmethod
    def get_loader() -> Type[SafeLoader]:
        loader = yaml.SafeLoader
        loader.add_constructor("!Config", YamlUtils.config_constructor)
        return loader

    def read_config_from_file_async_direct(self) -> None:
        yaml.add_representer(Config, self.config_representer)
        with open(self.__CONFIG_FULL_PATH, "r") as file:
            config = yaml.load(file, Loader=self.get_loader())
            if config is not None:
                self.config = config
            else:
                self.config = Config()
                self.__write_data_to_file_direct()

    def __write_data_to_file_direct(self):
        with open(self.__CONFIG_FULL_PATH, "w") as file:
            yaml.dump(self.config, file, allow_unicode=True)

