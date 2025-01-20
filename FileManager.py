import os
import typing


class FileManager:

    def __init__(self) -> None:
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.full_path = os.path.join(self.current_dir, "demofile2.txt")

        # Creates a file if it does not exist
        with open(self.full_path, "a") as f:
            f.write("")

    def get_read_instance(self) -> typing.TextIO:
        return open(self.full_path, "r")

    def get_write_instance(self) -> typing.TextIO:
        return open(self.full_path, "w")

