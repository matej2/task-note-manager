import datetime


class StringUtils:
    @staticmethod
    def format_date(input_date: datetime.datetime) -> str:
        return input_date.strftime("%B")
        pass

    @staticmethod
    def format_status(data: dict) -> str:
        output = ""
        for key, value in data.items():
            if value is not None:
                output += f"{key}: {value}\n"
        return output
