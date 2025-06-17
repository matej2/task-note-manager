import re
from datetime import datetime

from models.NoteList import NoteList


class TaskManager:
    def __init__(self):
        pass
    @staticmethod
    def list_to_string(result: list[str]) -> str:
        if result[0] != "":
            return result[0]
        else:
            return result[1]
    @staticmethod
    def get_task_list(note: str) -> list[str]:
        result = re.findall(r"^([^:]*):|;([^:]*):", note)
        formatted_result = []

        for r in result:
            formatted_result.append(TaskManager.list_to_string(r))

        return formatted_result

    @staticmethod
    def get_task_names(note_list: NoteList) -> list[str]:
        note = note_list.get_todays_note()
        result = TaskManager.get_task_list(note.things_done)
        result.extend(TaskManager.get_task_list(note.to_be_done))
        result.extend(TaskManager.get_task_list(note.problems))
        return result
