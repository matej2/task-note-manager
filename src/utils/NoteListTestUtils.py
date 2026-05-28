from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList


class NoteListTestUtils:
    @staticmethod
    def get_test_note_list():
        return NoteList(
            notes=[
                NoteEntry(
                    "12. Jan. 2024",
                    "Created draft")
            ]
        )