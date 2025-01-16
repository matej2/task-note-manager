import datetime
import tkinter

from FileManager import FileManager


class DataManager:

    def __init__(self, things_done: tkinter.Entry) -> None:
        self.things_done = things_done
        self.file_manager = FileManager()

    def get_value(self):
        e_text = self.things_done.get()
        self.file_manager.add_entry(e_text, datetime.datetime.now())
