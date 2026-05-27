import re

from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager
from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList
from src.models.Task import Task


class TaskManager:
    def __init__(self, config_manager: ConfigManager, data_manager: DataManager):
        self.config_manager = config_manager
        self.data_manager = data_manager

    def get_tasks_from_note_list(self, note_list: NoteList) -> list[Task]:
        result = list()
        for n in note_list.notes:
            result = [*result, *self.get_tasks_from_note_entry(n)]
        return result

    def get_tasks_from_note_entry(self, note_entry: NoteEntry) -> list[Task]:
        result = re.findall(self.config_manager.TASK_NAME_REGEX, note_entry.done)
        result.extend(re.findall(self.config_manager.TASK_NAME_REGEX, note_entry.in_progress))
        result.extend(re.findall(self.config_manager.TASK_NAME_REGEX, note_entry.problems))

        return [Task(r[0], r[1]) for r in result]
