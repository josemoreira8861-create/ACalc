import tkinter as tk
from tkinter import ttk


class BaseResultsFrame(ttk.Frame):
    def show_results(self, results):
        raise NotImplementedError


# ---------------- ROLLETE ----------------
class RolleteResultsFrame(BaseResultsFrame):
    def __init__(self, parent):
        super().__init__(parent)

        columns = ("razao", "erro", "A", "B", "C", "D")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.tree.heading("razao", text="Razão")
        self.tree.heading("erro", text="Erro")
        self.tree.heading("A", text="A")
        self.tree.heading("B", text="B")
        self.tree.heading("C", text="C")
        self.tree.heading("D", text="D")

        # Optional: column widths
        self.tree.column("razao", width=100)
        self.tree.column("erro", width=100)

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar (important for tables)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        scrollbar.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def show_results(self, results):
        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not results:
            return

        # Insert rows
        for r in results:
            self.tree.insert("", "end", values=(
                f"{r['razaom']:.8f}",
                f"{r['erro']:.8f}",
                r["A"],
                r["B"],
                r["C"],
                r["D"],
            ))


# ---------------- ESFERAS ----------------
class EsferasResultsFrame(BaseResultsFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self)
        self.label.grid()

    def show_results(self, results):
        self.label.config(text=str(results))


RESULT_FRAMES = {
    "rollete": RolleteResultsFrame,
    "esferas": EsferasResultsFrame,
}