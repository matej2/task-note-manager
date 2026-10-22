from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, patch, MagicMock, AsyncMock

from src.manager.ExportManager import ExportManager
from test.util.TestUtils import get_note_list


class TestExportManager(IsolatedAsyncioTestCase):
    @patch("src.manager.ExportManager.NoteByTaskNameByDate")
    @patch("src.manager.ExportManager.NoteByStatusByDate")
    @patch("src.manager.ExportManager.OdsTabExportBase")
    async def test_export_data(self, export_base_mock, by_status_mock, by_task_mock):
        export_base_mock.set_dependencies.return_value = None
        export_base_mock.delete_data.return_value = None

        status_instance = MagicMock()
        status_instance.run_export = AsyncMock()

        task_instance = MagicMock()
        task_instance.run_export = AsyncMock()

        by_status_mock.return_value = status_instance
        by_task_mock.return_value = task_instance

        export_manager = ExportManager(
            config_manager=MagicMock(),
            data_manager=MagicMock(),
            task_manager=MagicMock(),
        )

        input_note_list = get_note_list()

        await export_manager.export_data(input_note_list)

        by_status_mock.assert_called_once()
        by_task_mock.assert_called_once()

        export_base_mock.set_dependencies.assert_called_once()
        export_base_mock.delete_data.assert_called_once()

        status_instance.run_export.assert_called_once_with(input_note_list)
        task_instance.run_export.assert_called_once_with(input_note_list)
