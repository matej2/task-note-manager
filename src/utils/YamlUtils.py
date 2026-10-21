from typing import Type, cast

import yaml
from yaml import SafeLoader

from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList


class YamlUtils:
    __allowed_nodes_note_entry = {
        "date",
        "problems",
        "done",
        "in_progress"
    }

    __allowed_nodes_note_list = {
        "notes"
    }

    @staticmethod
    def remove_unknown_note_entry_keys(data: dict) -> dict:
        return {
            key: val
            for key, val in data.items()
            if key in YamlUtils.__allowed_nodes_note_entry
        }

    @staticmethod
    def remove_unknown_note_list_keys(data: dict) -> dict:
        return {
            key: val
            for key, val in data.items()
            if key in YamlUtils.__allowed_nodes_note_list
        }

    @staticmethod
    def note_entry_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> NoteEntry:
        yaml_nodes = YamlUtils.remove_unknown_note_entry_keys(loader.construct_mapping(node))

        date = yaml_nodes.get("date", None)
        done = yaml_nodes.get("done", None)
        in_progress = yaml_nodes.get("in_progress", None)
        problem = yaml_nodes.get("problems", None)

        return NoteEntry(**yaml_nodes)

    @staticmethod
    def note_entry_list_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> NoteList:
        yaml_nodes = YamlUtils.remove_unknown_note_list_keys(loader.construct_mapping(node))
        return NoteList(**yaml_nodes)

    @staticmethod
    def get_loader() -> Type[SafeLoader]:
        loader = yaml.SafeLoader
        loader.add_constructor("!NoteList", YamlUtils.note_entry_list_constructor)
        loader.add_constructor("!NoteEntry", YamlUtils.note_entry_constructor)
        return loader

    @staticmethod
    def note_list_representer(dumper, data: NoteList):
        return dumper.represent_mapping("!NoteList", data.__dict__)

    @staticmethod
    def note_entry_representer(dumper, data: NoteEntry):
        return dumper.represent_mapping("!NoteEntry",
                                        {k: (None if v == '' else v) for k, v in data.__dict__.items()})

    @staticmethod
    def string_representer(dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

    @staticmethod
    def none_representer(dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', '', style='"')