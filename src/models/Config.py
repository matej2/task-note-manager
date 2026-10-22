import os

from utils.FileUtils import FileUtils


class Config:
    def __init__(self, save_directory: str | None = None):
        if save_directory is None:
            self.save_directory = os.path.join(FileUtils.get_working_dir(), "task_notes.yaml")
