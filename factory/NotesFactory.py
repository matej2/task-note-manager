import datetime

from models.NoteEntry import NoteEntry


class NotesFactory:
    @staticmethod
    def create_empty_note() -> NoteEntry:
        return NoteEntry("", "", "", "")

    @staticmethod
    def create_note(done: str, to_do: str, problems: str):
        current_date = datetime.date.today().strftime("%d. %b. %Y")
        return NoteEntry(current_date, done, to_do, problems)
