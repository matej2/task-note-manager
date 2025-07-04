import re
from collections import OrderedDict
from datetime import datetime, timedelta
import datetime

from pyexcel_ods3 import save_data

from ConfigManager import ConfigManager
from DataManager import DataManager
from models.LocalizedDate import LocalizedDate
from models.NoteEntry import NoteEntry
from models.Task import Task


class ExportManager:

    def __init__(self, config_manager: ConfigManager, data_manager: DataManager) -> None:
        self.config_manager = config_manager
        self.data_manager = data_manager
        self._sheet_data = {}


    def __delete_file(self) -> None:
        import os
        if os.path.exists(self.config_manager.export_file_name):
            os.remove(self.config_manager.export_file_name)

    def __delete_data(self) -> None:
        self._sheet_data = {}

    @staticmethod
    def __is_array_empty(l: list):
        flag = True

        if len(l) != 0:
            for item in l:
                if len(item) > 0:
                    flag = False
        return flag


    def __add_sheet_row(self, data: list[object], tab: str) -> None:
        if tab in self._sheet_data.keys():
            curr_data = self._sheet_data.get(tab)
        else:
            curr_data = []

        if len(data) == 0:
            data = self.config_manager.export_empty_row

        curr_data.append(data)

        self._sheet_data.update({tab: curr_data})
        self.__save_as_ordered_dict()

    def __add_sheet_column(self, data: list[object], tab: str, column: int) -> None:
        data_to_add = []

        if tab in self._sheet_data.keys():
            curr_data = self._sheet_data.get(tab)
        else:
            curr_data = []

        if len(data) == 0:
            data_to_add = [self.config_manager.export_empty_row]
        else:
            data_to_add = data

        for i in range(0, len(curr_data)):
            curr_data[i].insert(column, data_to_add[i])

        self._sheet_data.update({tab: curr_data})
        self.__save_as_ordered_dict()

    def __save_as_ordered_dict(self) -> None:
        input_data = OrderedDict()
        input_data.update(self._sheet_data)
        save_data(self.config_manager.export_file_name, input_data)

    def export_data(self) -> None:
        self.__delete_file()
        self.__delete_data()

        note_list = self.data_manager._read_data_from_file()
        sheet_content = [
            self.config_manager.export_data_date,
            self.config_manager.export_data_done,
            self.config_manager.export_data_in_progress,
            self.config_manager.export_data_problems
        ]

        self.__add_sheet_row(sheet_content, self.config_manager.export_file_tab_name_default)

        for note in note_list.notes:
            sheet_content = [note.date, note.done, note.in_progress, note.problems]

        self.__add_sheet_row(sheet_content, self.config_manager.export_file_tab_name_default)
        self.__export_task_names()

    def __extract_task_data(self, note: str) -> list[Task]:
        result = re.findall(self.config_manager.task_name_regex, note)
        formatted_result = []

        for r in result:
            formatted_result.append(Task(r[0], r[1]))

        return formatted_result


    def extract_task_names(self, note: str) -> list[str]:
        result = self.__extract_task_data(note)

        response = []
        for r in result:
            response.append(list(r.keys())[0])

        return response

    def __get_week_dates(self) -> list[datetime.date]:
        date_list = []
        todays_date = datetime.datetime.now()

        for i in range(0, 7):
            week_day = LocalizedDate(self.config_manager.date_format, todays_date - timedelta(days=i))
            date_list.append(week_day)
        return list(reversed(date_list))

    def __export_task_names(self) -> None:
        date_list = self.__get_week_dates()
        first_row = ['']
        first_row.extend(date_list)

        for i,row in enumerate(first_row):
            first_row[i] = str(row)
        self.__add_sheet_row(first_row, self.config_manager.export_file_tab_name_task_names)

        task_descriptions = {}

        for date_index, date in enumerate(date_list):
            note_list = self.__get_data_for_date(date)

            # Collect task names from all fields
            tasks_data = []
            if len(note_list) > 0:
                for note in note_list:
                    tasks_data.extend(self.__extract_task_data(note.done))
                    tasks_data.extend(self.__extract_task_data(note.in_progress))
                    tasks_data.extend(self.__extract_task_data(note.problems))

            for task in tasks_data:
                if date in first_row:
                    column_index = first_row.index(date)
                    task_descriptions.get(task.name)[column_index] = task.description

                result = [task.name]
                for i in range(0, date_index):
                    result.insert(1, '')
                result.append(task.description)
                self.__add_sheet_row(result, self.config_manager.export_file_tab_name_task_names)



    def __get_data_for_date(self, date: datetime.date) -> list[NoteEntry] | list[None]:
        result = []
        note_list = self.data_manager._read_data_from_file()
        if note_list is not None:
            for note in note_list.notes:
                if note.date == str(date):
                    result.append(note)
        return result