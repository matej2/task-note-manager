from models.NoteEntry import NoteEntry


class NoteList:
    def __init__(self, notes: list[NoteEntry] = None):
        if notes is None:
            notes = []
        self.notes = notes

    def __str__(self):
        output = ""
        for note in self.notes:
            output += f'Date: {note.date}\nThings done: {note.things_done}\nTo be done: {note.to_be_done}\nProblems: {note.problems}'
        return output