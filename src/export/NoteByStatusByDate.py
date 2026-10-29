from src.export.IOdsTabExport import IOdsTabExport
from src.export.OdsTabExportBase import OdsTabExportBase
from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager
from src.models.NoteList import NoteList


class NoteByStatusByDate(IOdsTabExport):
    def __init__(self, config_manager: ConfigManager, data_manager: DataManager):
        self.config_manager = config_manager
        self.data_manager = data_manager

    def add_header(self):
        OdsTabExportBase.add_sheet_row( [
            self.config_manager.TASK_DATA_DATE.get("identifier"),
            self.config_manager.TASK_DATA_DONE.get("identifier"),
            self.config_manager.TASK_DATA_IN_PROGRESS.get("identifier"),
            self.config_manager.TASK_DATA_PROBLEMS.get("identifier"),
        ], self.config_manager.EXPORT_TAB_NAME_DEFAULT)

    def save_as_table_status_by_date(self) -> None:
        """
            self.config_manager.EXPORT_TH_DATE,
            self.config_manager.EXPORT_TH_DONE,
            self.config_manager.EXPORT_TH_IN_PROGRESS,
            self.config_manager.EXPORT_TH_PROBLEMS
        :return:
        """
        lines = list()
        for date, task_type in OdsTabExportBase.get_sheet_data_grouped().items():
            lines.append([
                date,
                str(task_type.get(self.config_manager.TASK_DATA_DONE.get("identifier"))),
                str(task_type.get(self.config_manager.TASK_DATA_IN_PROGRESS.get("identifier"))),
                str(task_type.get(self.config_manager.TASK_DATA_PROBLEMS.get("identifier")))
            ])

        OdsTabExportBase.save_lines(self.config_manager.EXPORT_TAB_NAME_DEFAULT, lines)

    def run_export(self, current_data: NoteList) -> None:
        self.add_header()
        for note in current_data.notes:
            OdsTabExportBase.add_task_data(note)

        self.save_as_table_status_by_date()
