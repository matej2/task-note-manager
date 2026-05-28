import logging
import os
from collections import OrderedDict
from pyexcel_ods3 import save_data

from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager
from src.models.NoteList import NoteList


class OdsTabExportBase:
    config_manager = None
    logger = logging.getLogger(__name__)
    data_manager = None
    _sheet_data = {}
    current_data = NoteList(list())

    @classmethod
    def init(cls, config_manager: ConfigManager, data_manager: DataManager, current_data: NoteList) -> None:
        """Call only once per app execution"""
        cls.config_manager = config_manager
        cls.data_manager = data_manager
        cls.current_data = current_data


    @classmethod
    def save_as_ordered_dict(cls) -> None:
        input_data = OrderedDict(cls._sheet_data)
        save_data(cls.config_manager.EXPORT_FILE_NAME, input_data)

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
    def delete_data(cls) -> None:
        cls._sheet_data = {}

