import os
import platform


class FileUtils:
    @staticmethod
    def get_working_dir():
        if platform.system() == "Windows":
            os.makedirs(os.path.join(os.environ["APPDATA"], "TaskNoteManager"), exist_ok=True)
            return os.path.join(os.environ["APPDATA"], "TaskNoteManager")
        else:
            os.makedirs(os.path.join(os.path.expanduser("~"), ".TaskNoteManager"), exist_ok=True)
            return os.path.join(os.path.expanduser("~"), ".TaskNoteManager")