from typing import Self


class NoteEntry:
    def __init__(self, date: str = "", done: str = "", in_progress: str = "", problems: str = ""):
        self.date = date
        self.done = done or ""
        self.in_progress = in_progress or ""
        self.problems = problems or ""

    def is_empty(self) -> bool:
        return self.done == "" and self.in_progress == "" and self.problems == ""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NoteEntry):
            return NotImplemented
        return self.date == other.date and self.done == other.done and self.in_progress == other.in_progress and self.problems == other.problems

