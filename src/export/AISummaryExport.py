from export.IOdsTabExport import IOdsTabExport
from export.OdsTabExportBase import OdsTabExportBase
from manager.AISummaryManager import AISummaryManager
from manager.ConfigManager import ConfigManager
from manager.DataManager import DataManager
from models.AISummaryResponse import AISummaryResponse
from models.NoteList import NoteList


class AISummaryExport(IOdsTabExport):
    def __init__(self, export_context: OdsTabExportBase, config_manager: ConfigManager, data_manager: DataManager, ai_summary_manager: AISummaryManager):
        self.export_context = export_context
        self.config_manager = config_manager
        self.data_manager = data_manager
        self.ai_summary_manager = ai_summary_manager

    def get_header(self, *args):
        return [
            self.config_manager.TASK_DATA_TASK_NAMES.get("identifier"),
            self.config_manager.EXPORT_TH_AI_SUMMARY
        ]

    def run_export(self, current_data: NoteList):
        #json_response = self.ai_summary_manager.generate(current_data)
        json_response = """[
            {
                "task_name": "Task16",
                "task_description": "Inventory sync development began with performance tuning, followed by backend integration and UI wiring. A memory leak under load was identified and addressed during this process."
            },
            {
                "task_name": "Task17",
                "task_description": "Mobile layout fixes initiated with a skeleton implementation, proceeded with polishing error messages, and culminated in preparing the feature for release."
            },
            {
                "task_name": "Task18",
                "task_description": "The notification center project commenced with drafting the design and progressed to writing the migration script."
            },
            {
                "task_name": "Taks1",
                "task_description": "Testing activities were initiated to validate ongoing development."
            },
            {
                "task_name": "Task2",
                "task_description": "Testing and troubleshooting efforts were performed for the login update, which encountered specific issues during implementation."
            },
            {
                "task_name": "Task3",
                "task_description": "Problems regarding session management were identified and tracked."
            },
            {
                "task_name": "Task55",
                "task_description": "The project initialization task was successfully completed."
            },
            {
                "task_name": "",
                "task_description": "General maintenance, administrative tasks, and troubleshooting activities were conducted, including monitoring dashboard tweaks, fixing flaky tests, interviewing a candidate, managing IDE license renewals, addressing noisy overnight alerts, and recording general progress notes."
            }
        ]"""
        ai_summary_response = AISummaryResponse.model_validate_json(json_response)
        lines: list[list[str]] = [self.get_header()]

        for task_name, task_description in ai_summary_response.root:
            lines.append([task_name[1], task_description[1]])

        self.export_context.save_lines(
            self.config_manager.EXPORT_TH_AI_SUMMARY,
            lines
        )
