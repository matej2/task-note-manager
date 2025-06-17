class NoteEntry:
    def __init__(self, date: str, done: str, in_progress: str, problems: str):
        self.date = date
        self.done = done
        self.in_progress = in_progress
        self.problems = problems

    def is_empty(self) -> bool:
        return self.done == "" and self.in_progress == "" and self.problems == ""

    def __str__(self):
        return f'\n\nDate: {self.date}\nThings done: {self.done}\nTo be done: {self.in_progress}\nProblems: {self.problems}\n\n'

