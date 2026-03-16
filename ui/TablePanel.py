import tkinter as tk
from tkinter import ttk, Menu
from repositories.RepositoryInterface import RepositoryInterfce
import tkinter.font as tkFont

class Table(tk.Frame):
    _color2="#66ccff"
    
    def __init__(self, parent, repository : RepositoryInterfce):
        super().__init__(parent, bg=self._color2)
        # bottom_panel.pack(fill="both", expand=True)
        
        self._repository = repository
        columns = repository.get_headers()
        data = repository.get_rows()
        
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(container, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self._sort_tree(c, False))
            self.tree.column(col, width=150, anchor="center")
            
        for row in data:
            self.tree.insert("", tk.END, values=row) 
        
        
       # Прокрутка
        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        
        self.autosize_columns()        
        
        # Подія виділення рядка
        self.tree.bind("<ButtonRelease-1>", self._on_select_row)
    
        
    # ====== Події ======
    def _on_select_row(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])["values"]
            print("Selected row:", item)

    def _sort_tree(self, col, reverse):
        # перевіряємо чи колонка числова
        # TODO Optimize cheking loops 
        is_numeric = True
        values = [self.tree.set(k, col) for k in self.tree.get_children("")]
        for v in values:
            try:
                float(v)
            except ValueError:
                is_numeric = False
                break
        if(is_numeric):
           data = [(float(self.tree.set(k, col)), k) for k in self.tree.get_children("")]
        else:
            data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]    
        
        data.sort(reverse=reverse)
        for index, (val, k) in enumerate(data):
            self.tree.move(k, "", index)
            
        self.tree.heading(col, command=lambda: self._sort_tree(col, not reverse))
    
    # -------  Service methods  ---------------------- 
        
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
