import unittest
from unittest.mock import patch, MagicMock, Mock, mock_open

from DataManagerBase import DataManagerBase
from models.NoteEntry import NoteEntry
from models.NoteList import NoteList


class TestDataManagerBase(unittest.TestCase):
    def setUp(self):
        mock_instance = MagicMock()
        self.data_manager_base = DataManagerBase(mock_instance)

    @patch('threading.Thread')
    def test_read_data_from_file_async(self, mock_thread):
        mock_instance = MagicMock()
        mock_thread.return_value = mock_instance

        self.data_manager_base.read_data_from_file_async(lambda x: x, {})

        mock_thread.assert_called_once()

        kwargs = mock_thread.call_args.kwargs
        self.assertIsNotNone(kwargs.get("target"))
        kwargs_for_callable = kwargs.get("kwargs")
        self.assertIsNotNone(kwargs_for_callable.get("read_instance"))
        self.assertIsNotNone(kwargs_for_callable.get("first_callback"))
        self.assertIsNotNone(kwargs_for_callable.get("args"))

        mock_instance.start.assert_called_once()

    @patch('threading.Thread')
    def test_write_data_from_file_async(self, mock_thread):
        mock_instance = MagicMock()
        mock_thread.return_value = mock_instance
        mock_callback = MagicMock()

        self.data_manager_base._write_data_to_file_async(NoteList(Mock()), mock_callback)

        mock_thread.assert_called_once()

        kwargs = mock_thread.call_args.kwargs
        self.assertIsNotNone(kwargs.get("target"))
        kwargs_for_callable = kwargs.get("kwargs")
        self.assertIsNotNone(kwargs_for_callable.get("write_instance"))
        self.assertIsNotNone(kwargs_for_callable.get("note_list"))
        self.assertIsNotNone(kwargs_for_callable.get("callback"))

        mock_instance.start.assert_called_once()

    def test_read_data_from_file_with_undefined_arguments(self):
        file_content = "key: value"
        m = mock_open(read_data=file_content)

        with patch("builtins.open", m):
            first_callback = Mock()
            args = {}

            read_instance = open("dummy")  # will use mocked open

            self.data_manager_base._read_data_from_file(
                read_instance,
                first_callback,
                args
            )

            first_callback.assert_called_once()
            args = first_callback.call_args.args
            self.assertEquals(args[0], {'key': 'value'})

    def test_read_data_from_file_with_defined_arguments(self):
        file_content = "key: value"
        m = mock_open(read_data=file_content)

        with patch("builtins.open", m):
            first_callback = Mock()
            input_args = {"test": "hello"}

            read_instance = open("dummy")  # will use mocked open

            self.data_manager_base._read_data_from_file(
                read_instance,
                first_callback,
                input_args
            )

            first_callback.assert_called_once()
            args = first_callback.call_args.args
            self.assertEquals(args[0], {'key': 'value'})
            self.assertEquals(args[1], {'test': 'hello'})


    def test_write_data_to_file_with_undefined_arguments(self):
        m = mock_open()
        note_list = NoteList(notes=[NoteEntry()])

        with patch("builtins.open", m):
            first_callback = Mock()

            write_instance = open("dummy")  # will use mocked open

            self.data_manager_base._write_data_to_file(
                write_instance,
                note_list,
                first_callback
            )

            first_callback.assert_called_once()
            args = first_callback.call_args.args
            self.assertEquals(args[0], note_list)

if __name__ == '__main__':
    unittest.main()