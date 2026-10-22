from customtkinter import CTkTextbox as Text, CTkLabel as Label
from unittest.mock import MagicMock


class TKinterTestUtils:
    @staticmethod
    def create_text_element_mock() -> Text:
        text_element_mock = Text()
        text_element_mock.get = MagicMock(return_value="Text element mock")
        return text_element_mock
    @staticmethod
    def create_label_element_mock():
        text_element_mock = Label()
        text_element_mock.get = MagicMock(return_value="Text element mock")
        return text_element_mock