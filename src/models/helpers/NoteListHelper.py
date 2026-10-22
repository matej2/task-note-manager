from typing import Generator

from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList


class NoteListHelper:
    @staticmethod
    def get_note_list_iter(note_list: NoteList) -> Generator[NoteEntry, None, None]:
        index = len(note_list.notes)-1
        while index >= 0:
            yield note_list.notes[index]
            index += 1