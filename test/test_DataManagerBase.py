from typing import Any
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, mock_open, patch, MagicMock, ANY

from src.manager.DataManagerBase import DataManagerBase
from test.util.TestUtils import get_note_list


class TestDataManagerBase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:

        file_manager_mock = Mock()
        file_manager_mock.get_read_wrapper = mock_open(read_data="foo")
        file_manager_mock.get_write_wrapper = mock_open()

        self.data_manager_base = DataManagerBase(file_manager_mock)

    async def test_read_data_from_file_async_direct(self):
        # Empty file
        with patch("yaml.load") as mock_empty:
            mock_empty.read.return_value = None

            result = await self.data_manager_base.read_data_from_file_async_direct()

            assert result is not None
            assert len(result.notes) == 1

        # Non-empty file
        with patch("yaml.load") as mock_non_empty:
            mock_non_empty.return_value = get_note_list() #Should return an NoteList, but the test gets MagicMock

            result = await self.data_manager_base.read_data_from_file_async_direct()

            assert result is not None
            assert len(result.notes) == 2 # This is empty

    async def test_write_data_to_file_direct(self):
        note_list = get_note_list()
        with patch("yaml.dump") as dump_mock:
            await self.data_manager_base._write_data_to_file_direct(note_list)
            dump_mock.assert_called_once()
            dump_mock.assert_called_with(note_list, ANY, allow_unicode=True)