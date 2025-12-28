import tkinter as tk
from tkinter import ttk, Menu
from datetime import datetime

class CurrencyUI(tk.Tk):
    # Background colors
    _color1="#6A0DAD"
    _color2="#66ccff"
    _color_white = "#ffffffff"
    
    _top_color1 = "#6A0DAD"     # фіолетовий
    _top_color2 = "#55CCFF"     # блакитний
    _bottom_color = "#55CCFF"
    
    # Fonts
    _font_main = ("Segoe UI", 16, "bold")
    _font_small = ("Segoe UI", 14)
    
    # Coordinates
    _columns = [20, 220, 360]
    _rows = [20, 60, 100]
    
    # Advisor variables
    _currencies = ["USD", "EUR", "GBP", "CHF", "PLN", "Silver", "Gold", "Platinum"]
    _selected_currency = "USD"
    
    _best_buy_rate = 44.48
    _best_buy_bank = "RadaBank"
    
    _best_sell_rate = 46.54
    _best_sell_bank = "Raiffaisenbank"
    
    
    def __init__(self):
        super().__init__()
        self.title("Currency Exchange Advisor")
        self.geometry("900x600")
        self.configure(bg="#cce6ff")

        self._create_menu() # ---- Меню ----
        self._build_tabs() # ---- Основна панель з табами ----

    # ====== ++ Menu =========================
    def _create_menu(self):
        menubar = Menu(self)
        file_menu = Menu(menubar, tearoff=0)
        edit_menu = Menu(menubar, tearoff=0)

        # Розділ 1
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Exit", command=self.quit)

        # Розділ 2
        edit_menu.add_command(label="Update")
        edit_menu.add_command(label="Refresh Rates")
        edit_menu.add_command(label="Settings")

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Actions", menu=edit_menu)

        self.config(menu=menubar)

    # ====== ++ Build Tabs ===================
    def _build_tabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)

        tab_status = ttk.Frame(notebook)
        tab_history = ttk.Frame(notebook)
        notebook.add(tab_status, text="Current Status")
        notebook.add(tab_history, text="History")
        
        self.fill_status_tab(tab_status)
        # self.fill_history_tab(tab_history)

    def fill_status_tab(self, parent):
        print('start create top panel')
        self._create_top_panel(parent)
        self._create_bottom_panel(parent)

    # ====== Upper panel (gradient) =========
    def _create_top_panel(self, parent):
        top_panel = GradientFrame(parent, color1=self._color1, color2=self._color2, height=220)
        top_panel.pack(fill="x")

        # first line: date currency lable, currency combobox
        date_str = datetime.now().strftime("%d.%m.%Y")
        top_panel.create_text(
            self._columns[0], self._rows[0],
            text=f"Date: {date_str}",
            font=self._font_main,
            fill="white",
            anchor="nw"
        )
        
        top_panel.create_text(
            self._columns[1], self._rows[0],
            text=f"Currency ",
            font=self._font_main,
            fill="white",
            anchor="nw"
        )
        
        # Combobox currency
        self._selected_currency = tk.StringVar()
        currency_combobox = ttk.Combobox(
            top_panel,
            textvariable=self._selected_currency,
            values=self._currencies,
            width=self.get_max_len(self._currencies) + 2,
            state = "readonly"
        )
          
        # Вставляємо у Canvas
        window_id = top_panel.create_window(self._columns[2], self._rows[0], window=currency_combobox, anchor="nw")
                        
        def make_transparent():
            bg = top_panel.get_bg_at(self._columns[2], self._rows[0])

            style = ttk.Style()
            style.configure(
                "Transparent.TCombobox",
                fieldbackground=bg,
                background=bg,
                foreground="black",
                borderwidth=0,
                relief="flat",
                padding=0,
                font=self._font_main,
            )
                        
        currency_combobox.configure(style="Transparent.TCombobox", font=self._font_main)
        top_panel.after(50, make_transparent)
        
        def set_default():
            currency_combobox.set("USD")
            
        top_panel.after(10, set_default)    
        
        # 2-й ряд: Best Buy, rate, Bank
        
        top_panel.create_text(
            self._columns[0], self._rows[1],
            text=f"Best buy ",
            font=self._font_main,
            fill="white",
            anchor="nw"
        )
        
        top_panel.create_text(
            self._columns[1], self._rows[1],
            text=self._best_buy_rate,
            font=self._font_main,
            fill="white",
            anchor="nw"
        )
        
        top_panel.create_text(
            self._columns[2], self._rows[1],
            text=self._best_buy_bank,
            font=self._font_main,
            fill="white",
            anchor="nw"
        )
       

        # 3-й ряд: Best sell, rate, bank
        top_panel.create_text(
            self._columns[0], self._rows[2],
            text=f"Best sell ",
            font=self._font_main,
            fill="white",
            anchor="nw"
        )
        
        top_panel.create_text(
            self._columns[1], self._rows[2],
            text=self._best_sell_rate,
            font=self._font_main,
            fill="white",
            anchor="nw"
        )
        
        top_panel.create_text(
            self._columns[2], self._rows[2],
            text=self._best_sell_bank,
            font=self._font_main,
            fill="white",
            anchor="nw"
        )

        # Заповнення кольором фону прозорих елементів
        for widget in top_panel.winfo_children():
            widget.configure(background=self._color1)
        
    # ====== Bottom panel  ==================    
    def _create_bottom_panel(self, parent):
        bottom_panel = tk.Frame(parent, bg=self._color2)
        # bottom_panel.pack(fill="both", expand=True)

    # # ====== Нижня панель з таблицею ======
    # def _create_bottom_panel(self, parent):
        
        # Headings and background styles
        style = ttk.Style()
        style.theme_use("default")

        # ---- Стиль заголовків ----
        style.configure(
            "Treeview.Heading",
             background=self._color1,
            foreground="white",
            font=self._font_small
            )

        # ---- Стиль тіла таблиці ----
        style.configure(
            "Treeview",
            background=self._color2,
            fieldbackground=self._color2,  # заливка фону під рядками
            foreground="black",
            rowheight=24
            )
        # ---- Стиль вибраного рядка ----
        style.map(
            "Treeview",
            background=[("selected", "#99bbff")],
            foreground=[("selected", "black")]
            )
        
        columns = ("Bank", "Buy rate", "Sell rate")
        
        self.tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self._sort_tree(c, False))
            self.tree.column(col, width=150, anchor="center")

    #     # Прокрутка
        vsb = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    #     # Дані таблиці (замість запиту до БД)
        data = [
            ("PrivatBank", "39.3000", "40.1000"),
            ("MonoBank", "39.4500", "40.1500"),
            ("OschadBank", "39.2000", "40.0500"),
            ("PUMB", "39.3800", "40.0900")
        ]
        for row in data:
            self.tree.insert("", "end", values=row)

    #     # Подія виділення рядка
        self.tree.bind("<ButtonRelease-1>", self._on_select_row)

    # ====== Події ======
    def _on_select_row(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])["values"]
            print("Selected row:", item)

    def _sort_tree(self, col, reverse):
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        data.sort(reverse=reverse)
        for index, (val, k) in enumerate(data):
            self.tree.move(k, "", index)
        self.tree.heading(col, command=lambda: self._sort_tree(col, not reverse))
    
    def get_max_len(self, arg =[]):
        '''
        Return len of list element which has max lenght
        '''
        if arg is None:
            return 0
        
        max_len = 0
        for i in arg:
            if len(i) > max_len:
                max_len = len(i)
        return max_len        

