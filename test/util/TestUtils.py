from datetime import datetime

from src.models.LocalizedDate import LocalizedDate
from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList


def get_empty_note_list():
    return NoteList([NoteEntry(
        date=str(LocalizedDate("%d. %b. %Y"))
    ), ])

def get_note_list():
    return NoteList([
        NoteEntry(
            date=str(LocalizedDate("%d. %b. %Y")),
            done="Lored ipsum",
            in_progress="Something",
            problems="None"),
        NoteEntry(
            date=str(LocalizedDate("%d. %b. %Y")),
            done="Lored ipsum",
            in_progress="Something",
            problems="None"
    ) ])

def get_current_date():
    return datetime(
        datetime.now().year,
        datetime.now().month,
        datetime.now().day
    )