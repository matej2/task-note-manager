from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, patch, AsyncMock

from src.manager.DataManager import DataManager
from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList
from test.util.TestUtils import get_note_list, get_empty_note_list


class TestDataManager(IsolatedAsyncioTestCase):
    def setUp(self):
        done = Mock()
        done.get.return_value = "Finished with tests UPDATED"

        in_progress = Mock()
        in_progress.get.return_value = "Refactoring UPDATED"

        problems = Mock()
        problems.get.return_value = "Need to prepare docs UPDATED"

        status = Mock()

        file_manager = Mock()

        config_manager = Mock()
        config_manager.DATE_FORMAT = "%d. %b. %Y"

        note_factory = Mock()
        note_factory.create_note.return_value = get_note_list().notes[1]

        current_data = get_note_list()

        self.data_manager = DataManager(
            done,
            in_progress,
            problems,
            status,
            file_manager,
            config_manager,
            note_factory,
            current_data
        )

    def test_extract_today_notes(self):
        # Input is None
        result = self.data_manager.extract_today_notes(None)
        assert result == NoteEntry()

        # Input is defined - todays note is included
        note_list = get_note_list()
        result = self.data_manager.extract_today_notes(note_list)
        assert result is not None
        assert result.done == "Finished with tests"
        assert result.in_progress == "Refactoring"
        assert result.problems == "Need to prepare docs"

        # Input is defined - todays note is not included
        note_list = get_empty_note_list()
        result = self.data_manager.extract_today_notes(note_list)
        assert result is not None
        assert result.done == ""
        assert result.in_progress == ""
        assert result.problems == ""

    async def test_process_save_input_with_defined_note_list(self):
        note_list = get_note_list()

        with patch.object(self.data_manager, "_write_data_to_file_direct", new_callable=AsyncMock) as write_data_mock:
            await self.data_manager.process_save_input(note_list)

            assert write_data_mock.called
            args, kwargs = write_data_mock.call_args
            result_note_list:NoteList = args[0]
            assert len(result_note_list.notes) == 2

    async def test_process_save_input_with_empty_note_list(self):
        with patch.object(self.data_manager, "_write_data_to_file_direct", new_callable=AsyncMock) as write_data_mock:
            await self.data_manager.process_save_input(NoteList(notes=list()))

            assert write_data_mock.called
            args, kwargs = write_data_mock.call_args
            result_note_list: NoteList = args[0]
            assert len(result_note_list.notes) == 1

