import logging
import os
import re
from collections import OrderedDict
from datetime import timedelta, datetime, date

from pyexcel_ods3 import save_data

from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager
from src.models.LocalizedDate import LocalizedDate
from src.models.NoteList import NoteList
from src.models.Task import Task


class ExportManager:

    def __init__(self, config_manager: ConfigManager, data_manager: DataManager):
        self.logger = logging.getLogger(__name__)
        self.config_manager = config_manager
        self.data_manager = data_manager
        self._sheet_data = {}


    def __delete_file(self) -> None:
        if os.path.exists(self.config_manager.export_file_name):
            os.remove(self.config_manager.export_file_name)

    def __delete_data(self) -> None:
        self._sheet_data = {}

    def __add_sheet_row(self, data: list[str], tab: str) -> None:
        curr_data = self._sheet_data.get(tab, list())
        curr_data.append(data)
        self._sheet_data.update({tab: curr_data})

    def __add_sheet_column(self, data: list[object], tab: str, column: int) -> None:
        curr_data = self._sheet_data.get(tab, list())

        if len(data) == 0:
            data = self.config_manager.export_empty_row

        for i in curr_data:
            curr_data[i].insert(column, data[i])

        self._sheet_data.update({tab: curr_data})
        self.__save_as_ordered_dict()

    def __save_as_ordered_dict(self) -> None:
        input_data = OrderedDict(self._sheet_data)
        save_data(self.config_manager.export_file_name, input_data)

    async def export_data(self) -> None:
        self.__delete_file()
        self.__delete_data()

        await self.__export_data_tasks_by_date()

    def __add_tasks_by_date_header(self):
        self.__add_sheet_row( [
            self.config_manager.export_th_date,
            self.config_manager.export_th_done,
            self.config_manager.export_th_in_progress,
            self.config_manager.export_th_problems
        ], self.config_manager.export_file_tab_name_default)

    async def __export_data_tasks_by_date(self) -> None:
        note_list = await self.data_manager.read_data_from_file_async_direct()

        self.__add_tasks_by_date_header()
        for note in iter(note_list.notes):
            self.__add_sheet_row(
                [note.date, note.done, note.in_progress, note.problems],
                self.config_manager.export_file_tab_name_default)

        self.__save_as_ordered_dict()
        self.logger.debug(f"Exported saved content to {self.config_manager.export_file_name}")

    def __extract_task_data(self, note: str) -> list[Task]:
        result = re.findall(self.config_manager.task_name_regex, note)
        formatted_result = []

        for r in result:
            formatted_result.append(Task(r[0], r[1]))

        return formatted_result

    # TODO: Implement Task manager
    def extract_task_names(self, note: str) -> list[str]:
        result = self.__extract_task_data(note)

        response = []
        for r in result:
            response.append(r.name)

        return response

    def __get_week_dates(self) -> list[date]:
        date_list = []
        today_date = datetime.now()

        for i in range(0, 7):
            week_day = LocalizedDate(self.config_manager.date_format, today_date - timedelta(days=i))
            date_list.append(week_day)
        return list(reversed(date_list))

    def __export_task_names(self) -> None:
        date_list = self.__get_week_dates()
        first_row = list(map(lambda x: str(x), date_list))

        self.__add_sheet_row(first_row, self.config_manager.export_file_tab_name_task_names)

        task_descriptions = dict(list())

        for date_index, date_value in enumerate(first_row):
            args = {
                'date_index': date_index,
                'date': date_value,
                'first_row': first_row,
                'task_descriptions': task_descriptions
            }

            # Extract
            #self.data_manager.read_data_from_file_async(self.__process_data_for_date, args)


    def __process_data_for_date(self, note_list: NoteList, args: dict[str, list]) -> None:
        tasks_data = []
        date_index = args.get('date_index', list())
        date_input = args.get('date')
        first_row = args.get('first_row', list())
        task_descriptions = args.get('task_descriptions', dict[str, list])

        if note_list is not None:
            for note in note_list.notes:
                tasks_data.extend(self.__extract_task_data(note.done))
                tasks_data.extend(self.__extract_task_data(note.in_progress))
                tasks_data.extend(self.__extract_task_data(note.problems))

        for task in tasks_data:
            if date_input in first_row:
                column_index = first_row.index(date_input)
                task_descriptions.get(task.name)[column_index] = task.description

            result = [task.name]
            for _ in range(date_index):
                result.insert(1, '')
            result.append(task.description)
            self.__add_sheet_row(result, self.config_manager.export_file_tab_name_task_names)
