import yaml

from models.NoteEntry import NoteEntry


class YamlUtils:
    @staticmethod
    def note_list_entry_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> NoteEntry:
        return NoteEntry(**loader.construct_mapping(node))
    @staticmethod
    def get_loader() -> yaml.loader.SafeLoader:
        loader = yaml.SafeLoader
        loader.add_constructor("!", YamlUtils.note_list_entry_constructor)
        return loader

