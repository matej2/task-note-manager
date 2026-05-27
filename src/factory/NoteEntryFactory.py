from src.manager.ConfigManager import ConfigManager
from src.models.LocalizedDate import LocalizedDate
from src.models.NoteEntry import NoteEntry


class NoteEntryFactory:
    def __init__(self, config: ConfigManager):
        self.config = config

    @staticmethod
    def create_empty_note() -> NoteEntry:
        return NoteEntry("", "", "")

    def create_note(self, done: str, in_progress: str, problems: str):
        current_date = LocalizedDate(self.config.DATE_FORMAT)
        return NoteEntry(str(current_date), done, in_progress, problems)
