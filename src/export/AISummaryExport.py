from export.IOdsTabExport import IOdsTabExport
from export.OdsTabExportBase import OdsTabExportBase
from manager.AISummaryManager import AISummaryManager
from manager.ConfigManager import ConfigManager
from manager.DataManager import DataManager
from models.AISummaryResponse import AISummaryResponse
from models.NoteList import NoteList


class AISummaryExport(IOdsTabExport):
    def __init__(self, config_manager: ConfigManager, data_manager: DataManager, ai_summary_manager: AISummaryManager):
        self.config_manager = config_manager
        self.data_manager = data_manager
        self.ai_summary_manager = ai_summary_manager

    def get_header(self, *args):
        return [
            self.config_manager.TASK_DATA_TASK_NAMES.get("identifier"),
            self.config_manager.EXPORT_TH_AI_SUMMARY
        ]


    def run_export(self, current_data: NoteList):
        json_response = self.ai_summary_manager.generate(current_data)
        ai_summary_response = AISummaryResponse.model_validate_json(json_response)
        lines: list[list[str]] = [self.get_header()]

        for task_name, task_description in ai_summary_response.root:
            lines.append([task_name[1], task_description[1]])

        OdsTabExportBase.save_lines(
            self.config_manager.EXPORT_TH_AI_SUMMARY,
            lines
        )
