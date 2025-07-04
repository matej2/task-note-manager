from datetime import datetime


class LocalizedDate:
    def __init__(self,  locale: str, input_date: datetime = None):
        self.__locale = locale
        if input_date is None:
            current_time = datetime.now()
            self.date_instance = datetime(
                current_time.year,
                current_time.month,
                current_time.day
            )
        else:
            self.date_instance = datetime(
                input_date.year,
                input_date.month,
                input_date.day
            )

    def __str__(self):
        return self.date_instance.strftime(self.__locale)