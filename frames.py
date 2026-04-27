import tkinter as tk
from tkinter import ttk


# ---------------- BASE FRAME ----------------
class BaseToolFrame(ttk.Frame):
    def __init__(self, parent, tool_name, on_calculate):
        super().__init__(parent)
        self.tool_name = tool_name
        self.on_calculate = on_calculate


# ---------------- ESFERAS ----------------
class FrameEsferas(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "esferas", on_calculate)

        self.diameter_var = tk.DoubleVar()
        self.type_var = tk.StringVar()

        ttk.Label(self, text="Diameter").pack()
        ttk.Entry(self, textvariable=self.diameter_var).pack()

        ttk.Label(self, text="Type").pack()
        self.type_cb = ttk.Combobox(self, textvariable=self.type_var, state="readonly")
        self.type_cb["values"] = ["Option1", "Option2"]
        self.type_cb.pack()

        ttk.Button(self, text="Calculate", command=self.send_data).pack()

    def send_data(self):
        self.on_calculate(self.tool_name, {
            "diameter": self.diameter_var.get(),
            "type": self.type_var.get(),
        })


# ---------------- OTHER FRAMES ----------------
class FrameRoda(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "roda", on_calculate)
        ttk.Label(self, text="Frame Roda Dentada").pack()


class FrameEngrenagem(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "engrenagem", on_calculate)
        ttk.Label(self, text="Frame Engrenagem").pack()


class FrameSemFim(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "semfim", on_calculate)
        ttk.Label(self, text="Frame Sem-fim").pack()


class FrameRollete(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "rollete", on_calculate)
        ttk.Label(self, text="Frame Rollete").pack()


class FrameReishauer(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "reishauer", on_calculate)
        ttk.Label(self, text="Frame Reishauer").pack()