# ====== Клас для градієнтного фону ======
class GradientFrame(tk.Canvas):
    def __init__(self, parent, color1, color2, height=200, **kwargs):
        super().__init__(parent, height=height, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self._cached_colors = {}
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        
        (r1, g1, b1) = self.winfo_rgb(self.color1)
        (r2, g2, b2) = self.winfo_rgb(self.color2)
        r_ratio = float(r2 - r1) / max(height, 1)
        g_ratio = float(g2 - g1) / max(height, 1)
        b_ratio = float(b2 - b1) / max(height, 1)
        
        # очищуємо попередній кеш
        self._cached_colors.clear()
        
        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%04x%04x%04x" % (nr, ng, nb) # color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"  #use this if falls
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)
            # кешуємо колір для цього рядка (y = i)
            self._cached_colors[i] = color
        self.lower("gradient")
     
    def get_bg_at(self, x, y):
        """
        Повертає колір у форматі #RRGGBB для координати (x,y).
        Ми кешуємо кольори по y-координаті, бо градієнт по вертикалі.
        """
        try:
            y_int = int(y)
        except (TypeError, ValueError):
            return "#000000"
        # обмежимо y в рамках від 0..(height-1)
        h = self.winfo_height() or 1
        if y_int < 0:
            y_int = 0
        if y_int >= h:
            y_int = h - 1
              
        
        return self._cached_colors.get(y_int, "#000000")    

# ====== Запуск ======
if __name__ == "__main__":
    app = CurrencyUI()
    app.mainloop()
