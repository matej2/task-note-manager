import unittest
from tkinter.font import Font
from unittest.mock import Mock, patch, MagicMock

from src.manager.UILayoutHelper import UILayoutHelper


class TestUILayoutHelper(unittest.TestCase):
    def setUp(self):
        config_manager = Mock()
        config_manager.get_regular_font.return_value = Mock()
        config_manager.NEW_NOTE_INPUT_PADY = 30
        config_manager.NEW_NOTE_INPUT_PADX = 30

        self.layout_helper = UILayoutHelper(config_manager)

    def test_display_new_note_input(self):
        parent = MagicMock()

        result = self.layout_helper.display_new_note_input(parent, 0, 0)

        assert result is not None

