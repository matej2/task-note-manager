from models.NoteEntry import NoteEntry


class NoteListOrdered:
    def __init__(self, tasks_done: list[NoteEntry], tasks_in_progress: list[NoteEntry], problems: list[NoteEntry]):
        self.tasks_done = tasks_done
        self.tasks_in_progress = tasks_in_progress
        self.problems = problems
