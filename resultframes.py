import tkinter as tk
from tkinter import ttk


class BaseResultsFrame(ttk.Frame):
    def show_results(self, results):
        raise NotImplementedError


# ---------------- ROLLETE ----------------
class RolleteResultsFrame(BaseResultsFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.text = tk.Text(self)
        self.text.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def show_results(self, results):
        self.text.delete("1.0", tk.END)

        for r in results:
            self.text.insert(
                tk.END,
                f"A={r['A']} B={r['B']} C={r['C']} D={r['D']} err={r['erro']:.5f}\n"
            )


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