import logging
from abc import ABC, abstractmethod
from datetime import date


class IOdsTabExport(ABC):
    logger = logging.getLogger(__name__)

    @abstractmethod
    def add_header(self):
        pass

    @abstractmethod
    async def run_export(self, for_date: date) -> None:
        pass