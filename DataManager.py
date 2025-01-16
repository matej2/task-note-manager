import datetime
import tkinter
import yaml
from FileManager import FileManager
from models.NoteEntry import NoteEntry, note_entry_representer


class DataManager:

    def __init__(self, things_done: tkinter.Entry) -> None:
        self.things_done = things_done
        self.file_manager = FileManager()
        yaml.add_representer(NoteEntry, note_entry_representer)

    def get_value(self, event=None):
        e_text = self.things_done.get()
        self.file_manager.add_entry(e_text, datetime.datetime.now())
