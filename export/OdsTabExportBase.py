from collections import OrderedDict
from pyexcel_ods3 import save_data

from ConfigManager import ConfigManager
from DataManager import DataManager


class OdsTabExportBase:
    def __init__(self, config_manager: ConfigManager, data_manager: DataManager):
        self.config_manager = config_manager
        self._sheet_data = None

    def __save_as_ordered_dict(self) -> None:
        input_data = OrderedDict(self._sheet_data)
        save_data(self.config_manager.export_file_name, input_data)

    def __add_sheet_row(self, data: list[object], tab: str) -> None:
        curr_data = self._sheet_data.get(tab, list())

        if len(data) == 0:
            data = self.config_manager.export_empty_row

        curr_data.append(data)

        self._sheet_data.update({tab: curr_data})
        self.__save_as_ordered_dict()

    def __add_sheet_column(self, data: list[object], tab: str, column: int) -> None:
        curr_data = self._sheet_data.get(tab, list())

        if len(data) == 0:
            data = self.config_manager.export_empty_row

        for i in curr_data:
            curr_data[i].insert(column, data[i])

        self._sheet_data.update({tab: curr_data})
        self.__save_as_ordered_dict()
