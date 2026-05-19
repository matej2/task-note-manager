import logging
import tkinter
from typing import Callable

import yaml

from ConfigManager import ConfigManager
from DataManagerBase import DataManagerBase
from FileManager import FileManager
from factory.NoteEntryFactory import NoteEntryFactory
from models.LocalizedDate import LocalizedDate
from models.NoteEntry import NoteEntry
from models.NoteList import NoteList
from models.helpers.NoteListHelper import NoteListHelper
from utils.YamlUtils import YamlUtils


class DataManager(DataManagerBase):

    def __init__(self,
                 things_done: tkinter.Text,
                 status: tkinter.Label,
                 file_manager: FileManager,
                 config_manager: ConfigManager,
                 note_factory: NoteEntryFactory
                 ) -> None:
        super().__init__(file_manager)
        self.done = things_done
        self.status = status
        self.logger = logging.getLogger(__name__)

        self.config_manager = config_manager
        self.note_factory = note_factory

        yaml.add_representer(NoteList, YamlUtils.note_list_representer)
        yaml.add_representer(NoteEntry, YamlUtils.note_entry_representer)

    def __extract_todays_notes(self, note_list : NoteList) -> NoteEntry | None:
        result = NoteEntry()
        if note_list is None:
            return result

        note_list_iter = NoteListHelper.get_note_list_iter(note_list)
        for note in note_list_iter:
            if note.date == str(LocalizedDate(self.config_manager.date_format)):
                result = note
        return result

    def get_data_for_current_day(self, callback: Callable) -> None: # pragma: no cover
        self.read_data_from_file_async(
            lambda note_list: callback(
                self.__extract_todays_notes(
                    note_list
                )
            )
        )

    @staticmethod
    def __override_existing_data_with_new_note(note_list: NoteList, entry: NoteEntry) -> None:
        for i,e in enumerate(note_list.notes):
            if e.date == entry.date:
                note_list.notes[i] = entry
                return
        note_list.notes.append(entry)

    @staticmethod
    def __get_text_from_input(input_text: tkinter.Text):
        return input_text.get("1.0", "end-1c")

    def __process_save_input(self, existing_data: NoteList, callback: Callable) -> None:
        if existing_data is None:
            existing_data = NoteList(list())

        done = DataManager.__get_text_from_input(self.done)

        new_note = self.note_factory.create_note(done)

        DataManager.__override_existing_data_with_new_note(existing_data, new_note)
        self._write_data_to_file_async(existing_data, callback)
        self.logger.debug(f"Wrote data to file, input: {done}")


    def save_input_data(self, callback: Callable) -> None:
        self.read_data_from_file_async(lambda note_entry: self.__process_save_input(note_entry, callback))
