import datetime


class NoteEntry:
    def __init__(self, date: datetime.datetime, things_done: str):
        self.date = date
        self.things_done = things_done


def note_entry_representer(dumper, data: NoteEntry):
    return dumper.represent_dict({'date': data.date, 'things_done': data.things_done})
