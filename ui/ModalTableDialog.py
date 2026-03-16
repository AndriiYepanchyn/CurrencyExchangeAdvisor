import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import DataBaseApi
import repositories.RepositoryInterface as RepositoryInterface


class ModalTableDialog(tk.Toplevel):

    def __init__(self, parent, repository: RepositoryInterface):
        super().__init__(parent)
        self.repo = repository

        self.title("Changing parameters of " + self.repo.get_title())
        self.geometry("700x400")

        # --- модальність ---
        self.transient(parent)
        self.grab_set()
        self.center_on_parent(parent)
        
        self.headers, self.rows = self.repo.get_table()

        # --- таблиця ---
        self.tree = ttk.Treeview(self, columns=self.headers, show="headings")

        for h in self.headers:
            self.tree.heading(h, text=h)
            self.tree.column(h, width=120)

        

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    #     # --- заповнення ---
        for row in self.rows:
            self.insert_row(row)
            
        self.autosize_columns()    

        self.tree.bind("<Button-3>", self.show_context_menu)

     
    def on_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)

        if not row_id:
            return

        col_index = int(column.replace("#", "")) - 1              
                

    
# -------  Service methods  ---------------------- 
    def center_on_parent(self, parent):
        self.update_idletasks()
        parent.update_idletasks()

        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()

        sw = self.winfo_width()
        sh = self.winfo_height()

        x = px + (pw - sw) // 2
        y = py + (ph - sh) // 2

        self.geometry(f"+{x}+{y}")
        
    def autosize_columns(self):
        font = tkFont.nametofont("TkDefaultFont")

        for col in self.tree["columns"]:
            # ширина заголовка
            max_width = font.measure(col)

            # перевіряємо всі рядки
            for item in self.tree.get_children():
                cell_value = str(self.tree.set(item, col))
                cell_width = font.measure(cell_value)
                max_width = max(max_width, cell_width)

            # додаємо padding
            max_width += 4
            self.tree.column(col, width=max_width)        