from functools import reduce

from src.models.NoteEntry import NoteEntry

class NoteList:
    def __init__(self, notes: list[NoteEntry]):
        if notes is None:
            notes = []
        self.notes = notes

    def __str__(self):
        return reduce(lambda sum, curr: str(sum) + "\n---\n\n" + str(curr), self.notes)
