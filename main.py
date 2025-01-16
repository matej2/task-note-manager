import tkinter

from DataManager import DataManager


class Application(tkinter.Frame):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry("300x200")
        tkinter.Frame.__init__(self, self.root)

        self.create_input_widgets()

        self.data_manager = DataManager(self.things_done, self.things_in_progress, self.problems)
        self.root.bind('<Return>', self.data_manager.get_value)

        self.create_action_widgets()

    def create_input_widgets(self):
        tkinter.Label(self.root, text="What was done: ").grid(row=0, column=0)
        self.things_done = tkinter.Entry(self.root)
        self.things_done.grid(row=0, column=1)
        self.things_done.focus_set()

        tkinter.Label(self.root, text="What needs to be done: ").grid(row=1, column=0)
        self.things_in_progress = tkinter.Entry(self.root)
        self.things_in_progress.grid(row=1, column=1)

        tkinter.Label(self.root, text="Any problems: ").grid(row=2, column=0)
        self.problems = tkinter.Entry(self.root)
        self.problems.grid(row=2, column=1)

    def create_action_widgets(self):
        self.button = tkinter.Button(self.root, text="Enter", command=self.data_manager.get_value)
        self.button.grid(row=3, column=0)

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application().start()
