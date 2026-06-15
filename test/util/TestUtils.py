from datetime import datetime, timedelta

from src.models.LocalizedDate import LocalizedDate
from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList


def get_empty_note_list():
    yesterday = datetime.now() - timedelta(days=1)

    return NoteList([NoteEntry(
        date=str(LocalizedDate("%d. %b. %Y", yesterday))
    ), ])

def get_note_list():
    yesterday = datetime.now() - timedelta(days=1)
    return NoteList([
        NoteEntry(
            date=str(LocalizedDate("%d. %b. %Y", yesterday)),
            done="Lored ipsum",
            in_progress="Something",
            problems="None"),
        NoteEntry(
            date=str(LocalizedDate("%d. %b. %Y")),
            done="Finished with tests",
            in_progress="Refactoring",
            problems="Need to prepare docs"
    ) ])

def get_current_date():
    return datetime(
        datetime.now().year,
        datetime.now().month,
        datetime.now().day
    )