class NoteEntry:
    def __init__(self, date: str, things_done: str, to_be_done: str, problems: str):
        self.date = date
        self.things_done = things_done
        self.to_be_done = to_be_done
        self.problems = problems

    def __str__(self):
        txt = "Date:".rjust(15) + self.date + '\n'
        txt += "Things done:".rjust(15) + self.things_done + '\n'
        txt += "To be done:".rjust(15) + self.to_be_done + '\n'
        txt += "Problems:".rjust(15) + self.problems + '\n'
        return txt

