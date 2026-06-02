import unittest
from unittest.mock import Mock, patch

from customtkinter import CTkFrame, CTk, CTkFont, CTkBaseClass, CTkLabel

from src.manager.UILayoutHelper import UILayoutHelper


class TestUILayoutHelper(unittest.TestCase):
    def setUp(self):
        self.root = CTk()

        config_manager = Mock()
        config_manager.get_regular_font.return_value = CTkFont(
            family="Arial",
            size=4
        )
        config_manager.NEW_NOTE_INPUT_PADY = 30
        config_manager.NEW_NOTE_INPUT_PADX = 30

        self.parent = CTkFrame(master=None)

        self.layout_helper = UILayoutHelper(config_manager)

    @staticmethod
    def __check_position(result: CTkBaseClass):
        info = result.grid_info()
        assert info["row"] == 0
        assert info["column"] == 0

    def test_display_new_note_input(self):

        result = self.layout_helper.display_new_note_input(self.parent, 0, 0)

        assert result is not None
        assert result.master is not None
        self.__check_position(result)


    def test_display_ftodays_notes_label(self):
        with patch.object(UILayoutHelper, "display_new_note_label") as new_note_mock:
            new_note_mock.return_value = CTkLabel(self.parent)

            result = self.layout_helper.display_todays_notes_label("Todays notes", self.parent, 0, 0)

            assert result.master is not None
            self.__check_position(result)

