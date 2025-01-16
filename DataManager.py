import datetime
import tkinter
import yaml
from FileManager import FileManager
from models.NoteEntry import NoteEntry, note_entry_representer


class DataManager:

    def __init__(self, things_done: tkinter.Entry, things_in_progress: tkinter.Entry, problems: tkinter.Entry) -> None:
        self.things_done = things_done
        self.things_in_progress = things_in_progress
        self.problems = problems

        self.file_manager = FileManager()
        yaml.add_representer(NoteEntry, note_entry_representer)

    def get_value(self, event=None):
        e_text = self.things_done.get()
        to_be_done = self.things_in_progress.get()
        problems = self.problems.get()

        self.file_manager.add_entry(e_text, to_be_done, problems, datetime.datetime.now())
