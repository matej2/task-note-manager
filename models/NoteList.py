import datetime

from models.NoteEntry import NoteEntry

class NoteList:
    def __init__(self, notes: list[NoteEntry] = None):
        if notes is None:
            notes = []
        self.notes = notes

    def get_note_by_date(self, date: str) -> NoteEntry | None:
        for note in self.notes:
            if note.date == date:
                return note
        return None

    def get_todays_note(self) -> NoteEntry | None:
        result = None
        for note in self.notes:
            if note.date == datetime.date.today().strftime("%d. %b. %Y"):
                result = note
        return result