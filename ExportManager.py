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

    def save_as_ordered_dict(self, data: list[list[str]]) -> None:
        input_data = OrderedDict()
        input_data.update({"Notes": data})
        save_data("task_notes.ods", input_data)

    def export_data(self) -> None:
        note_list = self.data_manager.read_data_from_file()
        all_notes = [["Date", "Things done", "To be done", "Problems"]]

        for note in note_list.notes:
            new_line = [note.date, note.done, note.in_progress, note.problems]
            all_notes.append(new_line)

        self.save_as_ordered_dict(all_notes)

    def export_tasks_by_date(self) -> None:
        curr_date = datetime.date.today().strftime(self.config_manager.date_format)
        previous_dates = []
        previous_tasks = []

        for n in range(7):
            previous_dates.append((curr_date - timedelta(days=n)).strftime(self.config_manager.date_format))

        for d in previous_dates:
            note = self.get_data_for_date(d)
            if note is not None:
                previous_tasks.append(note)

        previous_dates.insert(0, "Task name")

        self.save_as_ordered_dict(previous_tasks)

    def get_data_for_date(self, date: datetime.date) -> list[NoteEntry] | list[None]:
        result = []
        note_list = self.data_manager.read_data_from_file()
        if note_list is not None:
            for note in note_list.notes:
                if note.date == date:
                    result.append(note)
        return result