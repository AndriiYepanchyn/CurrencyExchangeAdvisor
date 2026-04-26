from ui.TablePanel import TablePanel
import tkinter as tk
from tkinter import ttk, Menu
from tkinter import messagebox


class EditableTablePanel(TablePanel):
    def __init__(self, parent, repository):
        super().__init__(parent, repository)
        self._editing = False
        
        self.tree.tag_configure("new_row", background="white") 
        
        # Додатковий метод по МВ1 на таблиці
        self.tree.bind("<Button-1>", self.on_click_block, add="+")
                
        # подвійний клік для редагування
        # self.tree.bind("<Double-1>", self.edit_cell)
      
    #=====  Події  ========================  
    def create_context_menu(self):
        self.menu = super().create_context_menu()

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
       iid = self.tree.insert("", "end", values = [""] * len(self.columns), tags=("new_row"))
       self._editing_row = iid
       self._editing_col_index = 0
       self._editing = True
       
       self.start_row_edit()    
       
    def start_row_edit(self):
        col = f"#{self._editing_col_index + 1}"
        self.edit_cell_by_iid(self._editing_row, col)   
        
    def edit_cell_by_iid(self, row, col):
        # Створення клітинки поверх tree
        x, y, w, h = self.tree.bbox(row, col)
        value = self.tree.set(row, col)
        entry = tk.Entry(self.tree)
        entry.place(x=x, y=y, width=w, height=h)
        entry.insert(0, value)
        entry.focus()
        
        if self._editing:
            expected = f"#{self._editing_col_index + 1}"
            if col != expected:
                return

        def save(event):
            value = entry.get()
            self.tree.set(row, col, value)
            entry.destroy()
            
            if self._editing:
                self.on_cell_saved(value) 

        entry.bind("<Return>", save)  
        entry.bind("<FocusOut>", save)       
            
    def finish_row_edit(self):
        iid = self._editing_row
        values = self.tree.item(iid)["values"]

        saving_row = dict(zip(self.columns, values))
        self._repository.insert(saving_row)
        
        self._editing = False
        self._editing_row = None
        self._editing_col_index = None     
        
    def on_cell_saved(self, value):
        if value.strip() == "":
            return  # можна додати валідацію

        self._editing_col_index += 1

        # якщо ще є колонки
        if self._editing_col_index < len(self.columns):
            self.start_row_edit()
        else:
            self.finish_row_edit() 
            
    def on_click_block(self, event):
        if not self._editing:
            return

        row = self.tree.identify_row(event.y)

        # якщо клік НЕ в поточний рядок
        if row != self._editing_row:
            result = messagebox.askyesno(
                "Незавершений рядок",
                "Рядок не буде збережений. Покинути редагування?"
            )

            if result:
                self.tree.delete(self._editing_row)
                self._editing = False
            else:
                self.start_row_edit()

            return "break"  # блокує стандартну поведінку     
        
    def edit_selected(self, event):
        row = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)

        if not row or not col:
            return
        
        print('Click on column = ', col)
        self.edit_cell_by_iid(row, col)   
        
        # TODO check implementation
    def delete_selected_row(self):
        selected = self.tree.selection()
        if not selected:
            return

        item_id = selected[0]
        values = self.tree.item(item_id)["values"]

        row_id = values[0]
        self.repository.delete(row_id)

        self.tree.delete(item_id)                   