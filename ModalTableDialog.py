import tkinter as tk
from tkinter import ttk
import DataBaseApi
from SelectQuerryEnum import SelectEnum


class ModalTableDialog(tk.Toplevel):
    
    select_bank_querry = 'SELECT * FROM banks'
    selec_currency_querry = 'SELECT * FROM currency'
    
    querry_selector = {SelectEnum.BANK_INFO: select_bank_querry, 
                       SelectEnum.CURRENCY_INFO: selec_currency_querry}

    def __init__(self, parent, querry_option: SelectEnum):
        super().__init__(parent)
        print("input option = ", querry_option)
        print("Selected querry = ", self.querry_selector.get(querry_option))

        self.title("Changing parameters of " + querry_option.value)
        self.geometry("700x400")

        # --- модальність ---
        self.transient(parent)
        self.grab_set()
        self.center_on_parent(parent)
        
        # --- Database connection ---
        database_connector = DataBaseApi.DataBaseApi("sqlite")
        database_connector.connect()
        self.headers, self.rows = database_connector.get_table(self.querry_selector.get(querry_option))
        
        print('Headers: ', self.headers, "headers type: ", type(self.headers))
        print('Rows: ', self.rows)

        # --- таблиця ---
        self.tree = ttk.Treeview(self, columns=self.headers + ["action"], show="headings")

        for h in self.headers:
            self.tree.heading(h, text=h)
            self.tree.column(h, width=120)

        self.tree.heading("action", text="action")
        self.tree.column("action", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    #     # --- кнопки ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=5)

        tk.Button(btn_frame, text="New line", command=self.add_new_row).pack(side=tk.LEFT, padx=5)

    #     # --- заповнення ---
        for row in self.rows:
            self.insert_row(row)

        self.tree.bind("<Button-1>", self.on_click)

    # # ================== TABLE ==================
    def insert_row(self, row):
        self.tree.insert("", tk.END, values=list(row) + ["Видалити"])

    def add_new_row(self):
        empty = [""] * len(self.headers)
        item = self.tree.insert("", tk.END, values=empty + ["Зберегти"])
        self.tree.selection_set(item)
        self.tree.focus(item)

    def on_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)

        if not row_id:
            return

        col_index = int(column.replace("#", "")) - 1

        # Клік по кнопці
        if self.headers and col_index == len(self.headers):
            action = self.tree.item(row_id)["values"][-1]

            if action == "Видалити":
                self.handle_delete(row_id)

            elif action == "Зберегти":
                self.handle_insert(row_id)

    # def handle_delete(self, item_id):
    #     values = self.tree.item(item_id)["values"]
    #     row_id = values[0]  # припускаємо, що перший стовпець — id

    #     self.delete_from_db(row_id)
    #     self.tree.delete(item_id)

    # def handle_insert(self, item_id):
    #     values = self.tree.item(item_id)["values"][:-1]

    #     self.insert_into_db(values)

    #     # Після збереження
        # self.tree.set(item_id, "action", "Видалити")
    
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
        
        
    # # ================== DB ==================

    # def get_connection(self):
    #     return sqlite3.connect(self.db_path)

    # def delete_from_db(self, row_id):
    #     with self.get_connection() as con:
    #         con.execute(
    #             f"DELETE FROM {self.table_name} WHERE id = ?",
    #             (row_id,)
    #         )

    # def insert_into_db(self, values):
    #     placeholders = ",".join("?" * len(values))
    #     columns = ",".join(self.headers)

    #     with self.get_connection() as con:
    #         con.execute(
    #             f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})",
    #             values
    #         )


