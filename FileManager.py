import datetime
import os
import typing

import yaml

from models.NoteEntry import NoteEntry


class FileManager:

    def __init__(self) -> None:
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.full_path = os.path.join(self.current_dir, "demofile2.txt")
        pass

    def add_entry(self, changes: str, to_be_done: str, problems: str, date: datetime.datetime):
        f = open(self.full_path, "a")
        file_line = yaml.dump(NoteEntry(date, changes, to_be_done, problems))
        f.write(f"{file_line}\n")
        f.close()
