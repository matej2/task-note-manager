import tkinter

from ConfigManager import ConfigManager
from DataManager import DataManager
from UI import UI


class Application(UI):
    def __init__(self):
        self.config_manager = ConfigManager()

        super().__init__(self.config_manager)

        self.note_list_output = []


        # Data manager needs to be initialized after input widgets are created
        self.data_manager = DataManager(self.things_done, self.things_in_progress, self.problems, self.task_list)
        self.configure_widgets()

        self.initialize()

    def initialize(self):
        self.list_data()

    def configure_widgets(self):
        self.submit_button.config(command=self.on_click_submit_button)
        self.open_file.config(command=self.data_manager.file_manager.open_file)
        self.list_button.config(command=self.list_data)

    def create_key_shortcuts(self):
        self.root.bind('<Return>', self.data_manager.add_value)

    def on_click_submit_button(self):
        self.data_manager.add_value()
        self.list_data()

        self.task_status.config(text="Task created")

    def list_data(self):
        note_list = self.data_manager.read_data()
        text = tkinter.StringVar(value=str(note_list))

        self.task_list.config(textvariable=text)


    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application().start()
