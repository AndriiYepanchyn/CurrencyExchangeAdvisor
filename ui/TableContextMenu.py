import tkinter as tk
from tkinter import ttk, messagebox

class Table_context_menu(tk.Menu):
    def __init__(self):
        super(self, tearoff=0)
        
        self.add_command(label = 'Add row')
        self.menu.add_command(label="Редагувати", command=self.edit_selected)

        self.menu.add_separator()

        self.menu.add_command(label="Видалити рядок", command=self.delete_row)
        self.menu.add_command(label="Видалити виділені", command=self.delete_selected)

        self.menu.add_separator()

        self.menu.add_command(label="Копіювати", command=self.copy_rows)
        self.menu.add_command(label="Вставити", command=self.paste_rows)
        