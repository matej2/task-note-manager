import re
from datetime import datetime, date, timedelta

from src.export.IOdsTabExport import IOdsTabExport
from src.export.OdsTabExportBase import OdsTabExportBase
from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager
from src.manager.TaskManager import TaskManager
from src.models.LocalizedDate import LocalizedDate
from src.models.NoteEntry import NoteEntry
from src.models.Task import Task


class NoteByTaskNameByDate(IOdsTabExport):
    def __init__(self, config_manager: ConfigManager, data_manager: DataManager, task_manager: TaskManager) -> None:
        self.config_manager = config_manager
        self.data_manager = data_manager
        self.task_manager = task_manager

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
            response.append(r.name)

        return response

    def __get_week_dates(self) -> list[date]:
        date_list = []
        today_date = datetime.now()

        for i in range(0, 7):
            week_day = LocalizedDate(self.config_manager.date_format, today_date - timedelta(days=i))
            date_list.append(week_day)
        return list(reversed(date_list))

    async def run_export(self) -> None:

        note_list = await self.data_manager.read_data_from_file_async_direct()
        first_row = self.add_header()

        for date_index, date_value in enumerate(first_row):
            for note in note_list.notes:
                self.__process_data_for_date(note, date_index, date_value, first_row)


    def add_header(self):
        date_list = self.__get_week_dates()

        first_row = list(map(lambda x: str(x), date_list))
        first_row.insert(0,'')
        OdsTabExportBase.add_sheet_row(first_row, self.config_manager.export_file_tab_name_task_names)
        return first_row


    def __process_data_for_date(self, note: NoteEntry, date_index: int, date_value: str, first_row) -> None:
        tasks_data = []

        tasks_data.extend(self.__extract_task_data(note.done))
        tasks_data.extend(self.__extract_task_data(note.in_progress))
        tasks_data.extend(self.__extract_task_data(note.problems))

        for task in tasks_data:
            result = [task.name]

            if note.date == date_value:
                for _ in range(date_index-1):
                    result.insert(1, '')
                result.append(task.description)
                OdsTabExportBase.add_sheet_row(result, self.config_manager.export_file_tab_name_task_names)

        OdsTabExportBase.save_as_ordered_dict()
