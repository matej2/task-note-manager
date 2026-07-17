from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList


class NoteListFactory:
    @staticmethod
    def get_empty_note_list():
        return NoteList([NoteEntry("", "", ""),])