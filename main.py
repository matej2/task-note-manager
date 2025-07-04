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
from factory.NotesFactory import NotesFactory
from models.NoteEntry import NoteEntry
from notification.Notification import Notification


class Application(UI):
    def __init__(self):
        self.config_manager = ConfigManager()
        super().__init__(self.config_manager)

        self.file_manager = FileManager(self.config_manager)
        self.note_factory = NotesFactory(self.config_manager)
        self.notification = Notification(self.config_manager)

        self.data_manager = DataManager(
            self.done_field,
            self.in_progress_field,
            self.problems_field,
            self.task_list_container,
            self.file_manager,
            self.config_manager,
            self.note_factory
        )
        self.export_manager = ExportManager(self.config_manager, self.data_manager)

        self._update_time_until_next_run(datetime.now(timezone.utc) + timedelta(hours=self.config_manager.frequency_hours))
        self.scheduler = Scheduler(self.__trigger_notification, self._update_time_until_next_run, self.config_manager)

        self.__configure_buttons()
        self.__initialize()

    def __initialize(self):
        notify2.init("test")
        self.__update_data()

        today_data = self.data_manager.get_data_for_current_day()
        self.__init_inputs(today_data)

    def __configure_buttons(self):
        self.submit_button.config(command=self.__on_click_submit_button)
        self.open_file.config(command=self.data_manager.file_manager.open_file)
        self.export_button.config(command=self.export_manager.export_data)

    def __on_click_submit_button(self):
        self.data_manager.save_input_data()
        self.__update_data()

        self.notification.config(text="")
        self.task_list.see(tkinter.END)

    def __init_inputs(self, entry: NoteEntry):
        self.__set_text(self.done_field, entry.done)
        self.__set_text(self.in_progress_field, entry.in_progress)
        self.__set_text(self.problems_field, entry.problems)

    @staticmethod
    def __set_text_and_disable(text: tkinter.Text, value: str):
        text.configure(state=NORMAL)
        Application.__set_text(text, value)
        text.configure(state=DISABLED)

    @staticmethod
    def __set_text(text: tkinter.Text, value: str):
        text.delete(1.0, END)
        text.insert(END, value)

    def __update_data(self):
        today_note = self.data_manager.get_data_for_current_day()
        Application.__set_text_and_disable(self.task_list, str(today_note))

    def __trigger_notification(self):
        self.notification.send_notification()
        self.root.focus_force()
        self.notification.config(text="Daily notification to enter data")

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application().start()
