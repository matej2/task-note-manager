import logging
import os
import traceback
from collections import OrderedDict

from pyexcel_ods3 import save_data

from manager.TaskManager import TaskManager
from models.Config import Config
from models.NoteEntry import NoteEntry
from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager


class OdsTabExportBase:
    config_manager = ConfigManager()
    logger = logging.getLogger(__name__)
    data_manager = None
    # Sheet data grouped by date - type - tasks - description
    __sheet_data_grouped: dict[str, dict[str, list[list[str]]]] = {}
    __sheet_lines: dict[str, list[list[str]]] = {}
    config_data = None

    def __init__(self, config_manager: ConfigManager, data_manager: DataManager, config_data: Config, task_manager: TaskManager) -> None:
        """Call only once per app execution"""
        self.config_manager = config_manager
        self.data_manager = data_manager
        self.config_data = config_data
        self.task_manager = task_manager

    def get_sheet_data_grouped(self):
        return self.__sheet_data_grouped

    def save_lines(self, tab_name: str, lines: list[list[str]]) -> None:
        self.__sheet_lines.setdefault(tab_name, []).extend(lines)
        save_data(self.config_data.export_file_path, self.__sheet_lines)
        self.logger.debug(f"Exported saved content to {self.config_data.export_file_path}, tab namme: {tab_name}")

    def add_task_data(self, note_entry: NoteEntry) -> None:
        done_id = self.config_manager.TASK_DATA_DONE.get("identifier")
        in_progress_id = self.config_manager.TASK_DATA_IN_PROGRESS.get("identifier")
        problems_id = self.config_manager.TASK_DATA_PROBLEMS.get("identifier")

        tasks_done = self.task_manager.get_tasks_from_field("done", note_entry)
        tasks_in_progress = self.task_manager.get_tasks_from_field("in_progress", note_entry)
        tasks_problems = self.task_manager.get_tasks_from_field("problems", note_entry)

        sheet_data_date = self.__sheet_data_grouped.get(note_entry.date, dict())

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

        if not note_entry.date in self.__sheet_data_grouped.keys():
            self.__sheet_data_grouped[note_entry.date] = {}

        self.__sheet_data_grouped[note_entry.date].update( {
            done_id: sheet_data_task_type_done,
            in_progress_id: sheet_data_task_type_in_progress,
            problems_id: sheet_data_task_type_problems
        })

    def delete_data(self) -> None:
        self.__sheet_data_grouped = {}
        self.__sheet_lines = {}

