import logging
from abc import ABC, abstractmethod

from src.models.NoteList import NoteList


class IOdsTabExport(ABC):
    logger = logging.getLogger(__name__)

    @abstractmethod
    def add_header(self, *args):
        pass

    @abstractmethod
    async def run_export(self, current_data: NoteList) -> None:
        pass