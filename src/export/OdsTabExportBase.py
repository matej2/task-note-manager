import logging
from collections import OrderedDict

from pyexcel_ods3 import save_data

from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager


class OdsTabExportBase:
    config_manager = ConfigManager()
    logger = logging.getLogger(__name__)
    data_manager = None
    _sheet_data: dict[str, list] = {}

    @classmethod
    def set_dependencies(cls, config_manager: ConfigManager, data_manager: DataManager) -> None:
        """Call only once per app execution"""
        cls.config_manager = config_manager
        cls.data_manager = data_manager

    @classmethod
    def save_as_ordered_dict(cls) -> None:
        input_data = OrderedDict(cls._sheet_data)
        save_data(cls.config_manager.EXPORT_FILE_NAME, input_data)

    @classmethod
    def add_sheet_row(cls, data: list[str], tab: str) -> None:
        curr_data = cls._sheet_data.get(tab, list())
        curr_data.append(data)

        cls._sheet_data.update({tab: curr_data})

    @classmethod
    def add_sheet_column(cls, tab: str, column: int, data: list[str]) -> None:
        curr_data = cls._sheet_data.get(tab, list())
        for i in curr_data:
            curr_data[i].insert(column, data[i])

        cls._sheet_data.update({tab: curr_data})

    @classmethod
    def delete_data(cls) -> None:
        cls._sheet_data = {}

