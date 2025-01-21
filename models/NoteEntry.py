import datetime


class NoteEntry:
    def __init__(self, date: datetime.datetime, things_done: str, to_be_done: str, problems: str):
        self.date = date
        self.things_done = things_done
        self.to_be_done = to_be_done
        self.problems = problems

    def __str__(self):
        return f'Date: {self.date.strftime("%d %b, %Y")}\nThings done: {self.things_done}\nTo be done: {self.to_be_done}\nProblems: {self.problems}\n\n'

