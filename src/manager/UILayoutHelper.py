
from customtkinter import CTkLabel as Label, WORD, CTkFrame as Frame, CTkTextbox as Text, CTkTextbox, \
    CTkButton as Button

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

    def display_new_note_label(self, text: str, parent: Frame, row: int, column: int) -> Label:
        field = Label(parent)
        field.configure(text=text, font=self.config_manager.get_header_font())
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
