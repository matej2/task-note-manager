from collections import OrderedDict
from datetime import datetime, timedelta

from pyexcel_ods3 import save_data

from ConfigManager import ConfigManager
from DataManager import DataManager


class ExportManager:

    def __init__(self, confix_manager: ConfigManager, data_manager: DataManager) -> None:
        self.config_manager = confix_manager
        self.data_manager = data_manager

    def save_ordered_dict(self, data: list[list[str]]):
        input_data = OrderedDict()
        input_data.update({"Notes": data})
        save_data("task_notes.ods", input_data)

    def export_data(self):
        note_list = self.data_manager.read_data()
        all_notes = [["Date", "Things done", "To be done", "Problems"]]

        for note in note_list.notes:
            new_line = [note.date, note.things_done, note.to_be_done, note.problems]
            all_notes.append(new_line)

        data = OrderedDict()
        data.update({"Notes": all_notes})
        save_data("task_notes.ods", data)

    def export_tasks_by_date(self):
        """
        This will export tasks statuses. It will use task names as rows and dates as columns
        """
        curr_date = datetime.date.today().strftime(self.config_manager.date_format)
        previous_dates = []
        previous_tasks = []

        for n in range(7):
            previous_dates.append((curr_date - timedelta(days=n)).strftime(self.config_manager.date_format))

        for d in previous_dates:
            note = self.data_manager.get_data_for_date(d)
            if note is not None:
                previous_tasks.append(note)

        previous_dates.insert(0, "Task name")


        self.save_ordered_dict(previous_tasks)
