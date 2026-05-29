from datetime import datetime, timezone
from tkinter import BaseWidget

from customtkinter import LEFT, CTkFrame as Frame, CTk as Tk, CTkButton as Button, CTkLabel as Label, \
    CTkToplevel as Toplevel

from src.manager.ConfigManager import ConfigManager
from src.manager.UILayoutHelper import UILayoutHelper


class UI(Frame):

    def __init__(self, config: ConfigManager):
        self.config_manager = config
        self.ui_helper = UILayoutHelper(config)

        self.root_container = Tk()
        self.root_container.title("Task note manager")
        self.root_container.configure(fg_color=self.config_manager.FRAME_BACKGROUND)

        Frame.__init__(self, self.root_container)
        self.root = Frame(self.root_container, fg_color=self.config_manager.FRAME_BACKGROUND)
        self.root.grid(row=0, column=0, padx=20, pady=20)

        # Buttons
        self.button_container = Frame(None)
        self.submit_button = Button(None)
        self.open_file = Button(None)
        self.list_button = Button(None)
        self.instructions_button = Button(None)
        self.export_button = Button(None)

        # Task list
        self.task_list_container = Frame(None)
        self.task_list = None
        self.task_name_list = Label(None)

        # Input fields
        self.input_container = Frame(None)
        self.done_field = None
        self.in_progress_field = None
        self.problems_field = None

        # Scheduler
        self.scheduler_container = Frame(None)
        self.counter = Label(None)
        self.notification = Label(None)

        self.__configure_button_widgets()
        self.__configure_input_widgets()
        self.__configure_status_widgets()
        self.__configure_scheduler_widgets()


    def __configure_button_widgets(self):
        self.button_container = self.ui_helper.display_frame(self.root, 4, 0, columnspan=3, sticky='e')

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
        self.input_container = self.ui_helper.display_frame(self.root, 1, 0, sticky='n')

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


    def __configure_status_widgets(self):
        self.task_list_container =  self.ui_helper.display_frame(self.root, 1, 2, rowspan=3, sticky='n')

        self.ui_helper.display_new_note_label("Todays notes: ", self.task_list_container, 0, 0)

        self.task_list = self.ui_helper.display_status_input(
            self.task_list_container,
            1,
            0
        )

        self.task_name_list = self.ui_helper.display_new_note_label(
            "",
            self.task_list_container,
            3,
            0
        )


    def __configure_scheduler_widgets(self):
        self.scheduler_container  = self.ui_helper.display_frame(self.root, 5, 0)

        self.counter = self.ui_helper.display_new_note_label("Remaining time: --:--", self.scheduler_container,0, 0)
        self.notification = self.ui_helper.display_warning_label("", self.scheduler_container, 0, 1)

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

        instructions_frame = self.ui_helper.display_frame(top, 1, 0, "How to use")

        self.ui_helper.display_new_note_label("1. Run the application at the start of your workday (manually or via autorun).\n2. After 6 hours of runtime, a prompt will appear to log your daily progress.", instructions_frame, 0, 0)

        about_frame = self.ui_helper.display_frame(top, 0, 0, "About")

        self.ui_helper.display_new_note_label("This application helps you effortlessly track your daily work activities.\n\nKey Features:\n• Answer 3 simple questions about your workday.\n• Generate useful data for reports, meetings, and personal notes.\n• Automatically save all responses into a human-readable YAML file.\n\nClick the 'Open file' button to view or manually edit your data. Each entry is marked with '!NoteEntry' for easy copying and customization.", about_frame, 0, 0)
