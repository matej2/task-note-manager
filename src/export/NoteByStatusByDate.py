from src.export.IOdsTabExport import IOdsTabExport
from src.export.OdsTabExportBase import OdsTabExportBase
from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager
from src.models.NoteList import NoteList


class NoteByStatusByDate(IOdsTabExport):
    def __init__(self, config_manager: ConfigManager, data_manager: DataManager):
        self.config_manager = config_manager
        self.data_manager = data_manager

        self.done_label = self.config_manager.TASK_DATA_DONE.get("identifier")
        self.in_progress_label = self.config_manager.TASK_DATA_IN_PROGRESS.get("identifier")
        self.problems_label = self.config_manager.TASK_DATA_PROBLEMS.get("identifier")

    def get_header(self):
        return [
            self.config_manager.TASK_DATA_DATE.get("identifier"),
            self.config_manager.TASK_DATA_DONE.get("identifier"),
            self.config_manager.TASK_DATA_IN_PROGRESS.get("identifier"),
            self.config_manager.TASK_DATA_PROBLEMS.get("identifier"),
        ]

    # TODO: Change  to set
    @staticmethod
    def format_task(task: dict) -> str:
        result = ""
        if len(task.keys()) == 0:
            return result

        for name, desc in task.items():
            if result != "":
                result += ";\n"
            if name == "":
                result += f"{desc}"
            else:
                result += f"{name}: {desc}"

        return result

    def save_as_table_status_by_date(self) -> None:
        """
            self.config_manager.EXPORT_TH_DATE,
            self.config_manager.EXPORT_TH_DONE,
            self.config_manager.EXPORT_TH_IN_PROGRESS,
            self.config_manager.EXPORT_TH_PROBLEMS
        :return:
        """
        lines = list()
        lines.append(self.get_header())

        for date, task_type in OdsTabExportBase.get_sheet_data_grouped().items():
            lines.append([
                date,
                self.format_task(task_type.get(self.done_label)),
                self.format_task(task_type.get(self.in_progress_label)),
                self.format_task(task_type.get(self.problems_label)),
            ])

        OdsTabExportBase.save_lines(self.config_manager.EXPORT_TAB_NAME_DEFAULT, lines)

    def run_export(self, current_data: NoteList):
        self.get_header()
        # Do this just once
        for note in current_data.notes:
            OdsTabExportBase.add_task_data(note)

        self.save_as_table_status_by_date()
