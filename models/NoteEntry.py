from typing import Self


class NoteEntry:
    def __init__(self, date: str = "", done: str = "", in_progress: str = "", problems: str = ""):
        self.date = date
        self.done = done
        self.in_progress = in_progress
        self.problems = problems

    def is_empty(self) -> bool:
        return self.done == "" and self.in_progress == "" and self.problems == ""

    def __str__(self):
        return f'Date: {self.date}\nThings done: {self.done}\nIn progress: {self.in_progress}\nProblems: {self.problems}'

    def __eq__(self, other: Self):
        return self.date == other.date and self.done == other.done and self.in_progress == other.in_progress and self.problems == other.problems

