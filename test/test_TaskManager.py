import unittest
from unittest.mock import Mock

from src.manager.TaskManager import TaskManager
from src.models.LocalizedDate import LocalizedDate
from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList
from src.models.Task import Task


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        config_manager_mock = Mock()
        config_manager_mock.TASK_NAME_REGEX = r"\s*([^:;]*)\s*:\s*([^:;]*)"
        self.task_manager = TaskManager(config_manager_mock)

        self.note_entry = NoteEntry(
            str(LocalizedDate("%d. %b. %Y")),
            "TASK1: Writing documentation; TASK2: Defining roadmap",
        )

        self.note_list = NoteList([self.note_entry,])

    def test_get_tasks_from_note_entry_with_defined_input(self):
        result = self.task_manager.get_tasks_from_note_entry(self.note_entry)
        
        assert len(result) == 2

        assert result[0].name == "TASK1"
        assert result[0].description == "Writing documentation"
        assert result[1].name == "TASK2"
        assert result[1].description == "Defining roadmap"

    def test_get_tasks_from_note_list(self):
        get_tasks_from_note_entry_mock = Mock()
        get_tasks_from_note_entry_mock.return_value = [Task("TASK1", "Started with project")]

        self.task_manager.get_tasks_from_note_entry = get_tasks_from_note_entry_mock

        result = self.task_manager.get_tasks_from_note_list(self.note_list)

        assert len(result) == 1
        assert result[0].name == "TASK1"
        assert result[0].description == "Started with project"
