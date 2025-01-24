import tkinter

from ConfigManager import ConfigManager
from DataManager import DataManager
from UI import UI


class Application(UI):
    def __init__(self):
        self.config_manager = ConfigManager()
        super().__init__(self.config_manager)

        self.data_manager = DataManager(self.things_done, self.things_in_progress, self.problems, self.task_list)
        self.configure_widgets()

        self.initialize()

    def initialize(self):
        self.list_data()

    def configure_widgets(self):
        self.submit_button.config(command=self.on_click_submit_button)
        self.open_file.config(command=self.data_manager.file_manager.open_file)

    def create_key_shortcuts(self):
        self.root.bind('<Return>', self.data_manager.add_value)
        self.things_done.bind('<Return>', self.data_manager.add_value)
        self.things_done.bind("<Tab>", self.focus_next_widget)
        self.things_in_progress.bind("<Tab>", self.focus_next_widget)
        self.problems.bind("<Tab>", self.focus_next_widget)

    def on_click_submit_button(self):
        self.data_manager.add_value()
        self.list_data()

    def list_data(self):
        note_list = self.data_manager.get_today_data()
        if len(note_list) == 0:
            text = tkinter.StringVar(value="No data")
        else:
            text = tkinter.StringVar(value=note_list)

        self.task_list.config(textvariable=text)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return ("break")

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application().start()
