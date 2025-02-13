import tkinter
from datetime import datetime, timedelta, timezone
from tkinter import END, NORMAL, DISABLED

from ConfigManager import ConfigManager
from DataManager import DataManager
from FileManager import FileManager
from Scheduler import Scheduler
from UI import UI


class Application(UI):
    def __init__(self):
        self.config_manager = ConfigManager()
        self.file_manager = FileManager(self.config_manager)
        super().__init__(self.config_manager)

        self.data_manager = DataManager(self.things_done, self.things_in_progress, self.problems, self.task_list_container, self.file_manager)

        self.update_time_until_next_run(datetime.now(timezone.utc) + timedelta(hours=self.config_manager.frequency_hours))
        self.scheduler = Scheduler(self.trigger_notification, self.update_time_until_next_run, self.config_manager)

        self.configure_widgets()

        self.initialize()

    def initialize(self):
        self.list_data()

    def configure_widgets(self):
        self.submit_button.config(command=self.on_click_submit_button)
        self.open_file.config(command=self.data_manager.file_manager.open_file)


    def create_key_shortcuts(self):
        self.root.bind('<Return>', self.data_manager.write_value)
        self.things_done.bind('<Return>', self.data_manager.write_value)
        self.things_done.bind("<Tab>", self.focus_next_widget)
        self.things_in_progress.bind("<Tab>", self.focus_next_widget)
        self.problems.bind("<Tab>", self.focus_next_widget)

    def on_click_submit_button(self):
        self.data_manager.write_value()
        self.list_data()

        self.notification.config(text="")

    @staticmethod
    def on_change_frequency(var, index, mode):
        print(var, index, mode)

    @staticmethod
    def set_input(text: tkinter.Text, value: str):
        text.configure(state=NORMAL)
        text.delete(1.0, END)
        text.insert(END, value)
        text.configure(state=DISABLED)

    def list_data(self):
        note_list = self.data_manager.get_today_data()
        if len(note_list) == 0:
            text = "No data"
        else:
            text = note_list

        Application.set_input(self.task_list, text)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return ("break")

    def trigger_notification(self):
        self.root.deiconify()
        self.root.focus_force()
        self.notify()

    def notify(self):
        self.notification.config(text="Daily notification to enter data")

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application().start()
