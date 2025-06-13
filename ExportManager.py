from collections import OrderedDict

from pyexcel_ods3 import save_data

from ConfigManager import ConfigManager
from DataManager import DataManager


class ExportManager:

    def __init__(self, confix_manager: ConfigManager, data_manager: DataManager) -> None:
        self.config_manager = confix_manager
        self.data_manager = data_manager

    def export_data(self):
        note_list = self.data_manager.read_data()
        all_notes = [["Date", "Things done", "To be done", "Problems"]]

        for note in note_list.notes:
            new_line = [note.date, note.things_done, note.to_be_done, note.problems]
            all_notes.append(new_line)

        data = OrderedDict()
        data.update({"Notes": all_notes})
        save_data("task_notes.ods", data)