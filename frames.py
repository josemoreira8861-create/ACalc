import tkinter as tk
from tkinter import ttk

# BASE DOS FRAMES
class BaseToolFrame(ttk.Frame):
    def __init__(self, parent, tool_name, on_calculate):
        super().__init__(parent)

        self.tool_name = tool_name
        self.on_calculate = on_calculate


# COTA DIAMETRAL SOBRE ESFERAS
class FrameEsferas(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "esferas", on_calculate)

        # ---------------- VARIABLES FIRST ----------------
        self.diameter_var = tk.DoubleVar()
        self.type_var = tk.StringVar()

        # ---------------- UI ----------------
        ttk.Label(self, text="Type").pack()

        self.type_cb = ttk.Combobox(
            self,
            textvariable=self.type_var,
            state="readonly"
        )
        self.type_cb["values"] = ["Option1", "Option2"]
        self.type_cb.pack()

        ttk.Label(self, text="Diameter").pack()
        ttk.Entry(self, textvariable=self.diameter_var).pack()

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

        self.artigo = tk.StringVar()
        self.modulo = tk.DoubleVar()
        self.beta = tk.DoubleVar()

        ttk.Label(self, text="Rollete").grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

        ttk.Label(self, text="Artigo").grid(row=1, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.artigo).grid(row=1, column=1, sticky="w")

        ttk.Label(self, text="Módulo (Mn)").grid(row=2, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.modulo).grid(row=2, column=1, sticky="w")

        ttk.Label(self, text="Beta (graus)").grid(row=3, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.beta).grid(row=3, column=1, sticky="w")

        ttk.Button(self, text="Calculate", command=self.send_data)\
            .grid(row=4, column=0, columnspan=2, pady=10, sticky="w")

        self.columnconfigure(1, weight=1)

    def send_data(self):
        self.on_calculate(self.tool_name, {
            "artigo": self.artigo.get(),
            "modulo": self.modulo.get(),
            "beta": self.beta.get(),
        })

class FrameReishauer(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "reishauer", on_calculate)
        ttk.Label(self, text="Frame Reishauer").pack()