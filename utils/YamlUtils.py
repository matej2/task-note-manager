import yaml

from models.NoteEntry import NoteEntry
from models.NoteList import NoteList


class YamlUtils:
    @staticmethod
    def note_entry_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> NoteEntry:
        return NoteEntry(**loader.construct_mapping(node))

    @staticmethod
    def note_entry_list_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> NoteList:
        return NoteList(**loader.construct_mapping(node))

    @staticmethod
    def get_loaders() -> yaml.loader.SafeLoader:
        loader = yaml.SafeLoader
        loader.add_constructor("tag:yaml.org,2002:map", YamlUtils.note_entry_list_constructor)
        return loader

    @staticmethod
    def note_list_representer(dumper, data: NoteList): return dumper.represent_mapping(u'tag:yaml.org,2002:map', data.__dict__)

    @staticmethod
    def note_entry_representer(dumper, data: NoteEntry): return dumper.represent_mapping(u'tag:yaml.org,2002:map',
                                                                                         data.__dict__)

