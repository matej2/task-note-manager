import datetime


class NoteEntry:
    def __init__(self, date: datetime.datetime, things_done: str, to_be_done: str, problems: str):
        self.date = date
        self.things_done = things_done
        self.to_be_done = to_be_done
        self.problems = problems


def note_entry_representer(dumper, data: NoteEntry):
    return dumper.represent_dict(
        {
            'date': data.date,
            'things_done': data.things_done,
            'to_be_done': data.to_be_done,
            'problems': data.problems
        }
    )
