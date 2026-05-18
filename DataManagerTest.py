import unittest
from unittest.mock import Mock, patch

from ConfigManager import ConfigManager
from DataManager import DataManager
from utils.NoteListTestUtils import NoteListTestUtils


class DataManagerTest(unittest.TestCase):
    def setup(self):
        config_manager_mock = ConfigManager()
        config_manager_mock.date_format = "%d. %b. %Y"

        self.data_manager = DataManager(
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            Mock(),
            config_manager_mock,
            Mock()
        )

    @patch("models.helpers.NoteListHelper")
    def test_extract_todays_notes_for_correct_input(self, note_list_iter):
        note_list = NoteListTestUtils.get_test_note_list()
        note_list_iter.return_value = note_list

        note_entry = self.data_manager.get_data_for_current_day(lambda x: x)

        assert note_entry is not None

