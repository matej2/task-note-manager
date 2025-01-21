import tkinter

from ConfigManager import ConfigManager


class UI(tkinter.Frame):

    def __init__(self, config: ConfigManager):
        self.root = tkinter.Tk()
        tkinter.Frame.__init__(self, self.root)
        self.config_manager = config

        self.button_container = tkinter.Frame(self.root)
        self.submit_button = tkinter.Button(self.button_container)
        self.open_file = tkinter.Button(self.button_container)
        self.list_button = tkinter.Button(self.button_container)

        self.task_list = tkinter.Label(self.root)

        self.things_done = tkinter.Entry(self.root)
        self.things_in_progress = tkinter.Entry(self.root)
        self.problems = tkinter.Entry(self.root)

        self.configure_button_widgets()
        self.configure_input_widgets()
        self.configure_status_widgets()

    def configure_button_widgets(self):
        self.button_container.grid(row=3, column=0, columnspan=2)

        self.submit_button.config(text="Submit")
        self.submit_button.grid(row=0, column=0, padx=30)

        self.open_file.config(text="Open file")
        self.open_file.grid(row=0, column=1)

    def configure_input_widgets(self):
        tkinter.Label(self.root, text="What was done: ").grid(row=0, column=0)
        self.things_done.grid(row=0, column=1)
        self.things_done.focus_set()

        tkinter.Label(self.root, text="What needs to be done: ").grid(row=1, column=0)
        self.things_in_progress.grid(row=1, column=1)

        tkinter.Label(self.root, text="Any problems: ").grid(row=2, column=0)
        self.problems.grid(row=2, column=1)

    def configure_status_widgets(self):
        self.task_list.grid(row=1, column=2, rowspan=4)
        self.task_list.config(font=(self.config_manager.font_family, self.config_manager.font_size_task_list))
