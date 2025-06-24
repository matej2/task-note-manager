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
        self.done = things_done
        self.in_progress = things_in_progress
        self.problems = problems
        self.status = status

        self.config_manager = config_manager
        self.note_factory = NotesFactory(self.config_manager)

        yaml.add_representer(NoteList, YamlUtils.note_list_representer)
        yaml.add_representer(NoteEntry, YamlUtils.note_entry_representer)

    def __extract_todays_notes(self, note_list : NoteList) -> NoteEntry | None:
        result = self.note_factory.create_empty_note()
        for note in note_list.notes:
            if note.date == datetime.date.today().strftime(self.config_manager.date_format):
                result = note
        return result

    def get_data_for_current_day(self) -> NoteEntry:
        result = NotesFactory.create_empty_note()
        note_list = self._read_data_from_file()

        if note_list is not None:
            result = self.__extract_todays_notes(note_list)
        return result

    @staticmethod
    def __override_existing_data_with_new_note(list: NoteList, entry: NoteEntry) -> None:
        for i,e in enumerate(list.notes):
            if e.date == entry.date:
                list.notes[i] = entry
                return
        list.notes.append(entry)

    @staticmethod
    def __get_text_from_input(input: tkinter.Text):
        return input.get("1.0", "end-1c")

    def save_input_data(self) -> None:
        existing_data = self._read_data_from_file()
        if existing_data is None:
            existing_data = NoteList()

        done = DataManager.__get_text_from_input(self.done)
        to_be_done = DataManager.__get_text_from_input(self.in_progress)
        problems = DataManager.__get_text_from_input(self.problems)

        new_note = self.note_factory.create_note(done, to_be_done, problems)

        DataManager.__override_existing_data_with_new_note(existing_data, new_note)
        self._write_data_to_file(existing_data)
