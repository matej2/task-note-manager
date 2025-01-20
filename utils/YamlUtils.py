import yaml

from models import NoteList
from models.NoteEntry import NoteEntry


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
        #loader.add_constructor("!", YamlUtils.note_entry_constructor)
        loader.add_constructor("!", YamlUtils.note_entry_list_constructor)
        return loader

    @staticmethod
    def note_entry_representer(dumper, data: NoteList):
        return dumper.represent_dict(
            {
                'date': data.date,
                'things_done': data.things_done,
                'to_be_done': data.to_be_done,
                'problems': data.problems
            }
        )

    @staticmethod
    def note_list_representer(dumper, data: NoteList): return dumper.represent_mapping(u'tag:yaml.org,2002:map', data.__dict__)

    @staticmethod
    def note_entry_representer(dumper, data: NoteEntry): return dumper.represent_mapping(u'tag:yaml.org,2002:map',
                                                                                         data.__dict__)

