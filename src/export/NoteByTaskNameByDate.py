from src.export.IOdsTabExport import IOdsTabExport
from src.export.OdsTabExportBase import OdsTabExportBase
from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager
from src.manager.TaskManager import TaskManager
from src.models.NoteList import NoteList


class NoteByTaskNameByDate(IOdsTabExport):
    def __init__(self, config_manager: ConfigManager, data_manager: DataManager, task_manager: TaskManager) -> None:
        self.config_manager = config_manager
        self.data_manager = data_manager
        self.task_manager = task_manager


    @staticmethod
    def process_task_types(task_type_name: str, task_name: str, task_date: str, task_description: str,  task_name_to_date: dict[str,dict[str,str]]):
        if task_name not in task_name_to_date.keys():
            task_name_to_date[task_name] = dict()

        if task_date not in task_name_to_date[task_name]:
            task_name_to_date[task_name][task_date] = f"{task_type_name}: {''.join(task_description)}"
        else:
            task_name_to_date[task_name][task_date] += f";\n{task_type_name}: {''.join(task_description)}"

    @staticmethod
    def get_data_mapped_by_name_and_date() -> dict[str,dict[str,str]]:
        task_name_to_date: dict[str,dict[str,str]] = dict()

        for task_date, task_types in OdsTabExportBase.get_sheet_data_grouped().items():

            for task_type_name, task_type in task_types.items():
                for task_name, task_description in task_type.items():
                    NoteByTaskNameByDate.process_task_types(task_name, task_name, task_date, task_description, task_name_to_date)

        return task_name_to_date

    def get_header(self) -> list[str]:
        all_dates = [
            x for x in OdsTabExportBase.get_sheet_data_grouped().keys()]
        all_dates.insert(0, '')
        return all_dates

    def run_export(self, current_data: NoteList):
        task_name_to_date = self.get_data_mapped_by_name_and_date()

        lines = list(list())
        all_date_values = self.get_header()
        lines.append(all_date_values)

        for task_name, task_dates in task_name_to_date.items():
            line = ['' for _ in all_date_values]
            line[0] = task_name

            for task_date, description in task_dates.items():
                date_index = all_date_values.index(task_date)
                line[date_index] = description
            lines.append(line)

        OdsTabExportBase.save_lines(self.config_manager.EXPORT_TAB_NAME_TASK_NAMES, lines)
