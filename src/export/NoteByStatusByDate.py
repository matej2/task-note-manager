from src.export.IOdsTabExport import IOdsTabExport
from src.export.OdsTabExportBase import OdsTabExportBase
from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager


class ByStatusForDate(IOdsTabExport):
    def __init__(self, config_manager: ConfigManager, data_manager: DataManager):
        self.config_manager = config_manager
        self.data_manager = data_manager
        OdsTabExportBase.init(self.config_manager, self.data_manager)

    def add_header(self):
        OdsTabExportBase.add_sheet_row( [
            self.config_manager.export_th_date,
            self.config_manager.export_th_done,
            self.config_manager.export_th_in_progress,
            self.config_manager.export_th_problems
        ], self.config_manager.export_file_tab_name_default)

    async def run_export(self) -> None:
        note_list = await self.data_manager.read_data_from_file_async_direct()

        self.add_header()
        for note in iter(note_list.notes):
            OdsTabExportBase.add_sheet_row(
                [note.date, note.done, note.in_progress, note.problems],
                self.config_manager.export_file_tab_name_default)

        OdsTabExportBase.save_as_ordered_dict()
        self.logger.debug(f"Exported saved content to {self.config_manager.export_file_name}")