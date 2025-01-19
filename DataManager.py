import datetime
import tkinter
import yaml
from FileManager import FileManager
from StringUtils import StringUtils
from models.NoteEntry import NoteEntry, note_entry_representer
from models.NoteList import NoteList
from utils.YamlUtils import YamlUtils


class DataManager:

    def __init__(self, things_done: tkinter.Entry, things_in_progress: tkinter.Entry, problems: tkinter.Entry, status: tkinter.Label) -> None:
        self.things_done = things_done
        self.things_in_progress = things_in_progress
        self.problems = problems
        self.status = status

        self.file_manager = FileManager()
        yaml.add_representer(NoteEntry, note_entry_representer)

    def get_status(self):
        with self.file_manager.get_read_instance() as file:
            data = yaml.load(file, Loader=YamlUtils.get_loader())
            status = StringUtils.format_status(data)
        return status

    def write_status(self, event=None):
        status_data = self.get_status()
        self.status.config(text=status_data)

    def get_value(self, event=None):
        done = self.things_done.get()
        to_be_done = self.things_in_progress.get()
        problems = self.problems.get()

        self.add_entry(done, to_be_done, problems, datetime.datetime.now())

        self.get_status()
        self.write_status(event)

    def add_entry(self, changes: str, to_be_done: str, problems: str, date: datetime.datetime):
        with self.file_manager.get_write_instance() as file:
            file_line = yaml.dump(NoteEntry(date, changes, to_be_done, problems))
            file.write(f"{file_line}\n")
            file.close()
