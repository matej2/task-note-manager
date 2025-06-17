import re

from models.NoteEntry import NoteEntry


class TaskManager:
    def __init__(self):
        pass

    @staticmethod
    def get_task_list(note: str) -> list[str]:
        result = re.findall(r"^\s*([^:]*):|;\s*([^:]*):", note)
        formatted_result = []

        for r in result:
            if r[0] != "":
                formatted_result.append(r[0])

            else:
                formatted_result.append(r[1])

        return formatted_result

    @staticmethod
    def get_task_names(note: NoteEntry) -> list[str]:
        result = TaskManager.get_task_list(note.things_done)
        result.extend(TaskManager.get_task_list(note.to_be_done))
        result.extend(TaskManager.get_task_list(note.problems))
        return result
