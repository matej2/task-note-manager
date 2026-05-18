from abc import ABC, abstractmethod
from datetime import date


class IOdsTabExport(ABC):
    @abstractmethod
    def add_content_row(self, row: list[str]) -> float:
        pass

    @abstractmethod
    def write_content(self) -> str:
        pass

    @abstractmethod
    def process_data_for_date(self, for_date: date) -> None:
        pass