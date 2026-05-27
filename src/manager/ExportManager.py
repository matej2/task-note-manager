from src.export.NoteByStatusByDate import NoteByStatusByDate
from src.export.NoteByTaskNameByDate import NoteByTaskNameByDate
from src.export.OdsTabExportBase import OdsTabExportBase
from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager


class ExportManager:

    def __init__(self, config_manager: ConfigManager, data_manager: DataManager):
        self.config_manager = config_manager
        self.data_manager = data_manager

        OdsTabExportBase.init(config_manager, data_manager)

        self.registered_export_types = [
            NoteByStatusByDate(config_manager, data_manager),
            NoteByTaskNameByDate(config_manager, data_manager),
        ]

    async def export_data(self) -> None:
        OdsTabExportBase.delete_data()

        for registered_type in self.registered_export_types:
            await registered_type.run_export()

