import tkinter

from DataManager import DataManager


class Application(tkinter.Frame):
    def __init__(self):
        self.root = tkinter.Tk()
        tkinter.Frame.__init__(self, self.root)

        self.note_list_output = []

        self.create_input_widgets()
        self.create_status_widgets()

        # Data manager needs to be initialized after input widgets are created
        self.data_manager = DataManager(self.things_done, self.things_in_progress, self.problems, self.task_list)

        self.create_key_shortcuts()
        self.create_action_widgets()

        self.initialize()

    def initialize(self):
        self.list_data()

    def create_key_shortcuts(self):
        self.root.bind('<Return>', self.data_manager.add_value)

    def create_input_widgets(self):
        tkinter.Label(self.root, text="What was done: ").grid(row=0, column=0)
        self.things_done = tkinter.Entry(self.root)
        self.things_done.grid(row=0, column=1)
        self.things_done.focus_set()

        tkinter.Label(self.root, text="What needs to be done: ").grid(row=1, column=0)
        self.things_in_progress = tkinter.Entry(self.root)
        self.things_in_progress.grid(row=1, column=1)

        tkinter.Label(self.root, text="Any problems: ").grid(row=2, column=0)
        self.problems = tkinter.Entry(self.root)
        self.problems.grid(row=2, column=1)

    def create_status_widgets(self):
        self.task_status = tkinter.Label(self.root, text="Task status")
        self.task_status.grid(row=0, column=2)

        self.task_list = tkinter.Label(self.root, text="Task list")
        self.task_list.grid(row=1, column=2, rowspan=4)

    def create_action_widgets(self):
        self.submit_button = tkinter.Button(self.root, text="Enter", command=self.on_click_submit_button)
        self.submit_button.grid(row=3, column=0)

        self.list_button = tkinter.Button(self.root, text="List", command=self.list_data)
        self.list_button.grid(row=3, column=1)

        self.open_file = tkinter.Button(self.root, text="Open file", command=self.data_manager.file_manager.open_file)
        self.open_file.grid(row=4, column=0)

    def on_click_submit_button(self):
        self.data_manager.add_value()
        self.list_data()

        self.task_status.config(text="Task created")

    def list_data(self):
        note_list = self.data_manager.read_data()
        self.task_list.config(text=str(note_list))

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application().start()
