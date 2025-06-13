import datetime
import tkinter

import yaml
from ConfigManager import ConfigManager
from DataManagerBase import DataManagerBase
from FileManager import FileManager
from models.NoteEntry import NoteEntry
from models.NoteList import NoteList
from utils.YamlUtils import YamlUtils


class DataManager(DataManagerBase):

    def __init__(self, things_done: tkinter.Text, things_in_progress: tkinter.Text, problems: tkinter.Text, status: tkinter.Label, file_manager: FileManager, config_manager: ConfigManager) -> None:
        super().__init__(file_manager)
        self.things_done = things_done
        self.things_in_progress = things_in_progress
        self.problems = problems
        self.status = status

        self.config_manager = config_manager

        yaml.add_representer(NoteList, YamlUtils.note_list_representer)
        yaml.add_representer(NoteEntry, YamlUtils.note_entry_representer)

    def get_today_data(self) -> list[NoteEntry] | list[None]:
        result = []
        note_list = self.read_data()
        if note_list is not None:
            for note in note_list.notes:
                if note.date == datetime.date.today().strftime(self.config_manager.date_format):
                    result.append(note)
        return result

    def get_today_data_single(self) -> NoteEntry | None:
        if len(self.get_today_data()) == 0:
            return NoteEntry("", "", "", "")
        else:
            return self.get_today_data()[0]

    def find_and_replace_data(self, list: NoteList, entry: NoteEntry) -> None:
        for i,e in enumerate(list.notes):
            if e.date == entry.date:
                list.notes[i] = entry
                break

    def split_string_to_tasks(self, string: str) -> list[str]:
        return string.split(";")

    def write_value(self) -> None:
        existing_data = self.read_data()
        if existing_data is None:
            existing_data = NoteList()

        done = self.things_done.get("1.0", "end-1c")
        to_be_done = self.things_in_progress.get("1.0", "end-1c")
        problems = self.problems.get("1.0", "end-1c")

        current_date = datetime.date.today().strftime(self.config_manager.date_format)

        new_note = NoteEntry(current_date, done, to_be_done, problems)

        self.find_and_replace_data(existing_data, new_note)

        self.write_data(existing_data)
    def export_data(self) -> None:
        pass
