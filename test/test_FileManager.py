import unittest
from unittest.mock import Mock, patch, mock_open

from src.manager.FileManager import FileManager


class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.config = Mock()
        self.config.FULL_PATH = "foo"

        self.file_manager = FileManager(self.config)

    def test_init(self):
        m = mock_open()
        with patch("builtins.open", m):
            FileManager(self.config)

            m.assert_called_with("foo", "a")
            handle = m()
            handle.write.assert_called_once_with("")

    def test_get_read_wrapper(self):
        m = mock_open()
        with patch("builtins.open", m):
            self.file_manager.get_read_wrapper()

            m.assert_called_with("foo", "r")

    def test_get_write_wrapper(self):
        m = mock_open()
        with patch("builtins.open", m):
            self.file_manager.get_write_wrapper()

            m.assert_called_with("foo", "w")

    def test_open_file_in_ext_app(self):
        with patch("webbrowser.open") as mock:
            self.file_manager.open_file_in_ext_app()

            assert mock.called


