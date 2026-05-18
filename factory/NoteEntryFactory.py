import datetime

from ConfigManager import ConfigManager
from models.LocalizedDate import LocalizedDate
from models.NoteEntry import NoteEntry


class NoteEntryFactory:
    def __init__(self, config: ConfigManager):
        self.config = config

    def create_note(self, done: str, in_progress: str, problems: str):
        current_date = LocalizedDate(self.config.date_format)
        return NoteEntry(str(current_date), done, in_progress, problems)
