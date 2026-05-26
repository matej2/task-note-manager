import logging
import os
from collections import OrderedDict
from pyexcel_ods3 import save_data

from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager


class OdsTabExportBase:
    config_manager = None
    logger = logging.getLogger(__name__)
    data_manager = None
    _sheet_data = {}

    @classmethod
    def init(cls, config_manager: ConfigManager, data_manager: DataManager) -> None:
        """Nadomestek za __init__. Pokliče se enkrat ob zagonu aplikacije."""
        if cls.config_manager is None:
            cls.config_manager = config_manager
        if cls.data_manager is None:
            cls.data_manager = data_manager

    @classmethod
    def save_as_ordered_dict(cls) -> None:
        input_data = OrderedDict(cls._sheet_data)
        save_data(cls.config_manager.export_file_name, input_data)
        cls.__delete_data()

    @classmethod
    def add_sheet_row(cls, data: list[object], tab: str) -> None:
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
    def __delete_file(cls) -> None:
        if os.path.exists(cls.config_manager.export_file_name):
            os.remove(cls.config_manager.export_file_name)

    @classmethod
    def __delete_data(cls) -> None:
        cls._sheet_data = {}

