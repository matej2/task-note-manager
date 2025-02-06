import datetime
import tkinter
import typing

import yaml
from DataManagerBase import DataManagerBase

from FileManager import FileManager
from StringUtils import StringUtils
from models.NoteEntry import NoteEntry
from models.NoteList import NoteList
from utils.YamlUtils import YamlUtils


class DataManager(DataManagerBase):

    def __init__(self, things_done: tkinter.Text, things_in_progress: tkinter.Text, problems: tkinter.Text, status: tkinter.Label, file_manager: FileManager) -> None:
        super().__init__(file_manager)
        self.things_done = things_done
        self.things_in_progress = things_in_progress
        self.problems = problems
        self.status = status

        yaml.add_representer(NoteList, YamlUtils.note_list_representer)
        yaml.add_representer(NoteEntry, YamlUtils.note_entry_representer)

    def get_today_data(self) -> list[NoteEntry] | list[None]:
        result = []
        note_list = self.read_data()
        if note_list is not None:
            for note in note_list.notes:
                if note.date == datetime.date.today().strftime("%d.%m.%Y"):
                    result.append(note)
        return result

    def write_value(self) -> None:
        existing_data = self.read_data()
        if existing_data is None:
            existing_data = NoteList()

        done = self.things_done.get("1.0", "end-1c")
        to_be_done = self.things_in_progress.get("1.0", "end-1c")
        problems = self.problems.get("1.0", "end-1c")

        current_date = datetime.date.today().strftime("%d.%m.%Y")

        new_note = NoteEntry(current_date, done, to_be_done, problems)
        existing_data.notes.append(new_note)

        self.write_data(existing_data)

