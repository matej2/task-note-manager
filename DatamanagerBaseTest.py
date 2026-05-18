import unittest
from unittest.mock import patch, MagicMock

from DataManagerBase import DataManagerBase


class DataManagerBaseTest(unittest.TestCase):
    def setUp(self):
        mock_instance = MagicMock()
        self.data_manager_base = DataManagerBase(mock_instance)

    @patch('threading.Thread')
    def test_read_data_from_file_async(self, mock_thread):
        mock_instance = MagicMock()
        mock_thread.return_value = mock_instance

        self.data_manager_base.read_data_from_file_async(lambda x: x, {})

        # 1. Assert a Thread object was initialized
        mock_thread.assert_called_once()

        # 2. Check the arguments used to create the thread
        kwargs = mock_thread.call_args.kwargs
        #self.assertEqual(kwargs.get('name'), "WorkerThread")

        # 3. Assert that .start() was called on that thread instance
        mock_instance.start.assert_called_once()