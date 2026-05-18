from typing import Generator

from models.NoteEntry import NoteEntry
from models.NoteList import NoteList


class NoteListHelper:
    @staticmethod
    def get_note_list_iter(note_list: NoteList) -> Generator[NoteEntry, None, None]:
        index = 0
        while index < len(note_list.notes):
            yield note_list.notes[index]
            index += 1