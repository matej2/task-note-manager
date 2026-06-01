from tkinter import DISABLED, LEFT

from customtkinter import CTkLabel as Label, WORD, CTkFrame as Frame, CTkTextbox as Text, CTkTextbox, \
    CTkButton as Button, CTkToplevel as Toplevel

from src.manager.ConfigManager import ConfigManager


class UILayoutHelper:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager

    def display_new_note_input(self, parent: Frame, row: int, column: int) -> CTkTextbox:
        field = Text(master=parent)
        field.configure(font=self.config_manager.get_regular_font(), wrap=WORD, width=300, height=150)
        field.grid(row=row, column=column, pady=self.config_manager.NEW_NOTE_INPUT_PADY,
                             padx=self.config_manager.NEW_NOTE_INPUT_PADX)
        return field


    def display_status_input(self, parent: Frame, row: int, column: int):
        field = self.display_new_note_input(parent, row, column)
        field.configure(state=DISABLED, height=500, width=300)
        return field

    def display_new_note_label(self, text: str, parent: Frame, row: int, column: int) -> Label:
        field = Label(parent)
        field.configure(
            text=text,
            font=self.config_manager.get_regular_font(),
            wraplength=300,
            justify=LEFT)
        field.grid(row=row, column=column, pady=self.config_manager.NEW_NOTE_LABEL_PADY,
                             padx=self.config_manager.NEW_NOTE_LABEL_PADX)
        return field

    def display_warning_label(self, text: str, parent: Frame, row: int, column: int) -> Label:
        field = Label(parent)
        field.configure(
            text=text,
            font=self.config_manager.get_large_font(),
            wraplength=300,
            justify=LEFT,
            text_color="red")
        field.grid(row=row, column=column, pady=self.config_manager.NEW_NOTE_LABEL_PADY,
                             padx=self.config_manager.NEW_NOTE_LABEL_PADX)
        return field


    def display_button(self, text: str, parent: Frame, row: int, column: int, is_primary: bool = False) -> Button:
        field = Button(parent)
        field.configure(
            text=text,
            font=self.config_manager.get_large_font(),
            border_spacing=self.config_manager.BUTTON_BORDER_SPACING,
            fg_color=self.config_manager.SECONDARY_BUTTON_COLOR, hover_color=self.config_manager.SECONDARY_BUTTON_COLOR_HOVER)

        if is_primary:
            field.configure(fg_color=self.config_manager.PRIMARY_BUTTON_COLOR, hover_color=self.config_manager.PRIMARY_BUTTON_COLOR_HOVER)
        field.grid(row=row, column=column, pady=self.config_manager.BUTTON_PADY,
                   padx=self.config_manager.BUTTON_PADX)
        return field

    def display_title(self, text: str, parent: Frame, row: int, column: int) -> Label:
        field = Label(parent)
        field.configure(
            text=text,
            font=self.config_manager.get_large_font(),
            wraplength=300,
            justify=LEFT,
            fg_color=self.config_manager.TITLE_BACKGROUND,
            corner_radius=3
        )
        field.grid(row=row, column=column, pady=self.config_manager.NEW_NOTE_LABEL_PADY,
                             padx=self.config_manager.NEW_NOTE_LABEL_PADX)
        return field

    def display_frame(self, parent: Frame | Toplevel, row: int, column: int, title: str = "",  **kwargs) -> Frame:
        parent_frame = Frame(parent)
        parent_frame.configure(
            border_color=self.config_manager.FRAME_BORDER,
            border_width=2,
            fg_color=self.config_manager.FRAME_BACKGROUND)
        parent_frame.grid_rowconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid(row=row, column=column, pady=10, padx=20, sticky="nsew", **kwargs)

        if title != "":
            self.display_title(title, parent_frame, 0, 0)
        sub_frame = Frame(parent_frame)
        sub_frame.configure(fg_color=self.config_manager.FRAME_BACKGROUND)
        sub_frame.grid(row=1, column=0, pady=10, padx=20)

        return sub_frame
