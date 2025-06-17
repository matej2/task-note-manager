import datetime

from models.NoteEntry import NoteEntry

class NoteList:
    def __init__(self, notes: list[NoteEntry] = None):
        if notes is None:
            notes = []
        self.notes = notes