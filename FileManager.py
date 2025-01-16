import datetime
import os
import typing


class FileManager:

    def __init__(self) -> None:
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.full_path = os.path.join(self.current_dir, "demofile2.txt")
        pass

    def add_entry(self, changes: str, date: datetime.datetime):
        f = open(self.full_path, "a")
        f.write(f"{date} {changes}\n")
        f.close()
