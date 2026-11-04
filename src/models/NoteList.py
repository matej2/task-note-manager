from src.models.NoteEntry import NoteEntry

class NoteList:
    notes: list[NoteEntry]

    def __init__(self, notes: list[NoteEntry] | None):
        if notes is None:
            notes = []
        self.notes = notes
