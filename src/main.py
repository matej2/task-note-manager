import asyncio
import tkinter
from datetime import datetime, timedelta, timezone
from tkinter import END, NORMAL, DISABLED

import notify2

from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager
from src.manager.ExportManager import ExportManager
from src.manager.FileManager import FileManager
from Scheduler import Scheduler
from UI import UI
from factory.NoteEntryFactory import NoteEntryFactory
from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList
from src.notification.Notification import Notification


class Application(UI):
    def __init__(self):
        self.config_manager = ConfigManager()
        super().__init__(self.config_manager)

        self.file_manager = FileManager(self.config_manager)
        self.note_factory = NoteEntryFactory(self.config_manager)
        self.notification_manager = Notification(self.config_manager)

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
        self.__configure_bindings()
        self.__initialize()

    def __initialize(self):
        notify2.init("test")
        asyncio.run(self.initialize_data_fields())


    async def initialize_data_fields(self):
        note_list = await self.data_manager.read_data_from_file_async_direct()
        await self.__update_data(note_list)

        today_note_entry = self.data_manager.extract_today_notes(note_list)
        self.__init_inputs(today_note_entry)


    def __configure_buttons(self):
        self.submit_button.config(command=self.__on_click_submit_button)
        self.open_file.config(command=self.data_manager.file_manager.open_file_in_ext_app)
        self.export_button.config(command=self.__on_click_export_button)

    def __on_click_export_button(self):
        asyncio.run(self.export_manager.export_data())

    def __after_submit(self):
        self.notification.config(text="")
        self.task_list.see(tkinter.END)

    def __on_click_submit_button(self, *args):
        asyncio.run(self.save_data())
        return "break"

    async def save_data(self):
        updated_note_list = await self.data_manager.save_input_data()
        await self.__update_data(updated_note_list)

    def __init_inputs(self, entry: NoteEntry):
        self.__set_text(self.done_field, entry.done)
        self.__set_text(self.in_progress_field, entry.in_progress)
        self.__set_text(self.problems_field, entry.problems)

    def __set_text_and_disable(self, value: NoteList):
        self.task_list.configure(state=NORMAL)
        self.__set_text(self.task_list, str(value))
        self.task_list.configure(state=DISABLED)

    @staticmethod
    def __set_text(text: tkinter.Text, value: str):
        text.delete(1.0, END)
        text.insert(END, str(value))

    async def __update_data(self, note_list: NoteList):
        self.__set_text_and_disable(note_list)
        self.__init_inputs(note_list.notes[-1])
        self.__after_submit()

    def __trigger_notification(self):
        self.notification_manager.send_notification()
        self.root.focus_force()
        self.notification.config(text="Daily notification to enter data")

    def __configure_bindings(self):
        self.__set_bindings(self.done_field)
        self.__set_bindings(self.in_progress_field)
        self.__set_bindings(self.problems_field)

    def __set_bindings(self, widget):
        widget.bind("<Return>", self.__on_click_submit_button)
        widget.bind("<Tab>", UI._focus_next_widget)
        widget.bind("<Control_L>s", self.__on_click_submit_button)

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application().start()
