import logging
import tkinter

import yaml

from src.manager.ConfigManager import ConfigManager
from src.manager.DataManagerBase import DataManagerBase
from src.manager.FileManager import FileManager
from src.factory.NoteEntryFactory import NoteEntryFactory
from src.models.LocalizedDate import LocalizedDate
from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList
from src.models.helpers.NoteListHelper import NoteListHelper
from utils.YamlUtils import YamlUtils


class DataManager(DataManagerBase):

    def __init__(self,
                 things_done: tkinter.Text,
                 things_in_progress: tkinter.Text,
                 problems: tkinter.Text,
                 status: tkinter.Label,
                 file_manager: FileManager,
                 config_manager: ConfigManager,
                 note_factory: NoteEntryFactory
                 ) -> None:
        super().__init__(file_manager)
        self.done = things_done
        self.in_progress = things_in_progress
        self.problems = problems
        self.status = status
        self.logger = logging.getLogger(__name__)

        self.config_manager = config_manager
        self.note_factory = note_factory

        yaml.add_representer(NoteList, YamlUtils.note_list_representer)
        yaml.add_representer(NoteEntry, YamlUtils.note_entry_representer)

    def extract_today_notes(self, note_list : NoteList) -> NoteEntry:
        result = NoteEntry()
        if note_list is None:
            return result

        note_list_iter = NoteListHelper.get_note_list_iter(note_list)
        for note in note_list_iter:
            if note.date == str(LocalizedDate(self.config_manager.DATE_FORMAT)):
                result = note
            break
        return result

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

    async def __process_save_input(self, existing_data: NoteList) -> None:
        if existing_data is None:
            existing_data = NoteList(list())

        done = DataManager.__get_text_from_input(self.done)
        to_be_done = DataManager.__get_text_from_input(self.in_progress)
        problems = DataManager.__get_text_from_input(self.problems)

        new_note = self.note_factory.create_note(done, to_be_done, problems)

        DataManager.__override_existing_data_with_new_note(existing_data, new_note)
        await self._write_data_to_file_direct(existing_data)
        self.logger.debug(f"Wrote data to file, input: {done} {to_be_done} {problems}")


    async def save_input_data(self) -> NoteList:
        note_list = await self.read_data_from_file_async_direct()
        await self.__process_save_input(note_list)
        return note_list
