import re
from typing import Any

from src.manager.ConfigManager import ConfigManager
from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList
from src.models.Task import Task


class TaskManager:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager

    def get_tasks_from_note_list(self, note_list: NoteList) -> list[Task]:
        result: list[Task] = list()
        for n in note_list.notes:
            result = [*result, *self.get_tasks_from_note_entry(n)]
        return result

    def get_tasks_from_note_entry(self, note_entry: NoteEntry) -> list[Task]:
        result = self.get_tasks_from_field("done", note_entry)
        result.extend(self.get_tasks_from_field("in_progress", note_entry))
        result.extend(self.get_tasks_from_field("problems", note_entry))

        return result

    def get_tasks_from_field(self, field: str, note_entry: NoteEntry) -> list[Task]:
        result = re.findall(self.config_manager.TASK_NAME_REGEX, str(getattr(note_entry, field)))

        mapped_tasks = []
        for r in result:
            if r[0] != "" or r[1] != "":
                mapped_tasks.append(Task(r[0], r[1]))
        return mapped_tasks


