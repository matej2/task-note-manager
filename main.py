import tkinter
from datetime import datetime, timedelta, timezone
from tkinter import END, NORMAL, DISABLED

import notify2

from ConfigManager import ConfigManager
from DataManager import DataManager
from ExportManager import ExportManager
from FileManager import FileManager
from Scheduler import Scheduler
from UI import UI
from models.NoteEntry import NoteEntry


class Application(UI):
    def __init__(self):
        self.config_manager = ConfigManager()
        super().__init__(self.config_manager)

        self.file_manager = FileManager(self.config_manager)
        self.data_manager = DataManager(self.things_done, self.things_in_progress, self.problems, self.task_list_container, self.file_manager, self.config_manager)
        self.export_manager = ExportManager(self.config_manager, self.data_manager)

        self.update_time_until_next_run(datetime.now(timezone.utc) + timedelta(hours=self.config_manager.frequency_hours))
        self.scheduler = Scheduler(self.trigger_notification, self.update_time_until_next_run, self.config_manager)

        self.configure_buttons()
        self.initialize()

    def initialize(self):
        notify2.init("test")
        self.update_data()

        today_data = self.data_manager.get_today_data_single()
        self.init_inputs(today_data)

    def configure_buttons(self):
        self.submit_button.config(command=self.on_click_submit_button)
        self.open_file.config(command=self.data_manager.file_manager.open_file)
        self.export_button.config(command=self.export_manager.export_data)

    def on_click_submit_button(self):
        self.data_manager.write_value()
        self.update_data()

        self.notification.config(text="")
        self.task_list.see(tkinter.END)

    def init_inputs(self, entry: NoteEntry):
        self.set_text(self.things_done, entry.things_done)
        self.set_text(self.things_in_progress, entry.to_be_done)
        self.set_text(self.problems, entry.problems)

    @staticmethod
    def set_text_and_disable(text: tkinter.Text, value: str):
        text.configure(state=NORMAL)
        Application.set_text(text, value)
        text.configure(state=DISABLED)

    @staticmethod
    def set_text(text: tkinter.Text, value: str):
        text.delete(1.0, END)
        text.insert(END, value)

    def update_data(self):
        today_note = self.data_manager.get_today_data()
        Application.set_text_and_disable(self.task_list, str(today_note))

    def trigger_notification(self):
        notify2.Notification("Daily notification to enter data").show()
        self.root.focus_force()
        self.notification.config(text="Daily notification to enter data")

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application().start()
