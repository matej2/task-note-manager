import tkinter as tk
from tkinter import ttk

from manager.ConfigManager import ConfigManager


class Loader(tk.Frame):
    def __init__(self, parent, config_manager: ConfigManager, text="Loading..."):
        super().__init__(parent, bg=config_manager.FRAME_BACKGROUND)
        inner = tk.Frame(self, bg=config_manager.FRAME_BACKGROUND)
        inner.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(inner, text=text, bg=config_manager.FRAME_BACKGROUND,
                 font=config_manager.get_regular_font()).pack(pady=(0, 10))

    def show(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.tkraise()               # raise above all siblings
        self.update_idletasks()   # make sure it paints right away

    def hide(self):
        self.place_forget()