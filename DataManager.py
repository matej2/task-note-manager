import datetime
import tkinter

import yaml

from FileManager import FileManager
from StringUtils import StringUtils
from models.NoteEntry import NoteEntry
from models.NoteList import NoteList
from utils.YamlUtils import YamlUtils


class DataManager:

    def __init__(self, things_done: tkinter.Text, things_in_progress: tkinter.Text, problems: tkinter.Text, status: tkinter.Label) -> None:
        self.things_done = things_done
        self.things_in_progress = things_in_progress
        self.problems = problems
        self.status = status

        self.file_manager = FileManager()

        yaml.add_representer(NoteList, YamlUtils.note_list_representer)
        yaml.add_representer(NoteEntry, YamlUtils.note_entry_representer)

    def read_data(self) -> NoteList:
        with self.file_manager.get_read_instance() as file:
            data = yaml.load(file, Loader=YamlUtils.get_loader())
        return data

    def add_value(self):
        existing_data = self.read_data()
        if existing_data is None:
            existing_data = NoteList()

        done = self.things_done.get("1.0", "end-1c")
        to_be_done = self.things_in_progress.get("1.0", "end-1c")
        problems = self.problems.get("1.0", "end-1c")

        new_note = NoteEntry(datetime.date.today(), done, to_be_done, problems)
        existing_data.notes.append(new_note)

        self.write_data(existing_data)

    def write_data(self, note_list: NoteList):
        with (self.file_manager.get_write_instance() as file):
            yaml.dump(note_list, file)
