import tkinter
from tkinter import Text
from unittest.mock import MagicMock


class TKinterTestUtils:
    @staticmethod
    def create_text_element_mock() -> Text:
        text_element_mock = tkinter.Text()
        text_element_mock.get = MagicMock(return_value="Text element mock")
        return text_element_mock
    @staticmethod
    def create_label_element_mock():
        text_element_mock = tkinter.Label()
        text_element_mock.get = MagicMock(return_value="Text element mock")
        return text_element_mock