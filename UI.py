import tkinter
import typing
from tkinter import RIGHT, Y, NONE, BOTTOM, X, END, TOP, CENTER, DISABLED

from ConfigManager import ConfigManager


class UI(tkinter.Frame):

    def __init__(self, config: ConfigManager):
        self.root = tkinter.Tk()
        self.root.title("Task note manager")

        tkinter.Frame.__init__(self, self.root)
        self.config_manager = config

        # Buttons
        self.button_container = tkinter.Frame(self.root)
        self.submit_button = tkinter.Button(self.button_container)
        self.open_file = tkinter.Button(self.button_container)
        self.list_button = tkinter.Button(self.button_container)

        self.instruction_container = tkinter.Frame(self.root)

        self.task_list_container = tkinter.Frame(self.root)
        self.task_list = tkinter.Text(self.task_list_container)

        # Input fields
        self.things_done = tkinter.Text(self.root)
        self.things_in_progress = tkinter.Text(self.root)
        self.problems = tkinter.Text(self.root)

        # Scheduler
        self.notification = tkinter.Label(self.button_container)


        self.configure_button_widgets()
        self.configure_input_widgets()
        self.configure_status_widgets()
        self.configure_instructions()

    def get_font_config(self) -> tuple:
        return self.config_manager.font_family, self.config_manager.font_size_normal

    def configure_button_widgets(self):
        self.button_container.grid(row=4, column=0, columnspan=2, sticky='e')

        self.submit_button.config(text="Submit", font=self.get_font_config())
        self.submit_button.grid(row=0, column=0, padx=30)

        self.open_file.config(text="Open file", font=self.get_font_config())
        self.open_file.grid(row=0, column=1)

        self.notification.config(highlightcolor="red", fg="red", font=self.get_font_config())
        self.notification.grid(row=0, column=2)

    def configure_input_widgets(self):
        tkinter.Label(self.root, text="What was done: ", font=self.get_font_config()).grid(row=1, column=0)
        self.things_done.grid(row=1, column=1)
        self.things_done.config(font=self.get_font_config(), height=4, width=30, wrap=tkinter.WORD)
        self.things_done.focus_set()

        tkinter.Label(self.root, text="What needs to be done: ", font=self.get_font_config()).grid(row=2, column=0)
        self.things_in_progress.config(font=self.get_font_config(), height=4, width=30, wrap=tkinter.WORD)
        self.things_in_progress.grid(row=2, column=1)

        tkinter.Label(self.root, text="Any problems: ", font=self.get_font_config()).grid(row=3, column=0)
        self.problems.config(font=self.get_font_config(), height=4, width=30, wrap=tkinter.WORD)
        self.problems.grid(row=3, column=1)

    def configure_status_widgets(self):
        tkinter.Label(self.task_list_container, text="Latest note: ", font=self.get_font_config()).grid(row=0, column=0)

        h = tkinter.Scrollbar(self.task_list_container, orient='horizontal', borderwidth=2, relief="groove")
        h.grid(row=2, column=0, sticky='nsew')
        v = tkinter.Scrollbar(self.task_list_container, borderwidth=2, relief="groove")
        v.grid(row=1, column=1, sticky='nsew')

        self.task_list.config(width=30, height=15, wrap=NONE,
            xscrollcommand=h.set,
            yscrollcommand=v.set,
            font=self.get_font_config(),
            state=DISABLED)
        self.task_list.grid(row=1, column=0)

        h.config(command=self.task_list.xview)
        v.config(command=self.task_list.yview)

        self.task_list_container.grid(row=1, column=2, rowspan=3, sticky='n', padx=10)

    def configure_instructions(self):

        instructions = tkinter.Label(self.instruction_container)
        instructions.config(
            text="Application is designed to keep track of your daily work. It will asl you 3 question. These are designed so that the data you provide is useful for reports, meetings and notes. Application will save this data to a yaml file, which you can see by clicking 'Open file' button. You can further edit data in this file to adapt it to your requrements.",
            wraplength=400,
            justify=CENTER,
            font=(self.config_manager.font_family, self.config_manager.font_size_small)
        )
        instructions.grid(row=1, column=0)

        scheduler_description = tkinter.Label(self.instruction_container)
        scheduler_description.config(
            text="When application is running, it will notify you to enter data every 6 hours. You can set appliation to run automatically at startup.",
            wraplength=400,
            justify=CENTER,
            font=(self.config_manager.font_family, self.config_manager.font_size_small)
        )
        scheduler_description.grid(row=2, column=0)

        self.instruction_container.grid(row=0, column=0, columnspan=3)