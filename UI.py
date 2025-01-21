import tkinter

from ConfigManager import ConfigManager


class UI(tkinter.Frame):

    def __init__(self, config: ConfigManager):
        self.root = tkinter.Tk()
        tkinter.Frame.__init__(self, self.root)
        self.config_manager = config

        self.submit_button = tkinter.Button(self.root)
        self.open_file = tkinter.Button(self.root)
        self.list_button = tkinter.Button(self.root)

        self.task_status = tkinter.Label(self.root)
        self.task_list = tkinter.Label(self.root)

        self.things_done = tkinter.Entry(self.root)
        self.things_in_progress = tkinter.Entry(self.root)
        self.problems = tkinter.Entry(self.root)

        self.configure_button_widgets()
        self.configure_input_widgets()
        self.configure_status_widgets()

    def configure_button_widgets(self):
        self.submit_button.config(text="Submit")
        self.submit_button.grid(row=3, column=1)

        self.open_file.config(text="Open file")
        self.open_file.grid(row=4, column=0)

        self.list_button.config(text="List")
        self.list_button.grid(row=4, column=1)

    def configure_input_widgets(self):
        tkinter.Label(self.root, text="What was done: ").grid(row=0, column=0)
        self.things_done.grid(row=0, column=1)
        self.things_done.focus_set()

        tkinter.Label(self.root, text="What needs to be done: ").grid(row=1, column=0)
        self.things_in_progress.grid(row=1, column=1)

        tkinter.Label(self.root, text="Any problems: ").grid(row=2, column=0)
        self.problems.grid(row=2, column=1)

    def configure_status_widgets(self):
        self.task_status.config(text="Task status")
        self.task_status.grid(row=0, column=2)

        self.task_list.grid(row=1, column=2, rowspan=4)
        self.task_list.config(font=(self.config_manager.font_family, self.config_manager.font_size_task_list))
