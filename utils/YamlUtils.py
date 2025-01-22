from typing import Type

import yaml
from yaml import SafeLoader

from models.NoteEntry import NoteEntry
from models.NoteList import NoteList


class YamlUtils:
    _allowed_nodes = [
        "date",
        "problems",
        "things_done",
        "to_be_done"
    ]

    @staticmethod
    def remove_unknown_keys(value: dict) -> dict:
        result = {}
        for key, value in value.items():
            if key in YamlUtils._allowed_nodes:
                result[key] = value
        return result

    @staticmethod
    def note_entry_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> NoteEntry:
        yaml_nodes = YamlUtils.remove_unknown_keys(loader.construct_mapping(node))

        return NoteEntry(**yaml_nodes)

    @staticmethod
    def note_entry_list_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> NoteList:
        return NoteList(**loader.construct_mapping(node))

    @staticmethod
    def get_loader() -> Type[SafeLoader]:
        loader = yaml.SafeLoader
        loader.add_constructor("!NoteList", YamlUtils.note_entry_list_constructor)
        loader.add_constructor("!NoteEntry", YamlUtils.note_entry_constructor)
        return loader

    @staticmethod
    def note_list_representer(dumper, data: NoteList): return dumper.represent_mapping("!NoteList", data.__dict__)

    @staticmethod
    def note_entry_representer(dumper, data: NoteEntry): return dumper.represent_mapping("!NoteEntry",
                                                                                         data.__dict__)

