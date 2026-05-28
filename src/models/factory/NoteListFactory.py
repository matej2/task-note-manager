from src.models.LocalizedDate import LocalizedDate
from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList


class NoteListFactory:
    @staticmethod
    def get_empty_note_list():
        return NoteList([NoteEntry(
            date=str(LocalizedDate("%d. %b. %Y"))
        ),])