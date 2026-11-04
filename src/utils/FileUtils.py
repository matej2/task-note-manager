import os
import platform


class FileUtils:
    @staticmethod
    def get_working_dir():
        save_directory = os.path.join(os.path.expanduser("~"), "TaskNoteManager")
        os.makedirs(save_directory, exist_ok=True)

        return save_directory