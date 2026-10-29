import logging
from collections import OrderedDict

from pyexcel_ods3 import save_data

from manager.TaskManager import TaskManager
from models.Config import Config
from models.NoteEntry import NoteEntry
from models.NoteList import NoteList
from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager


class OdsTabExportBase:
    config_manager = ConfigManager()
    logger = logging.getLogger(__name__)
    data_manager = None
    _sheet_data: dict[str, list[list[str]]] = {}
    # Sheet data grouped by date - type - tasks - description
    __sheet_data_grouped: dict[str, dict[str, list[list[str]]]] = {}
    config_data = Config()

    @classmethod
    def get_sheet_data_grouped(cls):
        return cls.__sheet_data_grouped

    @classmethod
    def set_dependencies(cls, config_manager: ConfigManager, data_manager: DataManager, config_data: Config, task_manager: TaskManager) -> None:
        """Call only once per app execution"""
        cls.config_manager = config_manager
        cls.data_manager = data_manager
        cls.config_data = config_data
        cls.task_manager = task_manager

    @classmethod
    def save_as_ordered_dict(cls) -> None:
        input_data = OrderedDict(cls._sheet_data)
        save_data(cls.config_data.export_file_path, input_data)
        cls.logger.debug(f"Exported saved content to {cls.config_data.export_file_path}")

    @classmethod
    def save_lines(cls, tab_name: str, lines: list[list[str]]) -> None:
        input_data = OrderedDict({
            tab_name: lines
        })
        save_data(cls.config_data.export_file_path, input_data)
        cls.logger.debug(f"Exported saved content to {cls.config_data.export_file_path}")


    @classmethod
    def add_sheet_row(cls, data: list[str], tab: str) -> None:
        curr_data = cls._sheet_data.get(tab, list())
        curr_data.append(data)

        cls._sheet_data.update({tab: curr_data})

    @classmethod
    def add_task_data(cls, note_entry: NoteEntry) -> None:
        done_id = cls.config_manager.TASK_DATA_DONE.get("identifier")
        in_progress_id = cls.config_manager.TASK_DATA_IN_PROGRESS.get("identifier")
        problems_id = cls.config_manager.TASK_DATA_PROBLEMS.get("identifier")

        tasks_done = cls.task_manager.get_tasks_from_field("done", note_entry)
        tasks_in_progress = cls.task_manager.get_tasks_from_field("in_progress", note_entry)
        tasks_problems = cls.task_manager.get_tasks_from_field("problems", note_entry)

        sheet_data_date = cls.__sheet_data_grouped.get(note_entry.date, dict())

        sheet_data_task_type_done = sheet_data_date.get(done_id, dict())
        sheet_data_task_type_in_progress = sheet_data_date.get(in_progress_id, dict())
        sheet_data_task_type_problems = sheet_data_date.get(problems_id, dict())

        tasks_for_type_and_date: list

        for task in tasks_done:
            sheet_data_task_type_done[task.name] = task.description

        for task in tasks_in_progress:
            sheet_data_task_type_in_progress[task.name] = task.description

        for task in tasks_problems:
            sheet_data_task_type_problems[task.name] = task.description

        if not note_entry.date in cls.__sheet_data_grouped.keys():
            cls.__sheet_data_grouped[note_entry.date] = {}

        cls.__sheet_data_grouped[note_entry.date].update( {
            done_id: sheet_data_task_type_done,
            in_progress_id: sheet_data_task_type_in_progress,
            problems_id: sheet_data_task_type_problems
        })


    @classmethod
    def add_sheet_column(cls, tab: str, column: int, data: list[str]) -> None:
        curr_data = cls._sheet_data.get(tab, list())
        for i in curr_data:
            curr_data[i].insert(column, data[i])

        cls._sheet_data.update({tab: curr_data})

    @classmethod
    def delete_data(cls) -> None:
        cls._sheet_data = {}
        cls.__sheet_data_grouped = {}

