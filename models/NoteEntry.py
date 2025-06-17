class NoteEntry:
    def __init__(self, date: str, things_done: str, to_be_done: str, problems: str):
        self.date = date
        self.done = things_done
        self.in_progress = to_be_done
        self.problems = problems

    def is_empty(self) -> bool:
        return self.done == "" and self.in_progress == "" and self.problems == ""

    def __str__(self):
        return f'\n\nDate: {self.date}\nThings done: {self.done}\nTo be done: {self.in_progress}\nProblems: {self.problems}\n\n'

