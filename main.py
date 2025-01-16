import tkinter

from DataManager import DataManager


class Application(tkinter.Frame):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry("300x200")
        tkinter.Frame.__init__(self, self.root)

        self.create_input_widgets()

        self.data_manager = DataManager(self.things_done)
        self.root.bind('<Return>', self.data_manager.get_value)

        self.create_buttons()

    def create_input_widgets(self):
        tkinter.Label(self.root, text="First Name").grid(row=0)

        self.things_done = tkinter.Entry(self.root)
        self.things_done.grid(row=0, column=1)
        self.things_done.focus_set()

    def create_buttons(self):
        self.button = tkinter.Button(self.root, text="Enter", command=self.data_manager.get_value)
        self.button.grid(row=1, column=0)

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application().start()
