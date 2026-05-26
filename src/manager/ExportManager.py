from src.export.NoteByStatusByDate import ByStatusForDate
from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager


class ExportManager:

    def __init__(self, config_manager: ConfigManager, data_manager: DataManager):
        self.config_manager = config_manager
        self.data_manager = data_manager

        self.export_modes = [
            ByStatusForDate(config_manager, data_manager),
        ]

    async def export_data(self) -> None:
        for mode in self.export_modes:
            await mode.run_export()

