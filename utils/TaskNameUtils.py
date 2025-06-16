import re


class TaskNameUtils:
    @staticmethod
    def list_to_string(result: list[str]) -> str:
        if result[0] is not "":
            return result[0]
        else:
            return result[1]
    @staticmethod
    def get_task_list(note: str) -> list[str]:
        result = re.findall(r"^([^:]*):|;([^:]*):", note)
        formatted_result = []

        for r in result:
            formatted_result.append(TaskNameUtils.list_to_string(r))

        return formatted_result