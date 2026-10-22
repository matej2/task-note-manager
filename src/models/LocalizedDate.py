from datetime import datetime


class LocalizedDate:
    def __init__(self,  locale: str, input_date: datetime = datetime.now()):
        self.__locale = locale
        self.date_instance = datetime(
            input_date.year,
            input_date.month,
            input_date.day
        )

    def __str__(self):
        return self.date_instance.strftime(self.__locale)