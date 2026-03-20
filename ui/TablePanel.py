import tkinter as tk
from tkinter import ttk, Menu
from repositories.RepositoryInterface import RepositoryInterfce
import tkinter.font as tkFont

class Table(tk.Frame):
    _color2="#66ccff"
    
    def __init__(self, parent, repository : RepositoryInterfce):
        super().__init__(parent, bg=self._color2)
                
        self._repository = repository
        self.columns = repository.get_headers()
        self.rows = repository.get_rows()
        
        self._dirty_row = None
        self.clipboard_rows = []
        
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
            self.tree.column(col, width=150, anchor="center")
            
        for row in self.rows:
            self.tree.insert("", tk.END, values=row) 
        
        
       # Прокрутка
        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        
        self.autosize_columns()     
        self.tree.tag_configure("new_row", background="white")   
        
        # Подія виділення рядка
        self.tree.bind("<ButtonRelease-1>", self.on_select_row)
        
        # подвійний клік для редагування
        # self.tree.bind("<Double-1>", self.edit_cell)
        
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
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])["values"]
            print("Selected row:", item)

    def show_context_menu(self, event):

        
        iid = self.tree.identify_row(event.y)
        
        if iid:
            self.tree.selection_set(iid)
            
        self._context_menu.post(event.x_root, event.y_root)
            
    def create_context_menu(self):
        self.menu = tk.Menu(self, tearoff=0)

        self.menu.add_command(label="Додати рядок", command=self.add_row)
        self.menu.add_command(label="Редагувати", command=self.edit_selected)
        self.menu.add_separator()

        self.menu.add_command(label="Копіювати")#, command=self.copy_rows)
        self.menu.add_command(label="Вставити")#, command=self.paste_rows)
        self.menu.add_separator()

        self.menu.add_command(label="Видалити рядок")#, command=self.delete_row)
        self.menu.add_command(label="Видалити виділені")#, command=self.delete_selected)

        
        return self.menu
    
    def add_row(self):
        if self._dirty_row is not None:
            return
        
        self._dirty_row = True
        iid = self.tree.insert("", "end", values = [""] * len(self.columns), tags=("new_row"))
        self.tree.selection_set(iid) 
        self.edit_cell_by_iid(iid, "#1")
        
    def edit_selected(self):
        sel = self.tree.selection()
        if sel:
            self.edit_cell_by_iid(sel[0], "#1") 
            
    def edit_cell_by_iid(self, row, col):

        x, y, w, h = self.tree.bbox(row, col)
        value = self.tree.set(row, col)
        entry = tk.Entry(self.tree)
        entry.place(x=x, y=y, width=w, height=h)
        entry.insert(0, value)
        entry.focus()

        def save(event):
            self.tree.set(row, col, entry.get())
            entry.destroy()
            # рядок більше не dirty
            if row == self._dirty_row:
                self._dirty_row = False

        entry.bind("<Return>", save)  
        entry.bind("<FocusOut>", save)                
    
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
