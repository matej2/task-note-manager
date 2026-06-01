import asyncio
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from customtkinter import END, NORMAL, DISABLED, CTkTextbox as Text

import notify2

from src.Scheduler import Scheduler
from src.UI import UI
from src.factory.NoteEntryFactory import NoteEntryFactory
from src.manager.ConfigManager import ConfigManager
from src.manager.DataManager import DataManager
from src.manager.ExportManager import ExportManager
from src.manager.FileManager import FileManager
from src.manager.TaskManager import TaskManager
from src.models.NoteEntry import NoteEntry
from src.models.NoteList import NoteList
from src.notification.Notification import Notification


class Application(UI):
    def __init__(self):
        self.config_manager = ConfigManager()
        super().__init__(self.config_manager)

        self.current_data = NoteList(list())

        asyncio.run(self.__init_wrapper())

    async def __init_wrapper(self):
        self.__setup()
        await self.__after_setup()


    def __setup(self):
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
            self.note_factory,
            self.current_data
        )
        self.task_manager = TaskManager(self.config_manager)
        self.export_manager = ExportManager(self.config_manager, self.data_manager, self.task_manager, self.current_data)

        self._update_time_until_next_run(datetime.now(timezone.utc) + timedelta(hours=self.config_manager.frequency_hours))
        self.scheduler = Scheduler(self.__trigger_notification, self._update_time_until_next_run, self.config_manager)

        self.__configure_buttons()
        self.__configure_bindings()

    async def __after_setup(self):
        self.current_data = await self.data_manager.read_data_from_file_async_direct()
        await self.__update_data()
        await self.initialize_data_fields()

    async def initialize_data_fields(self):
        today_note_entry = self.data_manager.extract_today_notes(self.current_data)
        self.__set_note_input_text(today_note_entry)

    def __configure_buttons(self):
        self.submit_button.configure(command=self.__on_click_submit_button)
        self.open_file.configure(command=self.data_manager.file_manager.open_file_in_ext_app)
        self.export_button.configure(command=self.__on_click_export_button)

    def __on_click_export_button(self):
        asyncio.run(self.process_export())

    async def process_export(self):
        await self.data_manager.process_save_input(self.current_data)
        await self.export_manager.export_data(self.current_data)
        Notification.send_info_notification("Export completed")


    def __after_submit(self, note_list: NoteList):
        self.notification.configure(text="")
        self.task_list.see(END)
        all_task_names = [str(s.name)+", " for s in self.task_manager.get_tasks_from_note_list(note_list)]
        task_names = "".join(list(OrderedDict.fromkeys(all_task_names)))
        self.task_name_list.configure(text=f"Tasks:\n\n{task_names}")

    def __on_click_submit_button(self, *args):
        asyncio.run(self.save_data())
        return "break"

    async def save_data(self):
        self.current_data = await self.data_manager.process_save_input(self.current_data)
        await self.__update_data()
        Notification.send_info_notification("Data saved")

    def __set_note_input_text(self, entry: NoteEntry):
        self.__set_text(self.done_field, entry.done)
        self.__set_text(self.in_progress_field, entry.in_progress)
        self.__set_text(self.problems_field, entry.problems)

    @staticmethod
    def __set_text_and_disable(field:Text, value: str):
        field.configure(state=NORMAL)
        Application.__set_text(field, value)
        field.configure(state=DISABLED)

    @staticmethod
    def __set_text(text: Text, value: str):
        text.delete(1.0, END)
        text.insert(END, str(value))

    async def __update_data(self):
        formatted_note_entries = [(f"Date: {n.date}\n"
                                   f"- Done: {n.done}\n"
                                   f"- In progress: {n.in_progress}\n"
                                   f"- Problems: {n.problems}") for n in self.current_data.notes]
        formatted_note_output = "\n\n".join(formatted_note_entries)

        today_note_entry = self.data_manager.extract_today_notes(self.current_data)


        self.__set_text_and_disable(self.task_list, formatted_note_output)
        self.__set_note_input_text(today_note_entry)
        self.__after_submit(self.current_data)

    def __trigger_notification(self):
        self.notification_manager.send_notification()
        self.root.focus_force()
        self.notification.configure(text="Daily notification to enter data")

    def __configure_bindings(self):
        self.__set_bindings(self.done_field)
        self.__set_bindings(self.in_progress_field)
        self.__set_bindings(self.problems_field)

    def __set_bindings(self, widget):
        widget.bind("<Tab>", UI._focus_next_widget)
        widget.bind("<Control_L>s", self.__on_click_submit_button)

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application().start()
