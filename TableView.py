import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import random


class TableView(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.headers = ["ID", "Name", "City", "Balance"]

        self.tree = ttk.Treeview(
            self,
            columns=self.headers,
            show="headings",
            selectmode="extended"
        )

        for h in self.headers:
            self.tree.heading(h, text=h, command=lambda c=h: self.sort_column(c, False))
            self.tree.column(h, anchor="w")

        self.tree.pack(fill="both", expand=True)

        self.editor = None # Editor cell object definition

        self.load_data()

        self.tree.bind("<Double-1>", self.edit_cell)
        self.tree.bind("<Return>", self.edit_cell)

        self.tree.bind("<Control-c>", self.copy)
        self.tree.bind("<Control-v>", self.paste)

        self.auto_size()

    # ---------------- DATA ----------------

    def load_data(self):

        names = ["John", "Anna", "Mike", "Sara", "Alex"]
        cities = ["Kyiv", "Dnipro", "Lviv", "Odessa"]

        for i in range(250):
            self.tree.insert(
                "",
                "end",
                values=(
                    i,
                    random.choice(names),
                    random.choice(cities),
                    round(random.uniform(100, 5000), 2)
                )
            )

    # ---------------- AUTOSIZE ----------------

    def auto_size(self):

        font = tkfont.nametofont("TkDefaultFont")

        for col in self.headers:

            max_width = font.measure(col)

            for row in self.tree.get_children():
                value = str(self.tree.set(row, col))
                width = font.measure(value)

                if width > max_width:
                    max_width = width

            self.tree.column(col, width=max_width + 20)

    # ---------------- SORT ----------------

    def sort_column(self, col, reverse):

        data = [
            (self.tree.set(child, col), child)
            for child in self.tree.get_children("")
        ]

        try:
            data.sort(key=lambda t: float(t[0]), reverse=reverse)
        except:
            data.sort(reverse=reverse)

        for index, (val, child) in enumerate(data):
            self.tree.move(child, "", index)

        self.tree.heading(
            col,
            command=lambda: self.sort_column(col, not reverse)
        )

    # ---------------- EDIT ----------------

    def edit_cell(self, event):

        region = self.tree.identify("region", event.x, event.y)

        if region != "cell":
            return

        row = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        x, y, w, h = self.tree.bbox(row, column)

        value = self.tree.set(row, column)

        self.editor = tk.Entry(self.tree)
        self.editor.place(x=x, y=y, width=w, height=h)

        self.editor.insert(0, value)
        self.editor.focus()

        self.editor.bind(
            "<Return>",
            lambda e: self.save_edit(row, column)
        )

        self.editor.bind(
            "<FocusOut>",
            lambda e: self.editor.destroy()
        )

    def save_edit(self, row, column):

        value = self.editor.get()
        self.tree.set(row, column, value)

        self.editor.destroy()

    # ---------------- COPY ----------------

    def copy(self, event=None):

        rows = self.tree.selection()

        data = []

        for r in rows:
            values = self.tree.item(r)["values"]
            data.append("\t".join(map(str, values)))

        text = "\n".join(data)

        self.clipboard_clear()
        self.clipboard_append(text)

    # ---------------- PASTE ----------------

    def paste(self, event=None):

        try:
            text = self.clipboard_get()
        except:
            return

        rows = text.split("\n")

        selected = self.tree.selection()

        if not selected:
            return

        start = self.tree.index(selected[0])

        for r, row in enumerate(rows):

            values = row.split("\t")

            if start + r >= len(self.tree.get_children()):
                break

            item = self.tree.get_children()[start + r]

            for c, value in enumerate(values):
                if c < len(self.headers):
                    self.tree.set(item, self.headers[c], value)


# ---------------- RUN ----------------

root = tk.Tk()
root.geometry("700x500")

table = TableView(root)
table.pack(fill="both", expand=True)

root.mainloop()