from models.NoteEntry import NoteEntry


class NoteList:
    def __init__(self, notes: list[NoteEntry] = None):
        if notes is None:
            notes = []
        self.notes = notes

    def __str__(self):
        output = "\n\n"
        for note in self.notes:
            output += f'Date: {note.date.strftime("%d %b, %Y")}\nThings done: {note.things_done}\nTo be done: {note.to_be_done}\nProblems: {note.problems}\n\n'
        return output
