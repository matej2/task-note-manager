import tkinter

from DataManager import DataManager


def main():
    master = tkinter.Tk()

    tkinter.Label(master, text="First Name").grid(row=0)
    things_done = tkinter.Entry(master)
    things_done.grid(row=0, column=1)

    data_manager = DataManager(things_done)

    button = tkinter.Button(master, text="Enter", command=data_manager.get_value)
    button.grid(row=1, column=0)

    master.mainloop()


if __name__ == "__main__":
    main()
