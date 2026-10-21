import yaml

from src.manager.FileManager import FileManager
from src.models.NoteList import NoteList
from src.utils.YamlUtils import YamlUtils


class DataManagerBase:

    def __init__(self, file_manager: FileManager) -> None:
        self.file_manager = file_manager

    async def read_data_from_file_async_direct(self) -> NoteList:
        with self.file_manager.get_read_wrapper() as file:
            data = yaml.load(file, Loader=YamlUtils.get_loader())
        if data is not None and len(data.notes) != 0:
            return data
        else:
            return NoteList()

    async def _write_data_to_file_direct(self, note_list: NoteList):
        with self.file_manager.get_write_wrapper() as file:
            yaml.dump(note_list, file, allow_unicode=True)
