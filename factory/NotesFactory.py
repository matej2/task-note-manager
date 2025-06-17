import datetime

from ConfigManager import ConfigManager
from models.NoteEntry import NoteEntry


class NotesFactory:
    def __init__(self, config: ConfigManager):
        self.config = config

    @staticmethod
    def create_empty_note() -> NoteEntry:
        return NoteEntry("", "", "", "")

    def create_note(self, done: str, in_progress: str, problems: str):
        current_date = datetime.date.today().strftime(self.config.date_format)
        return NoteEntry(current_date, done, in_progress, problems)
