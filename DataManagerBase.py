import threading
from typing import Callable

import yaml
from FileManager import FileManager
from models.NoteList import NoteList
from utils.YamlUtils import YamlUtils


class DataManagerBase:

    def __init__(self, file_manager: FileManager) -> None:
        self.file_manager = file_manager

    def read_data_from_file_async(self, first_callback: Callable, args: dict = {}):
        thread = threading.Thread(
            target=DataManagerBase._read_data_from_file,
            kwargs={
                "read_instance": self.file_manager.get_read_wrapper(),
                "first_callback":first_callback,
                "args": args
            })
        thread.start()
        return thread

    @staticmethod
    def _read_data_from_file(read_instance, first_callback, args) -> None:
        with read_instance as file:
            data = yaml.load(file, Loader=YamlUtils.get_loader())
        if args != {}:
            first_callback(data, args)
        else:
            first_callback(data)

    def _write_data_to_file_async(self, note_list: NoteList, callback: Callable):
        thread = threading.Thread(
            target=self._write_data_to_file,
            kwargs={
                "write_instance": self.file_manager.get_write_wrapper(),
                "note_list": note_list,
                "callback":callback
            })
        thread.start()

    @staticmethod
    def _write_data_to_file(write_instance, note_list: NoteList, callback):
        with (write_instance as file):
            yaml.dump(note_list, file)
        callback(note_list)
