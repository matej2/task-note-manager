import os

from utils.FileUtils import FileUtils


class Config:
    def __init__(
            self,
            save_directory: str | None = None,
            export_file_path: str | None = None,
            gemini_api_key: str | None = None,
    ):
        if save_directory is None:
            self.save_directory = os.path.join(FileUtils.get_working_dir(), "task_notes.yaml")
        else:
            self.save_directory = save_directory

        if export_file_path is None:
            self.export_file_path = os.path.join(FileUtils.get_working_dir(), "task_notes.ods")
        else:
            self.export_file_path = export_file_path

        if gemini_api_key is None:
            self.gemini_api_key = ""
        else:
            self.gemini_api_key = gemini_api_key
