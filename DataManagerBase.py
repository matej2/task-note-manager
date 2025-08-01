import threading

import yaml
from FileManager import FileManager
from models.NoteList import NoteList
from utils.YamlUtils import YamlUtils


class DataManagerBase:

    def __init__(self, file_manager: FileManager) -> None:
        self.file_manager = file_manager

    def read_data_from_file_async(self, first_callback: callable, args: dict = None):
        thread = threading.Thread(
            target=self._read_data_from_file,
            kwargs={
                "read_instance": self.file_manager.get_read_instance(),
                "first_callback":first_callback,
                "args": args
            })
        thread.start()

    def _read_data_from_file(self, read_instance, first_callback, args) -> None:
        with read_instance as file:
            data = yaml.load(file, Loader=YamlUtils.get_loader())
        if args is not None:
            first_callback(data, args)
        else:
            first_callback(data)

    def get_data_from_file(self) -> NoteList:
        with self.file_manager.get_read_instance() as file:
            data = yaml.load(file, Loader=YamlUtils.get_loader())
        return data

    def _write_data_to_file_async(self, note_list: NoteList, callback: callable):
        thread = threading.Thread(
            target=self.__write_data_to_file,
            kwargs={
                "write_instance": self.file_manager.get_write_instance(),
                "note_list": note_list,
                "callback":callback
            })
        thread.start()

    @staticmethod
    def __write_data_to_file(write_instance, note_list: NoteList, callback):
        with (write_instance as file):
            yaml.dump(note_list, file)
        callback(note_list)
