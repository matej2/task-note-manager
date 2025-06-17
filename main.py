import tkinter
from datetime import datetime, timedelta, timezone
from tkinter import END, NORMAL, DISABLED

import notify2

from ConfigManager import ConfigManager
from DataManager import DataManager
from ExportManager import ExportManager
from FileManager import FileManager
from Scheduler import Scheduler
from TaskManager import TaskManager
from UI import UI
from models.NoteEntry import NoteEntry


class Application(UI):
    def __init__(self):
        self.config_manager = ConfigManager()
        self.file_manager = FileManager(self.config_manager)
        super().__init__(self.config_manager)

        self.data_manager = DataManager(self.things_done, self.things_in_progress, self.problems, self.task_list_container, self.file_manager, self.config_manager)
        self.export_manager = ExportManager(self.config_manager, self.data_manager)

        self.update_time_until_next_run(datetime.now(timezone.utc) + timedelta(hours=self.config_manager.frequency_hours))
        self.scheduler = Scheduler(self.trigger_notification, self.update_time_until_next_run, self.config_manager)

        self.configure_widgets()

        self.initialize()

    def initialize(self):
        notify2.init("test")
        self.update_data()

        today_data = self.data_manager.get_today_data_single()
        self.init_inputs(today_data)

    def configure_widgets(self):
        self.submit_button.config(command=self.on_click_submit_button)
        self.open_file.config(command=self.data_manager.file_manager.open_file)
        self.export_button.config(command=self.export_manager.export_data)


    def on_click_submit_button(self):
        self.data_manager.write_value()
        self.update_data()

        self.notification.config(text="")
        self.task_list.see(tkinter.END)

    def init_inputs(self, entry: NoteEntry):
        self.fill_input_value(self.things_done, entry.things_done)
        self.fill_input_value(self.things_in_progress, entry.to_be_done)
        self.fill_input_value(self.problems, entry.problems)

    @staticmethod
    def set_input_disabled(text: tkinter.Text, value: str):
        text.configure(state=NORMAL)
        Application.fill_input_value(text, value)
        text.configure(state=DISABLED)

    @staticmethod
    def fill_input_value(text: tkinter.Text, value: str):
        text.delete(1.0, END)
        text.insert(END, value)

    def update_data(self):
        today_note = self.data_manager.get_today_data()
        self.output_task_data(today_note)
        self.output_task_names(today_note)

    def output_task_data(self, note: NoteEntry):
        if note.is_empty():
            text = "No data"
        else:
            text = str(note)

        Application.set_input_disabled(self.task_list, text)

    def output_task_names(self, note: NoteEntry):
        task_names = TaskManager.get_task_names(note)
        self.task_name_list.config(text=task_names)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return ("break")

    def trigger_notification(self):
        notify2.Notification("Daily notification to enter data").show()
        self.root.focus_force()
        self.notify()

    def notify(self):
        self.notification.config(text="Daily notification to enter data")

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application().start()
