from tkinter import DISABLED, LEFT

from customtkinter import CTkLabel as Label, WORD, CTkFrame as Frame, CTkTextbox as Text, CTkTextbox, \
    CTkButton as Button, CTkToplevel as Toplevel

from src.manager.ConfigManager import ConfigManager


class UILayoutHelper:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager

    def display_new_note_input(self, parent: Frame, row: int, column: int) -> CTkTextbox:
        field = Text(master=parent)
        field.configure(font=self.config_manager.get_regular_font(), wrap=WORD, width=200, height=100)
        field.grid(row=row, column=column, pady=self.config_manager.NEW_NOTE_INPUT_PADY,
                             padx=self.config_manager.NEW_NOTE_INPUT_PADX)
        return field


    def display_status_input(self, parent: Frame, row: int, column: int):
        field = self.display_new_note_input(parent, row, column)
        field.configure(state=DISABLED, height=400)
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
            font=self.config_manager.get_header_font(),
            wraplength=300,
            justify=LEFT,
            text_color="red")
        field.grid(row=row, column=column, pady=self.config_manager.NEW_NOTE_LABEL_PADY,
                             padx=self.config_manager.NEW_NOTE_LABEL_PADX)
        return field


    def display_button(self, text: str, parent: Frame, row: int, column: int) -> Button:
        field = Button(parent)
        field.configure(text=text, font=self.config_manager.get_header_font())
        field.grid(row=row, column=column, pady=self.config_manager.BUTTTON_PADY,
                             padx=self.config_manager.BUTTTON_PADX)
        return field

    def display_text(self, text: str, parent: Frame, row: int, column: int) -> Text:
        field = Text(parent)
        field.configure(text=text, font=self.config_manager.get_regular_font())
        field.grid(row=row, column=column, pady=self.config_manager.BUTTTON_PADY, padx=self.config_manager.BUTTTON_PADX)
        return field

    def display_title(self, text: str, parent: Frame, row: int, column: int) -> Label:
        field = Label(parent)
        field.configure(
            text=text,
            font=self.config_manager.get_header_font(),
            wraplength=300,
            justify=LEFT,
            fg_color="#edfffe"
        )
        field.grid(row=row, column=column, pady=self.config_manager.NEW_NOTE_LABEL_PADY,
                             padx=self.config_manager.NEW_NOTE_LABEL_PADX)
        return field

    def display_frame(self, parent: Frame | Toplevel, row: int, column: int, title: str = "",  **kwargs) -> Frame:
        parent_frame = Frame(parent)
        parent_frame.configure(border_color="gray", border_width=2)
        parent_frame.grid(row=row, column=column, pady=10, padx=20, **kwargs)

        if title != "":
            self.display_title(title, parent_frame, 0, 0)
        sub_frame = Frame(parent_frame)
        sub_frame.grid(row=1, column=0, pady=10, padx=20)

        return sub_frame
