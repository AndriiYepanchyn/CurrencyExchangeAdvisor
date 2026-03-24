import tkinter as tk
import repositories.RepositoryInterface as RepositoryInterface
from ui.EditableTablePanel import EditableTablePanel


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
        
        self.table = EditableTablePanel(self, repository)
        self.table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
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
        
    