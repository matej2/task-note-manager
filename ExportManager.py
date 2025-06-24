import re
from collections import OrderedDict
from datetime import datetime, timedelta
import datetime

from pyexcel_ods3 import save_data

from ConfigManager import ConfigManager
from DataManager import DataManager
from models.NoteEntry import NoteEntry


class ExportManager:

    def __init__(self, config_manager: ConfigManager, data_manager: DataManager) -> None:
        self.config_manager = config_manager
        self.data_manager = data_manager
        self._sheet_data = {}

    @staticmethod
    def __is_array_empty(l: list):
        flag = True

        if len(l) != 0:
            for item in l:
                if len(item) > 0:
                    flag = False
        return flag

    def __add_sheet_row(self, data: list[list[str]], tab: str) -> None:
        if self.__is_array_empty(data):
            data = [[self.config_manager.export_empty_row]]
        self._sheet_data.update({tab: data})

    def __save_as_ordered_dict(self) -> None:
        input_data = OrderedDict()
        input_data.update(self._sheet_data)
        save_data(self.config_manager.export_file_name, input_data)

    def export_data(self) -> None:
        note_list = self.data_manager._read_data_from_file()
        sheet_content = [[
            self.config_manager.export_data_date,
            self.config_manager.export_data_done,
            self.config_manager.export_data_in_progress,
            self.config_manager.export_data_problems
        ]]

        for note in note_list.notes:
            new_line = [note.date, note.done, note.in_progress, note.problems]
            sheet_content.append(new_line)

        self.__add_sheet_row(sheet_content, self.config_manager.export_file_tab_name_default)
        self.__export_task_names()


    def extract_task_names(self, note: str) -> list[str]:
        result = re.findall(self.config_manager.task_name_regex, note)
        formatted_result = []

        for r in result:
            if r[0] != "":
                formatted_result.append(r[0])

            else:
                formatted_result.append(r[1])

        return formatted_result

    def __export_task_names(self) -> None:
        for i in range(0, 7):
            date = datetime.date.today() - timedelta(days=i)
            note_list = self.__get_data_for_date(date)
            if len(note_list) > 0:
                result = []
                for note in note_list:
                    result.extend(ExportManager.extract_task_names(self, note.done))
                    result.extend(ExportManager.extract_task_names(self, note.in_progress))
                    result.extend(ExportManager.extract_task_names(self, note.problems))

                self.__add_sheet_row([result], self.config_manager.export_file_tab_name_task_names)

        self.__save_as_ordered_dict()

    def __get_data_for_date(self, date: datetime.date) -> list[NoteEntry] | list[None]:
        result = []
        note_list = self.data_manager._read_data_from_file()
        date_str = date.strftime(self.config_manager.date_format)
        if note_list is not None:
            for note in note_list.notes:
                if note.date == date_str:
                    result.append(note)
        return result