from datetime import datetime, timezone
from tkinter import BaseWidget

from customtkinter import DISABLED, LEFT, WORD, CTkFrame as Frame, CTk as Tk, CTkButton as Button, CTkTextbox as Text, \
    CTkLabel as Label, CTkToplevel as Toplevel

from src.manager.ConfigManager import ConfigManager
from src.manager.UILayoutHelper import UILayoutHelper


class UI(Frame):

    def __init__(self, config: ConfigManager):
        self.root_container = Tk()
        self.root_container.title("Task note manager")

        Frame.__init__(self, self.root_container)
        self.root = Frame(self.root_container)
        self.root.grid(row=0, column=0, padx=20, pady=20)

        self.config_manager = config
        self.ui_helper = UILayoutHelper(config)

        # Buttons
        self.button_container = Frame(self.root)
        self.submit_button = Button(None)
        self.open_file = Button(None)
        self.list_button = Button(None)
        self.instructions_button = Button(None)
        self.export_button = Button(None)

        # Task list
        self.task_list_container = Frame(self.root)
        self.task_list = Text(self.task_list_container)
        self.task_name_list = Label(self.task_list_container)

        # Input fields
        self.input_container = Frame(self.root, border_color="black", border_width=2)
        self.done_field = Text(self.input_container)
        self.in_progress_field = Text(self.input_container)
        self.problems_field = Text(self.input_container)

        # Scheduler
        self.scheduler_container = Frame(self.root)
        self.counter = Label(self.scheduler_container)
        self.notification = Label(self.scheduler_container)

        self.__configure_button_widgets()
        self.__configure_input_widgets()
        self.__configure_status_widgets()
        self.__configure_scheduler_widgets()


    def __configure_button_widgets(self):
        self.button_container.grid(row=4, column=0, columnspan=3, sticky='e', pady=(10, 20))

        self.submit_button = self.ui_helper.display_button("Submit", self.button_container, 0, 0)
        self.open_file = self.ui_helper.display_button("Open File", self.button_container, 0, 1)
        self.export_button = self.ui_helper.display_button("Export data - ODS", self.button_container, 0, 4)
        self.instructions_button = self.ui_helper.display_button("Instructions", self.button_container, 0, 3)

        self.instructions_button.configure(command=self.__open_information_popup)


    @staticmethod
    def _focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"


    def __configure_input_widgets(self):
        self.ui_helper.display_new_note_label(
            "What was done: ",
            self.input_container,
            0,
            0
        )
        self.done_field = self.ui_helper.display_new_note_input(
            self.input_container,
            1,
            0
        )
        self.done_field.focus_set()

        self.ui_helper.display_new_note_label(
            "What needs to be done: ",
            self.input_container,
            2,
            0
        )
        self.in_progress_field = self.ui_helper.display_new_note_input(
            self.input_container,
            3,
            0
        )

        self.ui_helper.display_new_note_label(
            "Any problems: ",
            self.input_container,
            4,
            0
        )
        self.problems_field = self.ui_helper.display_new_note_input(
            self.input_container,
            5,
            0
        )
        self.input_container.grid(row=1, column=0, sticky='n', padx=20, pady=20)

    def __configure_status_widgets(self):
        Label(self.task_list_container, text="Todays notes: ", font=self.config_manager.get_header_font()).grid(row=0, column=0)

        self.task_list.configure(wrap=WORD,
                              font=self.config_manager.get_regular_font(),
                              state=DISABLED)
        self.task_list.grid(row=1, column=0)

        self.task_name_list.configure(wraplength=300, justify=LEFT)
        self.task_name_list.grid(row=3, column=0)

        self.task_list_container.grid(row=1, column=2, rowspan=3, sticky='n', padx=10)

    def __configure_scheduler_widgets(self):
        self.scheduler_container.grid(row=5, column=0)
        self.counter.configure(font=self.config_manager.get_regular_font(), text="Remaining time: --:--")
        self.counter.grid(row=0, column=0)

        self.notification.configure(text_color="red", font=self.config_manager.get_regular_font())
        self.notification.grid(row=0, column=1)

    def _update_time_until_next_run(self, next_run_time: datetime):
        if next_run_time:
            now = datetime.now(timezone.utc)
            time_until_next_run = next_run_time - now

            # Format the time difference
            hours, remainder = divmod(time_until_next_run.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02}:{minutes:02}"

            # Update the label in the Tkinter GUI
            self.counter.configure(text=f"Notification in: {time_str} hours")
        else:
            self.counter.configure(text="No upcoming notification")

    def __create_section(self, parent: BaseWidget, title: str, body: str):
        section = Frame(parent)
        Label(section, text=title, font=(self.config_manager.FONT_FAMILY, self.config_manager.FONT_SIZE_NORMAL, "bold")).grid(row=0, column=0)
        Label(section, text=body, font=self.config_manager.get_regular_font(), wraplength=400,
                      justify=LEFT).grid(row=1, column=0)
        return section

    def __open_information_popup(self):
        top = Toplevel(self.root)
        top.title("About application")
        top.configure(padx=10, pady=10)

        instructions = self.__create_section(top, "Instructions", """At the start of a workday, run the application - either manual or you can set it to autorun at startup. 6 hours from application startup, you will be asked to provide data.
                    """)
        instructions.grid(row=0, column=0)

        about = self.__create_section(top, "About", """This application is designed to keep track of your daily work. It will ask you 3 question. The data you provide using these questions is useful for reports, meetings and notes. 

Application will save these answers to a yaml file, which you can see by clicking 'Open file' button. You can further edit data in this file to adapt it to your requrements. Each entry is marked with "!NoteEntry", you may copy it and modify it.
            """)
        about.grid(row=1, column=0)

        config_list = Label(top)
        config_list.configure(
            text="Configuration:\n" + str(self.config_manager),
            wraplength=400,
            justify=LEFT,
            font="TkFixedFont"
        )
        config_list.grid(row=3, column=0)
