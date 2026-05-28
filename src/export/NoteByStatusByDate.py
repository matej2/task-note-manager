from src.export.IOdsTabExport import IOdsTabExport
from src.export.OdsTabExportBase import OdsTabExportBase
from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager


class NoteByStatusByDate(IOdsTabExport):
    def __init__(self, config_manager: ConfigManager, data_manager: DataManager):
        self.config_manager = config_manager
        self.data_manager = data_manager

    def add_header(self):
        OdsTabExportBase.add_sheet_row( [
            self.config_manager.EXPORT_TH_DATE,
            self.config_manager.EXPORT_TH_DONE,
            self.config_manager.EXPORT_TH_IN_PROGRESS,
            self.config_manager.EXPORT_TH_PROBLEMS
        ], self.config_manager.EXPORT_TAB_NAME_DEFAULT)

    async def run_export(self) -> None:
        self.add_header()
        for note in OdsTabExportBase.current_data.notes:
            OdsTabExportBase.add_sheet_row(
                [note.date, note.done, note.in_progress, note.problems],
                self.config_manager.EXPORT_TAB_NAME_DEFAULT)

        OdsTabExportBase.save_as_ordered_dict()
        self.logger.debug(f"Exported saved content to {self.config_manager.EXPORT_FILE_NAME}")