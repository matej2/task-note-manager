import unittest
from unittest.mock import patch, Mock, MagicMock

from yaml import SafeLoader

from src.utils.YamlUtils import YamlUtils
from test.util.TestUtils import get_note_list


class TestYamlUtils(unittest.TestCase):
    def setUp(self):
        self.yaml_utils = YamlUtils()

    @patch("src.utils.YamlUtils")
    def test_remove_unknown_keys(self, yaml_utils_mock):
        yaml_utils = YamlUtils()

        result = yaml_utils.remove_unknown_keys({"done": "test", "notes": "test"})


        assert len(result.keys()) == 1

    @patch("src.utils.YamlUtils.YamlUtils.remove_unknown_keys")
    def test_note_entry_constructor(self, remove_keys_mock):
        loader_mock = Mock()
        node_mock = Mock()
        remove_keys_mock.return_value = {"done": "implementation", "in_progress": "test"}

        note_entry = self.yaml_utils.note_entry_constructor(loader_mock, node_mock)

        assert note_entry.done == "implementation"
        assert note_entry.in_progress == "test"

    def test_note_entry_list_constructor(self):
        loader_mock = Mock()
        note_entry = get_note_list().notes[0]
        loader_mock.construct_mapping.return_value = {"notes": [note_entry]}

        note_list = self.yaml_utils.note_entry_list_constructor(loader_mock, Mock())

        assert note_list.notes[0].done == "Lored ipsum"
        assert note_list.notes[0].in_progress == "Something"
        assert note_list.notes[0].problems == "None"

    @patch("src.utils.YamlUtils.YamlUtils.note_entry_constructor")
    @patch("src.utils.YamlUtils.YamlUtils.note_entry_list_constructor")
    @patch("yaml.SafeLoader", autospec=True)
    def test_get_loader(self, safe_loader_mock, list_constructor_mock, entry_constructor_mock):
        loader_mock = MagicMock()
        loader_mock.add_constructor.return_value = None

        self.yaml_utils.get_loader()

        safe_loader_mock.add_constructor.assert_any_call("!NoteList", list_constructor_mock)
        safe_loader_mock.add_constructor.assert_any_call("!NoteEntry", entry_constructor_mock)


