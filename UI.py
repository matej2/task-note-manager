import tkinter
import typing

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

        self.instruction_container = tkinter.Frame(self.root)

        self.task_list = tkinter.Label(self.root)

        self.things_done = tkinter.Text(self.root)
        self.things_in_progress = tkinter.Text(self.root)
        self.problems = tkinter.Text(self.root)

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
        tkinter.Label(self.root, text="Latest note: ", font=self.get_font_config()).grid(row=0, column=2)

        self.task_list.grid(row=1, column=2, rowspan=3, sticky='n')
        self.task_list.config(justify=tkinter.LEFT, font=(self.config_manager.font_family, self.config_manager.font_size_small))

    def configure_instructions(self):
        title = tkinter.Label(self.instruction_container)
        title.config(text="Task note manager", font=(self.config_manager.font_family, self.config_manager.font_size_large))
        title.grid(row=0, column=0)

        instructions = tkinter.Label(self.instruction_container)
        instructions.config(text="Application asks you 3 question about your daily work. \nQuestions are designed so that the data you provide is useful for reports, meetings and notes. \nApplication will save this data to a yaml file, which you can see by clicking 'Open file' button. \nYou can further edit data in this file to adapt it to your requrements.")
        instructions.grid(row=1, column=0)

        self.instruction_container.grid(row=0, column=0, columnspan=2)

