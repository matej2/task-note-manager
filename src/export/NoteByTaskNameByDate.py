from datetime import datetime, date, timedelta

from src.export.IOdsTabExport import IOdsTabExport
from src.export.OdsTabExportBase import OdsTabExportBase
from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager
from src.manager.TaskManager import TaskManager
from src.models.LocalizedDate import LocalizedDate
from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList


class NoteByTaskNameByDate(IOdsTabExport):
    def __init__(self, config_manager: ConfigManager, data_manager: DataManager, task_manager: TaskManager) -> None:
        self.config_manager = config_manager
        self.data_manager = data_manager
        self.task_manager = task_manager

    def __get_week_dates(self) -> list[LocalizedDate]:
        today_date = datetime.now()

        date_list = [
            LocalizedDate(self.config_manager.DATE_FORMAT, today_date - timedelta(days=i))
            for i in range(365)
        ]

        return list(reversed(date_list))

    def run_export(self, current_data: NoteList) -> None:
        task_name_to_date = dict(dict(str()))


        for date, task_types in OdsTabExportBase.get_sheet_data_grouped().items():

            for task_type_name, task_type in task_types.items():
                for task_name, task_description in task_type.items():
                    if task_name not in task_name_to_date.keys():
                        task_name_to_date[task_name] = dict()
                    if date not in task_name_to_date[task_name]:
                        task_name_to_date[task_name][date] = f"{task_type_name}: {''.join(task_description)}\n"
                    else:
                        task_name_to_date[task_name][date] += f"{task_type_name}: {''.join(task_description)}\n"



        lines = list(list())
        key_index = 1
        all_date_values = [
            x for x in OdsTabExportBase.get_sheet_data_grouped().keys()]
        all_date_values.insert(0, '')
        lines.append(all_date_values)

        for task_name, task_dates in task_name_to_date.items():
            line = ['' for _ in all_date_values]
            line[0] = task_name

            for task_date, description in task_dates.items():
                if task_date not in all_date_values:
                    raise RuntimeError(f'Task date {task_date} not available')
                date_index = all_date_values.index(task_date)
                line[date_index] = description
                key_index += 1
            lines.append(line)
            line = list()

        OdsTabExportBase.save_lines(self.config_manager.EXPORT_TAB_NAME_TASK_NAMES, lines)


    def get_header(self):
        date_list = self.__get_week_dates()

        first_row = list(map(lambda x: str(x), date_list))
        first_row.insert(0,'')
        return first_row

    def save_as_table_status_by_date(self) -> None:
        lines = list()
        lines.append(self.get_header())

        for date, task_type in OdsTabExportBase.get_sheet_data_grouped().items():
            lines.append([
                date,
                self.format_task(task_type.get(self.done_label)),
                self.format_task(task_type.get(self.in_progress_label)),
                self.format_task(task_type.get(self.problems_label)),
            ])

        OdsTabExportBase.save_lines(self.config_manager.EXPORT_TAB_NAME_DEFAULT, lines)


    def __process_data_for_date(self, note: NoteEntry, date_index: int, date_value: str) -> None:
        for task in self.task_manager.get_tasks_from_note_entry(note):
            result = [task.name]

            if note.date == date_value:
                for _ in range(date_index-1):
                    result.insert(1, '')
                result.append(task.description)
                OdsTabExportBase.add_sheet_row(result, self.config_manager.EXPORT_TAB_NAME_TASK_NAMES)