import yaml
from FileManager import FileManager
from models.NoteList import NoteList
from utils.YamlUtils import YamlUtils


class DataManagerBase:

    def __init__(self, file_manager: FileManager) -> None:
        self.file_manager = file_manager

    def check_datatype(self, value: object, class_name: type):
        if not isinstance(value, class_name):
            raise RuntimeError(f'Wrong datatype, expected {type}')

    def read_data(self) -> NoteList:
        with self.file_manager.get_read_instance() as file:
            data = yaml.load(file, Loader=YamlUtils.get_loader())
        #self.check_datatype(data, NoteList)
        return data

    def write_data(self, note_list: NoteList):
        with (self.file_manager.get_write_instance() as file):
            yaml.dump(note_list, file)
