from typing import Self


class NoteEntry:
    def __init__(self, date: str, done: str, in_progress: str, problems: str):
        self.date = date
        self.done = done

    def is_empty(self) -> bool:
        return self.done == ""

    def __str__(self):
        return f'\n\nDate: {self.date}\nThings done: {self.done}\n\n'

    def __eq__(self, other: Self):
        return self.date == other.date and self.done == other.done

