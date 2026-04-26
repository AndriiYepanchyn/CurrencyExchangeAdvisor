import tkinter as tk
from tkinter import ttk, Menu
from repositories.RepositoryInterface import RepositoryInterfce
import tkinter.font as tkFont
from tkinter import messagebox


class TablePanel(tk.Frame):
    _color2="#66ccff"
    
    def __init__(self, parent, repository : RepositoryInterfce):
        super().__init__(parent, bg=self._color2)
        
        try:        
            self._repository = repository
            self.columns = repository.get_headers()
            self.rows = repository.get_rows()
        except  Exception as e:
            title = repository.get_title()
            result = messagebox.showerror(
                "Can't get table data ",
                f"Cant't get table data using repositiry {title}. \n{e}" 
            )  
        
        self.selected_rows = None
        
        # Creating table
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(container, 
                                 columns=self.columns, 
                                 show="headings", 
                                 selectmode="extended"
                                 )
        
        for col in self.columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_tree(c, False))
            self.tree.column(col, width=150, anchor="w")
            
        for row in self.rows:
            self.tree.insert("", tk.END, values=row) 
        
        
       # Прокрутка
        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        
        self.autosize_columns()     
          
        # Подія виділення рядка
        self.tree.bind("<ButtonRelease-1>", self.on_select_row)
        
        # Context menu
        self._context_menu = self.create_context_menu()
        self.tree.bind("<Button-3>", self.show_context_menu)
       
    # ====== Події ======
    def sort_tree(self, col, reverse):
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
            
        self.tree.heading(col, command=lambda: self.sort_tree(col, not reverse))
    
    def on_select_row(self, event):
        self.selected_rows = self.tree.selection()

    def show_context_menu(self, event):
        iid = self.tree.identify_row(event.y)
        
        if iid:
            self.tree.selection_set(iid)
            
        self._context_menu.post(event.x_root, event.y_root)
            
    def create_context_menu(self):
        self.menu = tk.Menu(self, tearoff=0)
        return self.menu
    
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
