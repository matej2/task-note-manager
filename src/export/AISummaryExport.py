from export.IOdsTabExport import IOdsTabExport
from export.OdsTabExportBase import OdsTabExportBase
from manager.AISummaryManager import AISummaryManager
from manager.ConfigManager import ConfigManager
from manager.DataManager import DataManager
from models.NoteList import NoteList


class AISummaryExport(IOdsTabExport):
    def __init__(self, config_manager: ConfigManager, data_manager: DataManager, ai_summary_manager: AISummaryManager):
        self.config_manager = config_manager
        self.data_manager = data_manager
        self.ai_summary_manager = ai_summary_manager

    def get_header(self, *args):
        OdsTabExportBase.add_sheet_row( [
            self.config_manager.TASK_DATA_TASK_NAMES.get("identifier"),
            self.config_manager.EXPORT_TH_AI_SUMMARY
        ], self.config_manager.EXPORT_TAB_NAME_AI_SUMMARY)


    def run_export(self, current_data: NoteList) -> None:
        summary_by_tasks = self.ai_summary_manager.generate(current_data)
        self.get_header()
        for task_name, task_description in summary_by_tasks:
            OdsTabExportBase.add_sheet_row(
                [task_name, task_description],
                self.config_manager.EXPORT_TH_AI_SUMMARY)

        OdsTabExportBase.save_as_ordered_dict()