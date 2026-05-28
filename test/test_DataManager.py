import unittest
from unittest.mock import patch, Mock, mock_open

from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager
from src.manager.FileManager import FileManager
from src.utils.NoteListTestUtils import NoteListTestUtils


class DataManagerTest(unittest.TestCase):
    def setUp(self):
        config_manager_mock = ConfigManager()
        config_manager_mock.DATE_FORMAT = "%d. %b. %Y"

        file_manager_mock = FileManager(config_manager_mock)
        file_content = "key: value"
        m = mock_open(read_data=file_content)
        self.patch_open = patch("builtins.open", m)
        self.patch_open.__enter__()

        file_manager_mock.get_read_wrapper = open("dummy")

        self.data_manager = DataManager(
            Mock(),
            Mock(),
            file_manager_mock,
            config_manager_mock,
            Mock()
        )

    @unittest.skip("reason for skipping")
    @patch("models.helpers.NoteListHelper")
    def test_extract_todays_notes_for_correct_input(self, note_list_iter):
        note_list = NoteListTestUtils.get_test_note_list()
        note_list_iter.return_value = note_list

        note_entry = self.data_manager.get_data_for_current_day(lambda x: x)

        assert note_entry is None

    def test_get_data_for_current_day(self):
        callable_mock = Mock()

        self.data_manager.get_data_for_current_day(callable_mock)

    def tearDown(self):
        self.patch_open.__exit__()

