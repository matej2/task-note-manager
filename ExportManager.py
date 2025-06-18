import re
from collections import OrderedDict
from datetime import datetime, timedelta

from pyexcel_ods3 import save_data

from ConfigManager import ConfigManager
from DataManager import DataManager
from models.NoteEntry import NoteEntry


class ExportManager:

    def __init__(self, config_manager: ConfigManager, data_manager: DataManager) -> None:
        self.config_manager = config_manager
        self.data_manager = data_manager
        self._sheet_data = {}

    def add_sheet_row(self, data: list[list[str]], tab: str) -> None:
        self._sheet_data.update({tab: data})

    def save_as_ordered_dict(self) -> None:
        input_data = OrderedDict()
        input_data.update(self._sheet_data)
        save_data("task_notes.ods", input_data)

    def export_data(self) -> None:
        note_list = self.data_manager.read_data_from_file()
        sheet_content = [["Date", "Things done", "To be done", "Problems"]]

        for note in note_list.notes:
            new_line = [note.date, note.done, note.in_progress, note.problems]
            sheet_content.append(new_line)

        self.add_sheet_row(sheet_content, "Default")
        self.export_task_names()


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

    def export_task_names(self) -> None:
        note = self.data_manager.get_data_for_current_day()

        result = ExportManager.get_task_list(note.done)
        result.extend(ExportManager.get_task_list(note.in_progress))
        result.extend(ExportManager.get_task_list(note.problems))
        self.add_sheet_row([result], "Tasks")
        self.save_as_ordered_dict()

    def get_data_for_date(self, date: datetime.date) -> list[NoteEntry] | list[None]:
        result = []
        note_list = self.data_manager.read_data_from_file()
        if note_list is not None:
            for note in note_list.notes:
                if note.date == date:
                    result.append(note)
        return result