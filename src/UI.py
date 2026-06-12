from datetime import datetime, timezone
from tkinter import BaseWidget

from customtkinter import LEFT, CTkFrame as Frame, CTk as Tk, CTkButton as Button, CTkLabel as Label, \
    CTkToplevel as Toplevel, CTkTextbox as Text

from src.manager.ConfigManager import ConfigManager
from src.manager.UILayoutHelper import UILayoutHelper


class UI(Frame):

    def __init__(self, config: ConfigManager):
        self.config_manager = config
        self.ui_helper = UILayoutHelper(config)

        self.root_container = Tk()
        self.root_container.title("Task note manager")
        self.root_container.configure(fg_color=self.config_manager.FRAME_BACKGROUND)

        self.root_container.grid_rowconfigure(0, weight=1)
        self.root_container.grid_columnconfigure(0, weight=1)

        Frame.__init__(self, self.root_container)
        self.root = Frame(self.root_container, fg_color=self.config_manager.FRAME_BACKGROUND)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.root.grid(row=0, column=0, padx=20, pady=20 , sticky="nsew")

        # Buttons
        self.submit_button = Button(None)
        self.open_file = Button(None)
        self.list_button = Button(None)
        self.instructions_button = Button(None)
        self.export_button = Button(None)

        # Task list
        self.task_list_container = self.ui_helper.display_frame(self.root, 0, 1)
        self.task_list = None
        self.task_name_list = None

        # Input fields
        self.input_container = self.ui_helper.display_frame(self.root, 0, 0)
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
        self.submit_button = self.ui_helper.display_button("Submit",self.input_container,6,0, True)
        self.open_file = self.ui_helper.display_button("Open YAML File", self.task_list_container, 4, 0)
        self.export_button = self.ui_helper.display_button("Export data to ODS", self.task_list_container, 4, 1)
        self.instructions_button = self.ui_helper.display_button("About", self.task_list_container, 4, 2)

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


    def __configure_status_widgets(self):
        self.ui_helper.display_todays_notes_label("Todays notes: ", self.task_list_container, 0, 0)

        self.task_list = self.ui_helper.display_status_input(
            self.task_list_container,
            1,
            0
        )

        self.ui_helper.display_todays_notes_label("Task list: ", self.task_list_container, 2, 0)

        self.task_name_list = self.ui_helper.display_status_input(
            self.task_list_container,
            3,
            0
        )
        self.task_name_list.configure(height=100, width=400)

    def __configure_scheduler_widgets(self):
        self.scheduler_container  = self.ui_helper.display_frame(self.root, 2, 0, columnspan=2)

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
        top.title("About")
        top.configure(padx=10, pady=10)

        instructions_frame = self.ui_helper.display_frame(top, 1, 0, "How to use")

        self.ui_helper.display_new_note_label("1. Launch the application at the start of your workday (manually or via startup autorun).\n2. Leave the app running quietly in the background.\n3. After 6 hours of runtime, a prompt will automatically appear on your screen.\n4. Answer 3 quick questions about your completed tasks and progress.\n5. Your log is securely saved, and you can access, edit, or export your data at any time.", instructions_frame, 0, 0)

        about_frame = self.ui_helper.display_frame(top, 0, 0, "About")

        self.ui_helper.display_new_note_label(f"Task Note Manager is a streamlined tool designed to help you effortlessly track and log your daily work activities.\n\nKey Features & Benefits:\n• Automated Reminders: The app automatically prompts you for input after 6 hours of runtime.\n• Structured Insights: Answer 3 simple questions to capture crucial details about your workday.\n• Meeting & Report Ready: Generated notes are perfect for daily standups, status updates, or personal tracking.\n• Local Storage: All data is saved safely in a clean, human-readable YAML format.\n• Full Control: Click the 'Open file' button to view, edit, or copy entries directly. Every log is marked with '!NoteEntry' for easy customization.\n\nData is saved in YAML file at {self.config_manager.FULL_PATH}", about_frame, 0, 0)
