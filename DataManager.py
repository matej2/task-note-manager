import datetime
import tkinter

import yaml

from ConfigManager import ConfigManager
from DataManagerBase import DataManagerBase
from FileManager import FileManager
from factory.NotesFactory import NotesFactory
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

    def extract_todays_notes(self, note_list : NoteList) -> NoteEntry | None:
        result = None
        for note in note_list.notes:
            if note.date == datetime.date.today().strftime("%d. %b. %Y"):
                result = note
        return result

    def get_today_data(self) -> NoteEntry:
        result = NotesFactory.create_empty_note()
        note_list = self.read_data()

        if note_list is not None:
            result = self.extract_todays_notes(note_list)
        return result

    def get_data_for_date(self, date: datetime.date) -> list[NoteEntry] | list[None]:
        result = []
        note_list = self.read_data()
        if note_list is not None:
            for note in note_list.notes:
                if note.date == date:
                    result.append(note)
        return result

    def override_existing_data_with_new_note(self, list: NoteList, entry: NoteEntry) -> None:
        for i,e in enumerate(list.notes):
            if e.date == entry.date:
                list.notes[i] = entry
                return
        list.notes.append(entry)

    def write_value(self) -> None:
        existing_data = self.read_data()
        if existing_data is None:
            existing_data = NoteList()

        done = self.things_done.get("1.0", "end-1c")
        to_be_done = self.things_in_progress.get("1.0", "end-1c")
        problems = self.problems.get("1.0", "end-1c")

        new_note = NotesFactory.create_note(done, to_be_done, problems)

        self.override_existing_data_with_new_note(existing_data, new_note)
        self.write_data(existing_data)
